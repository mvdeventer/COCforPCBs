@echo off
setlocal enabledelayedexpansion

REM COC Report Generator - Comprehensive Release Script Wrapper
REM Forwards all arguments to the Python release script

REM Capture start time
set START_TIME=%TIME%

if "%1"=="--help" goto :help
if "%1"=="-h" goto :help
if "%1"=="/?" goto :help
if "%1"=="" goto :help

REM Run the Python release script with all arguments
python scripts\release.py %*
set EXITCODE=%ERRORLEVEL%

REM Calculate elapsed time
set END_TIME=%TIME%
call :calculate_elapsed_time "%START_TIME%" "%END_TIME%"

if %EXITCODE% EQU 0 (
    echo.
    echo Release operation completed successfully!
    echo Total execution time: !ELAPSED_TIME!
) else (
    echo.
    echo Release operation failed!
    echo Total execution time: !ELAPSED_TIME!
    exit /b 1
)

endlocal
exit /b %EXITCODE%

:calculate_elapsed_time
REM Convert start and end times to seconds
set start=%~1
set end=%~2

REM Extract hours, minutes, seconds
for /f "tokens=1-3 delims=:,." %%a in ("%start%") do (
    set /a start_h=%%a
    set /a start_m=%%b
    set /a start_s=%%c
)

for /f "tokens=1-3 delims=:,." %%a in ("%end%") do (
    set /a end_h=%%a
    set /a end_m=%%b
    set /a end_s=%%c
)

REM Calculate total seconds
set /a start_total=start_h*3600 + start_m*60 + start_s
set /a end_total=end_h*3600 + end_m*60 + end_s

REM Handle day boundary (if end time is before start time)
if %end_total% LSS %start_total% set /a end_total+=86400

REM Calculate difference
set /a diff=end_total - start_total

REM Convert back to minutes and seconds
set /a minutes=diff/60
set /a seconds=diff%%60

if %minutes% GTR 0 (
    set ELAPSED_TIME=%minutes% min %seconds% sec
) else (
    set ELAPSED_TIME=%seconds% sec
)

exit /b 0

:help
echo.
echo ============================================================
echo COC Report Generator Release Script
echo ============================================================
echo.
echo Usage:
echo   release.bat [options]
echo.
echo Options:
echo   --patch         Force patch increment (x.x.X)
echo   --minor         Force minor increment (x.X.0)
echo   --major         Force major increment (X.0.0)
echo   --version 1.1.0 Set specific version
echo   --dry-run       Preview without changes
echo   --skip-build    Skip building executable/installer
echo   --skip-push     Skip pushing to GitHub
echo   --build-only    Build exe/installer only (no version bump or git ops)
echo   --exe-only      Build only executable (no installer, no git ops)
echo   --installer-only Build only installer (assumes exe exists, no git ops)
echo   --push-only     Commit and push current changes only (no version bump or build)
echo.
echo Examples:
echo   release.bat                 # Auto-increment based on commits
echo   release.bat --dry-run       # Preview what will happen
echo   release.bat --patch         # Quick patch release
echo   release.bat --skip-build    # Version bump and git only
echo   release.bat --version 1.1.0 # Set specific version
echo   release.bat --build-only    # Just rebuild current version
echo   release.bat --exe-only      # Build executable only
echo   release.bat --installer-only # Build installer only
echo   release.bat --push-only     # Commit and push changes (no build/version bump)
echo.
echo Note: Script fetches latest version from GitHub automatically
echo.
python scripts\release.py %*

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Release operation completed successfully!
) else (
    echo.
    echo Release operation failed!
    exit /b 1
)

endlocal
