@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if not exist fakenews.jar call compilar.bat || exit /b 1
java -Dfile.encoding=UTF-8 -jar fakenews.jar %*
