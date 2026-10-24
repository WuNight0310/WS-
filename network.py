import json
import os
import re
import socket
import sys
import threading
import urllib.request
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != BASE_DIR:
    os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class WSNetNode:
    """提供區網與跨外網雙人對戰 Host 與 Client 封包通訊，支援 UPnP 自動開埠與域名隧道連線"""

    def __init__(self, on_msg_callback, on_disconnect_callback=None):
        self.on_msg = on_msg_callback
        self.on_disconnect = on_disconnect_callback
        self.sock = None
        self.conn = None
        self.is_host = False
        self.connected = False
        self._send_lock = threading.Lock()

    @staticmethod
    def get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            try:
                return socket.gethostbyname(socket.gethostname())
            except Exception:
                return "127.0.0.1"

    @staticmethod
    def get_public_ip_async(callback):
        """背景非阻塞查詢本機外網公網 IPv4"""
        def worker():
            for url in ["https://api.ipify.org", "https://ident.me", "https://ifconfig.me/ip"]:
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=3.5) as resp:
                        ip = resp.read().decode("utf-8").strip()
                        if ip and "." in ip and len(ip) <= 16:
                            callback(ip)
                            return
                except Exception:
                    pass
            callback(None)

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def parse_host_port(raw_address: str, default_port: int = 15780):
        """自動解析 'IP:Port'、'tcp://domain:port' 或純 IP/域名"""
        addr = raw_address.strip()
        for prefix in ["tcp://", "http://", "https://"]:
            if addr.lower().startswith(prefix):
                addr = addr[len(prefix):]
        addr = addr.strip("/")
        if ":" in addr:
            host_part, port_part = addr.rsplit(":", 1)
            try:
                return host_part.strip(), int(port_part.strip())
            except ValueError:
                return addr, int(default_port)
        return addr, int(default_port)

    @staticmethod
    def try_upnp_forward_async(port: int, callback=None):
        """使用純 Python 標準庫發送 SSDP 與 UPnP SOAP 自動向家用路由器申請外網 Port 轉發"""
        def worker():
            local_ip = WSNetNode.get_local_ip()
            ssdp_req = (
                "M-SEARCH * HTTP/1.1\r\n"
                "HOST: 239.255.255.250:1900\r\n"
                "MAN: \"ssdp:discover\"\r\n"
                "MX: 2\r\n"
                "ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n\r\n"
            )
            try:
                udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp.settimeout(2.2)
                udp.sendto(ssdp_req.encode("utf-8"), ("239.255.255.250", 1900))
                resp_data, _ = udp.recvfrom(4096)
                udp.close()
                resp_text = resp_data.decode("utf-8", errors="ignore")
                loc_match = re.search(r"(?i)LOCATION:\s*(http://[^\r\n]+)", resp_text)
                if not loc_match:
                    if callback:
                        callback(False, "未偵測到支援 UPnP 的路由器回應")
                    return
                desc_url = loc_match.group(1).strip()
                from urllib.parse import urljoin
                with urllib.request.urlopen(desc_url, timeout=3.0) as r:
                    xml_text = r.read().decode("utf-8", errors="ignore")

                control_url = None
                service_type = None
                for st in [
                    "urn:schemas-upnp-org:service:WANIPConnection:1",
                    "urn:schemas-upnp-org:service:WANPPPConnection:1",
                ]:
                    if st in xml_text:
                        idx = xml_text.find(st)
                        sub = xml_text[idx:idx + 1500]
                        c_match = re.search(r"<controlURL>([^<]+)</controlURL>", sub)
                        if c_match:
                            service_type = st
                            control_url = urljoin(desc_url, c_match.group(1).strip())
                            break
                if not control_url or not service_type:
                    if callback:
                        callback(False, "路由器未開放 WANIPConnection 介面")
                    return

                soap_body = f"""<?xml version="1.0"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<s:Body>
<u:AddPortMapping xmlns:u="{service_type}">
<NewRemoteHost></NewRemoteHost>
<NewExternalPort>{port}</NewExternalPort>
<NewProtocol>TCP</NewProtocol>
<NewInternalPort>{port}</NewInternalPort>
<NewInternalClient>{local_ip}</NewInternalClient>
<NewEnabled>1</NewEnabled>
<NewPortMappingDescription>WS_Simulator_TCP_{port}</NewPortMappingDescription>
<NewLeaseDuration>0</NewLeaseDuration>
</u:AddPortMapping>
</s:Body>
</s:Envelope>"""
                req = urllib.request.Request(
                    control_url,
                    data=soap_body.encode("utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=\"utf-8\"",
                        "SOAPAction": f'"{service_type}#AddPortMapping"',
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=3.5) as sr:
                    if sr.status in (200, 201):
                        if callback:
                            callback(True, f"UPnP 自動開埠成功 (TCP Port {port})")
                        return
            except Exception as e:
                if callback:
                    callback(False, f"UPnP 未生效 ({e})")
                return
            if callback:
                callback(False, "UPnP 未生效")

        threading.Thread(target=worker, daemon=True).start()

    def start_host(self, port=15780):
        self.is_host = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", int(port)))
        self.sock.listen(1)
        threading.Thread(target=self._accept_worker, daemon=True).start()

    def _accept_worker(self):
        try:
            conn, addr = self.sock.accept()
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.conn = conn
            self.connected = True
            if self.on_msg:
                self.on_msg({"type": "SYS_CONNECTED", "peer": f"{addr[0]}:{addr[1]}"})
            self._recv_loop(conn)
        except Exception as e:
            if self.connected and self.on_msg:
                self.on_msg({"type": "SYS_ERROR", "error": str(e)})

    def connect_to_host(self, ip_or_host, port=15780):
        self.is_host = False
        host, parsed_port = self.parse_host_port(ip_or_host, default_port=port)

        def worker():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(8.0)
                s.connect((host, int(parsed_port)))
                s.settimeout(None)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.conn = s
                self.connected = True
                if self.on_msg:
                    self.on_msg({"type": "SYS_CONNECTED", "peer": f"{host}:{parsed_port}"})
                self._recv_loop(s)
            except Exception as e:
                if self.on_msg:
                    self.on_msg({"type": "SYS_ERROR", "error": str(e)})

        threading.Thread(target=worker, daemon=True).start()

    def _recv_loop(self, conn):
        buf = ""
        while self.connected:
            try:
                data = conn.recv(16384)
                if not data:
                    break
                buf += data.decode("utf-8", errors="replace")
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if line:
                        try:
                            msg = json.loads(line)
                            if self.on_msg:
                                self.on_msg(msg)
                        except Exception:
                            pass
            except Exception:
                break
        self.connected = False
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except Exception:
                pass

    def send(self, payload: dict) -> bool:
        if self.connected and self.conn:
            try:
                raw = json.dumps(payload, ensure_ascii=False) + "\n"
                with self._send_lock:
                    self.conn.sendall(raw.encode("utf-8"))
                return True
            except Exception:
                self.connected = False
        return False

    def send_action_log(self, text: str, player_state_dict: dict = None, opp_state_dict: dict = None):
        payload = {"type": "ACTION_LOG", "text": text}
        if player_state_dict is not None:
            payload["sender_state"] = player_state_dict
        if opp_state_dict is not None:
            payload["receiver_state"] = opp_state_dict
        return self.send(payload)

    def close(self):
        self.connected = False
        for s in (self.conn, self.sock):
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        self.conn = None
        self.sock = None


def _launch_from_any_file():
    try:
        from main import launch_game
        launch_game()
        return
    except ImportError:
        pass


if __name__ == "__main__":
    _launch_from_any_file()
