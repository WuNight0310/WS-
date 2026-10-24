@echo off
chcp 65001 >nul
title WS 卡牌對戰模擬系統 — 一鍵打包免安裝 EXE 工具
echo ========================================================
echo   正在準備打包《Weiß Schwarz 卡牌對戰模擬系統》免安裝版
echo ========================================================
echo.
echo [1/3] 檢查並安裝必要套件 (pyinstaller, pillow, pygame, requests)...
python -m pip install --upgrade pip pyinstaller pillow pygame requests
echo.
echo [2/3] 正在將程式編譯為免安裝執行檔 WS_CardBattle.exe ...
python -m PyInstaller --noconfirm --onedir --windowed --name "WS_CardBattle" --hidden-import=engine --hidden-import=network --hidden-import=PIL --hidden-import=pygame main.py
echo.
echo [3/3] 正在複製卡表 (sets)、卡圖快取 (ws_card_images) 與音檔 (ws_audio) 到發佈資料夾...
if exist "sets" xcopy /E /I /Y "sets" "dist\WS_CardBattle\sets" >nul
if exist "ws_card_images" xcopy /E /I /Y "ws_card_images" "dist\WS_CardBattle\ws_card_images" >nul
if exist "ws_audio" xcopy /E /I /Y "ws_audio" "dist\WS_CardBattle\ws_audio" >nul
echo.
echo ========================================================
echo   打包完成！
echo   請將【dist\WS_CardBattle】整個資料夾壓縮成 .zip 傳給朋友，
echo   朋友解壓縮後直接雙擊裏面的【WS_CardBattle.exe】即可遊玩（無須安裝 Python）！
echo ========================================================
pause
