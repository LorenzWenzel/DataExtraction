@echo off
REM Set the current directory without the 'Projekt' folder
for %%i in ("%cd%") do set currentDir=%%~dpi

REM Replace '\' with '/' for Docker compatibility
set LITHIREAPP_BASE=%currentDir:Projekt\=%
set LITHIREAPP_BASE=%LITHIREAPP_BASE:\=/%

REM Write out the base path
echo LITHIREAPP_BASE is set to: %LITHIREAPP_BASE%

REM Set the environment variable for Docker to pick up
set LITHIREAPP_BASE "%LITHIREAPP_BASE%"

REM Run docker-compose commands
docker-compose down
docker-compose up --build
