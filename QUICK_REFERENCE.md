# Quick Reference - COC Report Generator

## Run COC Report Generator

```powershell
python create_report.py
```

Automatically runs in virtual environment (venv) and generates COC report.

### Configure Input Files

```powershell
.\configure_files.bat
# or
python create_report.py --configure
```

Opens GUI to select the 6 input files (2 BOMs, 2 Schematics, 2 Assembly drawings).
Configuration is saved to `input_files_config.json` and remembered between runs.

### Debug Mode

```powershell
.\create_report_debug.bat
# or
python create_report.py --debug
```

Runs with detailed logging saved to `coc_debug.log`.

## Build Executables

### Build EXE Only

```powershell
python build_exe.py
```

Builds standalone EXE using PyInstaller (automatically uses venv).

### Build Complete Installer

```powershell
python build_installer.py
```

Builds EXE + Windows installer with Inno Setup (automatically uses venv).

## Version Management

### Check Version Status

```powershell
python check_versions.py
```

Shows current versions across all files and whether they're in sync.

### Update Version Files

```powershell
python update_versions.py
```

Syncs `version_info.txt` and `installer.iss` to match current git tag.

## Make a Release

### Automatic (Recommended)

```powershell
python scripts/release.py --auto
```

Automatically detects version bump from commit messages:
- `fix:` commits → patch version (1.0.0 → 1.0.1)
- `feat:` commits → minor version (1.0.0 → 1.1.0)
- `BREAKING CHANGE:` → major version (1.0.0 → 2.0.0)

### Force Specific Version Bump

```powershell
# Force patch (1.0.0 → 1.0.1)
python scripts/release.py --auto --bump patch

# Force minor (1.0.0 → 1.1.0)
python scripts/release.py --auto --bump minor

# Force major (1.0.0 → 2.0.0)
python scripts/release.py --auto --bump major
```

## Regular Commits

```powershell
git add .
git commit -m "fix: your fix description"
```

The pre-commit hook automatically updates version files before committing.

## What Happens When

### On Commit

1. Pre-commit hook runs
2. Version files updated to match latest tag
3. Files staged and commit proceeds

### On Release

1. Next version determined
2. Version files updated
3. Changes committed
4. Git tag created
5. Pushed to GitHub
6. GitHub release created

### On CI/CD Build

1. Tag triggers workflow
2. Version extracted from tag
3. Files updated (redundant, for safety)
4. EXE built
5. Installer created
6. Artifacts uploaded to release

## File Overview

| File | Purpose | Auto-Updated By |
|------|---------|-----------------|
| `version_info.txt` | Windows EXE metadata | Pre-commit hook, Release script, GitHub Actions |
| `installer.iss` | Inno Setup installer | Pre-commit hook, Release script, GitHub Actions |
| `coc_report.spec` | PyInstaller config | Self-updating (reads git tags) |
| Git tags | Source of truth | Release script |

## Conventional Commits

Use these prefixes for automatic version bump detection:

- `fix:` Bug fixes → patch version
- `feat:` New features → minor version
- `BREAKING CHANGE:` Breaking changes → major version
- `docs:` Documentation only → no version bump
- `chore:` Maintenance → no version bump

## Example Workflow

```powershell
# 1. Make changes
notepad generate_coc_report.py

# 2. Check current version status
python check_versions.py

# 3. Commit changes (pre-commit hook updates versions)
git add .
git commit -m "feat: add new BOM parsing feature"

# 4. Create release (auto-detects minor bump from 'feat:')
python scripts/release.py --auto

# Output:
# 📌 Current version: v1.0.2
# 🔼 Next version: v1.1.0
# ✅ Version files updated
# ✅ Committed
# ✅ Tagged v1.1.0
# ✅ Pushed to GitHub
# ✅ Release created
```

## Troubleshooting

### Versions out of sync?

```powershell
python update_versions.py
```

### Pre-commit hook not running?

```powershell
# Check if hook exists
Test-Path .git/hooks/pre-commit

# If missing, it should have been created
# Verify Python is in your PATH
```

### Wrong version in build?

```powershell
# Check git tags
git tag -l

# Ensure latest tag is correct format: vX.Y.Z
# Update files to match
python update_versions.py
```

## Documentation

- `VERSION_MANAGEMENT.md` - Complete guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `README.md` - Contributing section

## Summary

✅ Version files auto-update on every commit (pre-commit hook)
✅ Release script handles complete release workflow
✅ GitHub Actions builds and publishes automatically
✅ Manual sync available with `update_versions.py`
✅ Version status check with `check_versions.py`

**You never need to manually edit version numbers!**
