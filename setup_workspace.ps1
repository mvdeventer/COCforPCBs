# Workspace Setup - Run this to set up the project
Write-Host "Running workspace setup..."
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptPath\scripts\workspace_setup.py"
