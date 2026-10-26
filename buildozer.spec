[app]
title = WS Master Duel
package.name = wsmasterduel
package.domain = org.ws
source.dir = .
source.include_exts = py,png,jpg,webp,json,wav,ico,ttf,ttc
source.exclude_dirs = tests,bin,venv,.git,.github,__pycache__,android_apk_builder,artifacts
version = 2.0.0

requirements = hostpython3==3.11.6,python3==3.11.6,kivy==2.3.0,pillow,urllib3,certifi,idna,charset-normalizer,requests

icon.filename = %(source.dir)s/maple_icon.png
presplash.filename = %(source.dir)s/maple_icon.png
presplash.color = #0d111a

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 0
