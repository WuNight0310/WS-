@echo off
chcp 65001 >nul
title WS 卡牌對戰模擬系統 — 一鍵上傳至 GitHub 工具
echo ========================================================
echo   一鍵將《Weiß Schwarz 卡牌對戰模擬系統》上傳至 GitHub
echo ========================================================
echo.
if not exist ".git" (
    git init
    git branch -M main
)
git add main.py engine.py network.py sets/ ws_card_images/ ws_audio/ *.bat README.md .gitignore
git commit -m "Update WS Master Duel FullScreen Card Battle System"
echo.
set /p REPO_URL="請貼上你在 GitHub 建立的空白倉庫網址 (例如 https://github.com/你的帳號/ws-card-battle.git)："
if not "%REPO_URL%"=="" (
    git remote remove origin 2>nul
    git remote add origin %REPO_URL%
    git push -u origin main
    echo.
    echo ✔ 已成功推送至 GitHub！
) else (
    echo 尚未輸入網址，已先完成本地 Git Commit。
)
pause
