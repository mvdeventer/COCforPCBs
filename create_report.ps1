# Quick launcher for create_report.py
# Automatically runs in virtual environment

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptPath\create_report.py" $args
