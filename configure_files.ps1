# Configure input files for COC report generation
# Opens GUI to select and save input file paths

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "COC REPORT GENERATOR - FILE CONFIGURATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Select the 6 input files (BOMs, Schematics, Assembly drawings)" -ForegroundColor Yellow
Write-Host "Configuration will be saved and remembered for future runs" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptPath\create_report.py" --configure

Write-Host ""
Read-Host "Press Enter to continue"
