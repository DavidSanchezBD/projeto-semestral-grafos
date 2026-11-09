@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
where javac >nul 2>nul || (echo [ERRO] javac nao encontrado. Instale o JDK 21: winget install EclipseAdoptium.Temurin.21.JDK & exit /b 1)
if exist out rmdir /s /q out
mkdir out
cd src
javac -encoding UTF-8 -d ..\out br\maua\fakenews\*.java br\maua\fakenews\modelo\*.java br\maua\fakenews\algoritmos\*.java br\maua\fakenews\dados\*.java br\maua\fakenews\web\*.java || (cd .. & exit /b 1)
cd ..
jar --create --file fakenews.jar --main-class br.maua.fakenews.App -C out . || exit /b 1
echo Compilado com sucesso: fakenews.jar
