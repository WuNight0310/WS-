@echo off
chcp 65001 >nul
cd /d "%~dp0"
title WS 卡牌對戰模擬器 — 一鍵同步更新至 GitHub
echo ========================================================
echo   一鍵將《Weiß Schwarz 原版 Python 主程式》同步更新至 GitHub
echo ========================================================
echo.

if not exist ".git" git init
if not exist ".git" git branch -M main

git remote get-url origin >nul 2>&1
if errorlevel 1 git remote add origin https://github.com/WuNight0310/WS-.git

git config core.quotepath false
if exist "artifacts" rmdir /s /q "artifacts"
if exist "android_apk_builder" rmdir /s /q "android_apk_builder"
if exist "ws_master_duel_web_mobile.html" del /f /q "ws_master_duel_web_mobile.html"
git rm -rf --ignore-unmatch android_apk_builder ws_master_duel_web_mobile.html >nul 2>&1

echo [1/3] 正在掃描所有新增與修改的檔案 (git add -A)...
git add -A

echo [2/3] 正在建立本地版本紀錄 (git commit)...
git commit -m "Restore 100pct Pure Python WS Master Duel APK"

echo [3/3] 正在推送更新至 GitHub (git push)...
git push -u origin main --force

echo.
echo ========================================================
echo   ✔ 已全自動完成 GitHub 同步更新！（請至 Actions 下載純 Python 版 APK）
echo ========================================================
pause
