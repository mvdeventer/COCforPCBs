@echo off
REM Quick launcher for create_report.py in DEBUG MODE
REM Automatically runs in virtual environment with detailed logging

echo ============================================================
echo COC REPORT GENERATOR - DEBUG MODE
echo ============================================================
echo Debug log will be saved to: coc_debug.log
echo ============================================================
echo.

python "%~dp0create_report.py" --debug

echo.
echo ============================================================
echo Debug session complete. Check coc_debug.log for details.
echo ============================================================
pause
