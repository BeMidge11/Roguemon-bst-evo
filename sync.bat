@echo off
set GIT_EXE="C:\Users\benmi\AppData\Local\GitHubDesktop\app-3.5.8\resources\app\git\cmd\git.exe"

echo [1/3] Staging changes...
%GIT_EXE% add .

echo [2/3] Committing changes...
%GIT_EXE% commit -m "Restore and optimize BST/10 Evolution Simulator UI/Data"

echo [3/3] Pushing to GitHub...
%GIT_EXE% push -u origin main

echo.
echo Sync Complete!
pause
