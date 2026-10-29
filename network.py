import json
import os
import re
import socket
import sys
import threading
import urllib.request
import uuid
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.getcwd() != BASE_DIR:
    os.chdir(BASE_DIR)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


class WSNetNode:
    """提供區網與跨外網雙人對戰 Host 與 Client 封包通訊，支援 UPnP 自動開埠、隧道連線與雙向協議握手驗證"""

    def __init__(self, on_msg_callback, on_disconnect_callback=None):
        self.on_msg = on_msg_callback
        self.on_disconnect = on_disconnect_callback
        self.sock = None
        self.conn = None
        self.is_host = False
        self._hosting = False
        self.connected = False
        self.node_id = uuid.uuid4().hex[:12]
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
        """自動解析並淨化 'IP:Port'、'tcp://domain:port' 或純 IP/域名（自動修復手機鍵盤誤輸入之 !;! 與全形冒號）"""
        addr = (raw_address or "").strip()
        addr = addr.replace("!;!", ":").replace("：", ":").replace(" ", "")
        for prefix in ["tcp://", "http://", "https://", "tcp//", "http//", "https//"]:
            if addr.lower().startswith(prefix):
                addr = addr[len(prefix):]
        addr = addr.strip("/")
        if ":" in addr:
            host_part, port_part = addr.rsplit(":", 1)
            port_digits = re.sub(r"\D", "", port_part)
            if port_digits:
                try:
                    return host_part.strip(), int(port_digits)
                except ValueError:
                    pass
            return host_part.strip(), int(default_port)
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
        self._hosting = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", int(port)))
        self.sock.listen(5)
        threading.Thread(target=self._accept_worker, daemon=True).start()

    def _accept_worker(self):
        while self._hosting and not self.connected and self.sock:
            conn = None
            try:
                conn, addr = self.sock.accept()
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                conn.settimeout(5.0)
                buf = ""
                handshake_ok = False
                while "\n" not in buf and len(buf) < 4096:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    buf += chunk.decode("utf-8", errors="replace")
                if "\n" in buf:
                    first_line, rest_buf = buf.split("\n", 1)
                    hs_msg = json.loads(first_line.strip())
                    if isinstance(hs_msg, dict) and hs_msg.get("type") == "WS_HANDSHAKE":
                        ack_raw = json.dumps({
                            "type": "WS_HANDSHAKE_ACK",
                            "protocol": "WS_MASTER_DUEL_V2",
                            "node_id": self.node_id,
                        }) + "\n"
                        conn.sendall(ack_raw.encode("utf-8"))
                        handshake_ok = True
                if not handshake_ok:
                    try:
                        conn.close()
                    except Exception:
                        pass
                    continue
                conn.settimeout(None)
                self.conn = conn
                self.connected = True
                self._hosting = False
                if self.on_msg:
                    self.on_msg({"type": "SYS_CONNECTED", "peer": f"{addr[0]}:{addr[1]}"})
                self._recv_loop(conn, initial_buf=rest_buf)
                return
            except Exception:
                if conn is not None and not self.connected:
                    try:
                        conn.close()
                    except Exception:
                        pass
                if not self._hosting:
                    break
                continue

    def connect_to_host(self, ip_or_host, port=15780):
        self.is_host = False
        self._hosting = False
        host, parsed_port = self.parse_host_port(ip_or_host, default_port=port)

        def worker():
            try:
                if not host:
                    raise ValueError("目標位址為空，請輸入有效的 IP 或隧道網址")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(8.0)
                s.connect((host, int(parsed_port)))
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                hs_raw = json.dumps({
                    "type": "WS_HANDSHAKE",
                    "protocol": "WS_MASTER_DUEL_V2",
                    "node_id": self.node_id,
                }) + "\n"
                s.sendall(hs_raw.encode("utf-8"))
                buf = ""
                ack_ok = False
                rest_buf = ""
                while "\n" not in buf and len(buf) < 4096:
                    chunk = s.recv(1024)
                    if not chunk:
                        break
                    buf += chunk.decode("utf-8", errors="replace")
                if "\n" in buf:
                    first_line, rest_buf = buf.split("\n", 1)
                    ack_msg = json.loads(first_line.strip())
                    if isinstance(ack_msg, dict) and ack_msg.get("type") == "WS_HANDSHAKE_ACK":
                        ack_ok = True
                if not ack_ok:
                    s.close()
                    raise ConnectionError("目標位址已連通，但對方並非等待中的 WS 對戰房間")
                s.settimeout(None)
                self.conn = s
                self.connected = True
                if self.on_msg:
                    self.on_msg({"type": "SYS_CONNECTED", "peer": f"{host}:{parsed_port}"})
                self._recv_loop(s, initial_buf=rest_buf)
            except Exception as e:
                if self.on_msg:
                    self.on_msg({"type": "SYS_ERROR", "error": str(e)})

        threading.Thread(target=worker, daemon=True).start()

    def _recv_loop(self, conn, initial_buf: str = ""):
        buf = initial_buf or ""
        while self.connected:
            try:
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
                data = conn.recv(16384)
                if not data:
                    break
                buf += data.decode("utf-8", errors="replace")
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
        self._hosting = False
        self.connected = False
        for s in (self.conn, self.sock):
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        self.conn = None
        self.sock = None
