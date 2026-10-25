@echo off
chcp 65001 >nul
cd /d "%~dp0"
title WS 卡牌對戰模擬器 — 一鍵同步更新至 GitHub
echo ========================================================
echo   一鍵將《Weiß Schwarz 卡牌對戰模擬器》同步更新至 GitHub
echo ========================================================
echo.

if not exist ".git" (
    git init
    git branch -M main
)

REM 自動檢查是否已綁定 GitHub 遠端倉庫，若無則自動綁定 https://github.com/WuNight0310/WS-.git
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    git remote add origin https://github.com/WuNight0310/WS-.git
    echo [設定] 已自動綁定遠端倉庫：https://github.com/WuNight0310/WS-.git
)

REM 修正中文檔名在 Git 顯示亂碼的問題，並清除誤建的 artifacts 暫存資料夾
git config core.quotepath false
if exist "artifacts" rmdir /s /q "artifacts"

echo [1/3] 正在掃描所有新增與修改的檔案 (git add -A)...
git add -A

echo [2/3] 正在建立本地版本紀錄 (git commit)...
git commit -m "Auto update WS Master Duel Simulator (%date% %time%)"

echo [3/3] 正在推送更新至 GitHub (git push)...
git push -u origin main

echo.
echo ========================================================
echo   ✔ 已全自動完成 GitHub 同步更新！（同時觸發雲端 APK 自動編譯）
echo ========================================================
pause
