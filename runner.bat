@echo off
title Gig Scraper

:InstallPackages
color 0E
echo.
echo -------------------------------------------------------------------------------
echo                        Gig Scraper - Installation
echo -------------------------------------------------------------------------------
echo Installing required Python packages, please wait...
pip install -r requirements.txt >nul
if %ERRORLEVEL% neq 0 (
    color 0C
    echo Error during installation. Please check if 'pip' is installed.
    pause
    exit /b
)
echo Installation completed.
echo.

:RunScript
color 0B
echo -------------------------------------------------------------------------------
echo                        Running the Python Script
echo -------------------------------------------------------------------------------
python scraper.py
if %ERRORLEVEL% neq 0 (
    color 0C
    echo Error running script. Please check the Python script for errors.
    pause
    exit /b
)
echo.
echo Script execution finished.
echo -------------------------------------------------------------------------------

:End
color 0A
pause
exit /b
