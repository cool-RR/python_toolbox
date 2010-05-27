@echo off

if "%1" == "" goto help
if "%1" == "help" goto help
if "%1" == "/h" goto help
if "%1" == "/?" goto help

if "%1" == "--help" (
    :help
	echo.This is a script for creating a skeleton for a garlicsim simpack. Use this when
    echo.you want to make a new simpack to have the basic folders and files created for
    echo.you.
    echo.
    echo.    Usage: start_simpack.bat my_simpack_name
    echo.
    echo.The simpack will be created in the current path, in a directory with the name
    echo.of the simpack.
    goto end
)

xcopy "%~dp0\simpack_template\simpack_name" %1 /E/Q/K/I
del /S/Q "%1\*.pyc"
del /S/Q "%1\*.pyo"

echo.-----------
echo.%1 simpack created successfully! Explore the %1 folder and start
echo.filling in the contents of your new simpack.

:end
@echo on