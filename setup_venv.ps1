# Setup Virtual Environment for COC Report Generator
# Run this script to create and configure the Python virtual environment

Write-Host "=" * 60
Write-Host "COC Report Generator - Virtual Environment Setup"
Write-Host "=" * 60
Write-Host ""

# Check if .venv already exists
if (Test-Path ".venv") {
    Write-Host "[WARNING] Virtual environment already exists at .venv"
    $response = Read-Host "Do you want to recreate it? (y/N)"
    if ($response -ne "y") {
        Write-Host "Aborted."
        exit 0
    }
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force .venv
}

# Create virtual environment
Write-Host "[INFO] Creating virtual environment..."
python -m venv .venv

if (-not $?) {
    Write-Host "[ERROR] Failed to create virtual environment"
    Write-Host "Make sure Python is installed and available in PATH"
    exit 1
}

Write-Host "[OK] Virtual environment created"

# Activate virtual environment
Write-Host ""
Write-Host "[INFO] Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "[INFO] Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
Write-Host ""
Write-Host "[INFO] Installing dependencies from requirements.txt..."
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "[OK] Dependencies installed"
}
else {
    Write-Host "[WARNING] requirements.txt not found"
    Write-Host "Installing core dependencies manually..."
    pip install pandas openpyxl PyPDF2 python-docx PyMuPDF Pillow
}

# Summary
Write-Host ""
Write-Host "=" * 60
Write-Host "[SUCCESS] SETUP COMPLETE"
Write-Host "=" * 60
Write-Host ""
Write-Host "Virtual environment is ready at: .venv"
Write-Host ""
Write-Host "To activate the virtual environment:"
Write-Host "  PowerShell: .\.venv\Scripts\Activate.ps1"
Write-Host "  CMD:        .venv\Scripts\activate.bat"
Write-Host ""
Write-Host "To run the COC Report Generator:"
Write-Host "  python create_report.py"
Write-Host ""
Write-Host "VS Code will automatically use this virtual environment."
Write-Host ""
