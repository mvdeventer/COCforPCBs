# Quick launcher for create_report.py in DEBUG MODE
# Automatically runs in virtual environment with detailed logging

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "COC REPORT GENERATOR - DEBUG MODE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Debug log will be saved to: coc_debug.log" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptPath\create_report.py" --debug

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Debug session complete. Check coc_debug.log for details." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
