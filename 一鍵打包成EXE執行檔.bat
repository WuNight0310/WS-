@echo off
chcp 65001 >nul
cd /d "%~dp0"
title WS 卡牌對戰模擬器 — 一鍵打包免安裝 EXE 工具 (強制掛載圖標＆清除快取)
echo ========================================================
echo   正在準備打包《Weiß Schwarz 卡牌對戰模擬器》免安裝版
echo ========================================================
echo.
echo [1/4] 檢查並安裝必要套件 (pyinstaller, pillow, pygame, requests)...
python -m pip install --upgrade pip pyinstaller pillow pygame requests
echo.

echo [2/4] 正在確認並產生 Windows 多尺寸圖標檔 (maple_icon.ico)...
python -c "import os; from PIL import Image; p='maple_icon.png' if os.path.exists('maple_icon.png') else ('maple_angel_icon.png' if os.path.exists('maple_angel_icon.png') else ''); im=Image.open(p).convert('RGBA') if p else None; im.save('maple_icon.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)]) if im else None; print('✔ 已由', p, '自動產生標準 maple_icon.ico！' if im else '使用現有 maple_icon.ico')"

echo [3/4] 正在清除舊版 PyInstaller 編譯快取並封裝 WS_CardBattle.exe ...
if exist "build" rmdir /s /q "build"
if exist "dist\WS_CardBattle" rmdir /s /q "dist\WS_CardBattle"
if exist "WS_CardBattle.spec" del /f /q "WS_CardBattle.spec"

python -m PyInstaller --noconfirm --clean --onedir --windowed --icon="%~dp0maple_icon.ico" --name "WS_CardBattle" --hidden-import=engine --hidden-import=network --hidden-import=PIL --hidden-import=pygame main.py
echo.

echo [4/4] 正在複製卡表 (sets)、卡圖快取 (ws_card_images)、音檔 (ws_audio) 與圖標到發佈資料夾...
if exist "sets" xcopy /E /I /Y "sets" "dist\WS_CardBattle\sets" >nul
if exist "ws_card_images" xcopy /E /I /Y "ws_card_images" "dist\WS_CardBattle\ws_card_images" >nul
if exist "ws_audio" xcopy /E /I /Y "ws_audio" "dist\WS_CardBattle\ws_audio" >nul
if exist "maple_icon.ico" copy /Y "maple_icon.ico" "dist\WS_CardBattle\maple_icon.ico" >nul
if exist "maple_icon.png" copy /Y "maple_icon.png" "dist\WS_CardBattle\maple_icon.png" >nul

REM 強制通知 Windows 檔案總管刷新 EXE 圖標快取（避免 Windows 記住舊版無圖標的 WS_CardBattle.exe）
ie4uinit.exe -show >nul 2>&1
ie4uinit.exe -ClearIconCache >nul 2>&1

echo.
echo ========================================================
echo   ✔ 打包與圖標寫入完成！（已同步刷新 Windows 圖標快取）
echo   請打開【dist\WS_CardBattle】確認 WS_CardBattle.exe 的梅普露圖標！
echo ========================================================
pause
