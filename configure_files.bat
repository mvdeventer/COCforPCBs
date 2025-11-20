@echo off
REM Configure input files for COC report generation
REM Opens GUI to select and save input file paths

echo ============================================================
echo COC REPORT GENERATOR - FILE CONFIGURATION
echo ============================================================
echo Select the 6 input files (BOMs, Schematics, Assembly drawings)
echo Configuration will be saved and remembered for future runs
echo ============================================================
echo.

python "%~dp0create_report.py" --configure

echo.
pause
