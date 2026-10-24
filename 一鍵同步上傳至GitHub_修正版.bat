@echo off
setlocal EnableExtensions
title WS Card Battle Simulator - GitHub Sync

echo ========================================================
echo   WS Card Battle Simulator - GitHub Sync
echo ========================================================
echo.

where git >nul 2>nul
if errorlevel 1 goto no_git

if not exist "main.py" goto wrong_folder

if not exist ".git" (
    echo [INFO] Initializing local Git repository...
    git init
    if errorlevel 1 goto failed
)

git branch -M main
if errorlevel 1 goto failed

echo.
echo [IMPORTANT] Review the files below before uploading.
echo Make sure .gitignore excludes passwords, API keys, and private files.
echo.
git status --short
echo.
choice /M "Continue and upload these changes"
if errorlevel 2 goto cancelled

git add -A
if errorlevel 1 goto failed

git diff --cached --quiet
if not errorlevel 1 goto no_changes

echo.
set "COMMIT_MSG="
set /p "COMMIT_MSG=Commit message (press Enter for default): "
if not defined COMMIT_MSG set "COMMIT_MSG=Sync project updates"
git commit -m "%COMMIT_MSG%"
if errorlevel 1 goto failed

goto check_remote

:no_changes
echo.
echo [INFO] No new changes to commit.
goto check_remote

:check_remote
git remote get-url origin >nul 2>nul
if not errorlevel 1 goto show_remote

echo.
echo Enter your GitHub repository URL, for example:
echo https://github.com/WuNight0310/WS-.git
set "REPO_URL="
set /p "REPO_URL=Repository URL: "
if not defined REPO_URL goto missing_url
git remote add origin "%REPO_URL%"
if errorlevel 1 goto failed
goto push

:show_remote
echo.
echo [INFO] Using the configured GitHub remote:
git remote get-url origin
goto push

:push
echo.
echo [INFO] Pushing branch main to GitHub...
git push -u origin main
if errorlevel 1 goto push_failed

echo.
echo [SUCCESS] Push completed successfully.
goto finish

:no_git
echo [ERROR] Git was not found. Install Git for Windows first:
echo https://git-scm.com/download/win
goto failed

:wrong_folder
echo [ERROR] main.py was not found in the current folder.
echo Put this BAT file in the project root folder next to main.py.
goto failed

:missing_url
echo [ERROR] No repository URL was entered.
goto failed

:push_failed
echo.
echo [ERROR] Push failed. Read the Git error message above.
echo Check the repository URL, network connection, and GitHub permissions.
goto failed

:cancelled
echo.
echo Cancelled. No upload was performed.
goto finish

:failed
echo.
echo Operation did not complete. Review the messages above.
goto finish

:finish
echo.
pause
endlocal
