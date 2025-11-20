# Virtual Environment Integration - Summary

## What Was Implemented

All execution scripts now automatically ensure they run in the virtual environment (venv).

## Updated/Created Files

### 1. `create_report.py` - Enhanced COC Report Generator

**Changes:**
- ✅ Detects if running in virtual environment
- ✅ Automatically switches to venv if available
- ✅ Prompts user if venv not found
- ✅ Shows venv status on execution

**Usage:**
```powershell
python create_report.py
```

**Behavior:**
- If venv exists: Automatically restarts in venv
- If no venv: Prompts user to set up or continue anyway
- Shows clear status messages

### 2. `build_exe.py` - NEW: Build EXE Script

**Purpose:** Build standalone EXE using PyInstaller with venv

**Features:**
- ✅ Requires virtual environment (fails if not found)
- ✅ Auto-installs PyInstaller if missing
- ✅ Runs `pyinstaller coc_report.spec --clean --noconfirm`
- ✅ Shows build progress and results
- ✅ Displays EXE size on completion

**Usage:**
```powershell
python build_exe.py
```

**Output:**
- Builds `dist/COC_Report_Generator.exe`
- Shows file size in MB
- Reports success/failure clearly

### 3. `build_installer.py` - NEW: Build Complete Installer

**Purpose:** Build EXE + Windows installer in one command

**Features:**
- ✅ Requires virtual environment
- ✅ Step 1: Builds EXE using `build_exe.py`
- ✅ Step 2: Creates installer using Inno Setup
- ✅ Auto-detects Inno Setup installation
- ✅ Complete automated build process

**Usage:**
```powershell
python build_installer.py
```

**Output:**
- Builds `dist/COC_Report_Generator.exe`
- Creates `dist/installer/COC_Report_Generator_Setup_X.X.X.exe`
- Shows both file sizes
- Two-step progress display

## How It Works

### Virtual Environment Detection

All scripts use the same detection method:

```python
def is_venv_active():
    """Check if we're running in a virtual environment"""
    return hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
```

### Auto-Restart Mechanism

If not in venv, scripts find the venv Python executable and restart themselves:

```python
def ensure_venv():
    """Ensure we're running in the virtual environment"""
    if is_venv_active():
        return True

    venv_python = get_venv_python()  # .venv/Scripts/python.exe

    if venv_python:
        # Re-run this script using venv Python
        subprocess.run([str(venv_python), __file__])
        sys.exit()
```

### Build Scripts Behavior

**`build_exe.py`:**
```
1. Check if in venv → if not, restart in venv
2. Check if PyInstaller installed → if not, install it
3. Run PyInstaller with coc_report.spec
4. Report results
```

**`build_installer.py`:**
```
1. Check if in venv → if not, restart in venv
2. Run build_exe.py (which builds the EXE)
3. Find Inno Setup compiler
4. Run ISCC.exe with installer.iss
5. Report results
```

## Quick Reference Commands

### Set Up Virtual Environment

```powershell
# Option 1: Use PowerShell script (recommended)
powershell -ExecutionPolicy Bypass -File setup_venv.ps1

# Option 2: Manual setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run COC Report Generator

```powershell
# Automatically uses venv if available
python create_report.py
```

### Build EXE Only

```powershell
# Requires venv, auto-installs PyInstaller
python build_exe.py
```

### Build Complete Installer

```powershell
# Requires venv and Inno Setup
python build_installer.py
```

### Check Version Status

```powershell
# Check if version files are in sync
python check_versions.py
```

### Update Version Files

```powershell
# Sync version files to git tag
python update_versions.py
```

## Example Workflows

### First Time Setup

```powershell
# 1. Clone repository
git clone https://github.com/Koolkop1@/COCforPCBs.git
cd COCforPCBs

# 2. Set up virtual environment
powershell -ExecutionPolicy Bypass -File setup_venv.ps1

# 3. Generate report
python create_report.py
```

### Regular Use

```powershell
# Just run the script - venv is automatic
python create_report.py
```

### Building Release

```powershell
# Build installer (includes EXE build)
python build_installer.py

# Or just build EXE
python build_exe.py
```

### Development Workflow

```powershell
# 1. Make changes to code
notepad generate_coc_report.py

# 2. Test changes
python create_report.py

# 3. Build EXE to test
python build_exe.py

# 4. If satisfied, commit and release
git add .
git commit -m "feat: new feature"
python scripts/release.py --auto
```

## Error Handling

### No Virtual Environment

**Error:**
```
WARNING: Virtual environment not found at .venv

To set up the virtual environment, run:
  powershell -ExecutionPolicy Bypass -File setup_venv.ps1
```

**Solution:**
```powershell
powershell -ExecutionPolicy Bypass -File setup_venv.ps1
```

### Missing PyInstaller

**Automatic Fix:** `build_exe.py` will install it automatically

**Manual Fix:**
```powershell
.venv\Scripts\Activate.ps1
pip install pyinstaller
```

### Missing Inno Setup

**Error:**
```
[ERROR] Inno Setup not found
Install Inno Setup from: https://jrsoftware.org/isdl.php
```

**Solution:**
```powershell
# Option 1: Download from website
# https://jrsoftware.org/isdl.php

# Option 2: Install via Chocolatey
choco install innosetup
```

## File Structure

```
COCforPCBs/
├── create_report.py          # Main launcher (auto-venv)
├── build_exe.py              # Build EXE (auto-venv)
├── build_installer.py        # Build installer (auto-venv)
├── update_versions.py        # Update version files
├── check_versions.py         # Check version status
│
├── .venv/                    # Virtual environment
│   └── Scripts/
│       └── python.exe        # Venv Python
│
├── scripts/
│   ├── release.py            # GitHub release automation
│   └── update_version_files.py  # Version sync script
│
├── coc_report.spec           # PyInstaller config
├── installer.iss             # Inno Setup config
├── version_info.txt          # Windows EXE metadata
│
└── dist/                     # Build output
    ├── COC_Report_Generator.exe
    └── installer/
        └── COC_Report_Generator_Setup_X.X.X.exe
```

## Benefits

✅ **No manual venv activation needed** - Scripts handle it automatically
✅ **Consistent environment** - All scripts use same Python/packages
✅ **User-friendly** - Clear prompts and error messages
✅ **Build automation** - One command builds everything
✅ **ASCII-only output** - No Unicode encoding issues in Windows terminal

## Integration with Existing System

These scripts work seamlessly with the existing version management system:

- **Pre-commit hook:** Updates version files automatically
- **Release script:** `python scripts/release.py --auto`
- **GitHub Actions:** Builds on tag push
- **Version sync:** `python update_versions.py`

## Summary

All execution scripts now:
1. ✅ Auto-detect virtual environment
2. ✅ Auto-switch to venv if available
3. ✅ Prompt user if venv missing
4. ✅ Show clear status messages
5. ✅ Use ASCII-only output (no Unicode issues)

**Result:** No manual venv activation required - just run the scripts!

## Quick Command Reference

| Command | Purpose | Requires Venv |
|---------|---------|---------------|
| `python create_report.py` | Generate COC report | Recommended |
| `python build_exe.py` | Build EXE only | Required |
| `python build_installer.py` | Build EXE + installer | Required |
| `python check_versions.py` | Check version status | No |
| `python update_versions.py` | Sync version files | No |
| `python scripts/release.py --auto` | Create GitHub release | Recommended |

All scripts handle venv automatically - just run them! 🎉
