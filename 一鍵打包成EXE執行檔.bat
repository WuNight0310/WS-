@echo off
chcp 65001 >nul
cd /d "%~dp0"
title WS 卡牌對戰模擬器 — 一鍵打包免安裝 EXE 工具 (真實 Win32 DIB 圖標引擎)
echo ========================================================
echo   正在準備打包《Weiß Schwarz 卡牌對戰模擬器》免安裝版
echo ========================================================
echo.
echo [1/4] 檢查並安裝必要套件 (pyinstaller, pillow, pygame, requests)...
python -m pip install --upgrade pip pyinstaller pillow pygame requests
echo.

echo [2/4] 正在產生真實 Win32 DIB 格式圖標檔 (解決詳細資料 16x16 檢視無圖標問題)...
python win32_ico_builder.py

echo [3/4] 正在清除舊版 PyInstaller 快取並封裝 WS_CardBattle.exe ...
if exist "build" rmdir /s /q "build"
if exist "dist\WS_CardBattle" rmdir /s /q "dist\WS_CardBattle"
if exist "*.spec" del /f /q "*.spec"

python -m PyInstaller --noconfirm --clean --onedir --windowed -i "%~dp0maple_icon.ico" --name "WS_CardBattle" --hidden-import=engine --hidden-import=network --hidden-import=PIL --hidden-import=pygame main.py
echo.

echo [4/4] 正在複製卡表 (sets)、卡圖快取 (ws_card_images)、音檔 (ws_audio) 與圖標...
if exist "sets" xcopy /E /I /Y "sets" "dist\WS_CardBattle\sets" >nul
if exist "ws_card_images" xcopy /E /I /Y "ws_card_images" "dist\WS_CardBattle\ws_card_images" >nul
if exist "ws_audio" xcopy /E /I /Y "ws_audio" "dist\WS_CardBattle\ws_audio" >nul
if exist "maple_icon.ico" copy /Y "maple_icon.ico" "dist\WS_CardBattle\maple_icon.ico" >nul
if exist "maple_icon.png" copy /Y "maple_icon.png" "dist\WS_CardBattle\maple_icon.png" >nul

echo.
echo [刷新] 正在清除 Windows 檔案總管圖標快取並重啟 Explorer...
taskkill /f /im explorer.exe >nul 2>&1
del /f /s /q "%localappdata%\IconCache.db" >nul 2>&1
del /f /s /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*.db" >nul 2>&1
start explorer.exe

echo.
echo ========================================================
echo   ✔ 打包完成！現在無論是「詳細資料」小圖示或桌面大圖示皆可正常顯示！
echo ========================================================
explorer "%~dp0dist\WS_CardBattle"
pause
