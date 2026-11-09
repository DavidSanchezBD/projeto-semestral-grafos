@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
call compilar.bat || exit /b 1
cd test
javac -encoding UTF-8 -cp ..\out -d ..\out br\maua\fakenews\*.java || (cd .. & exit /b 1)
cd ..
java -Dfile.encoding=UTF-8 -cp out br.maua.fakenews.TestesAlgoritmos
