# Version File Management

This document explains how version numbers are managed across the COC Report Generator project.

## Overview

Version numbers must be consistent across multiple files:
- `version_info.txt` - Windows EXE metadata
- `installer.iss` - Inno Setup installer configuration
- `coc_report.spec` - PyInstaller build configuration
- Git tags - Source control version tags

## Automatic Version Updates

### 1. Pre-Commit Hook

A git pre-commit hook automatically updates version files before each commit:

**Location:** `.git/hooks/pre-commit`

**What it does:**
- Runs `scripts/update_version_files.py`
- Updates `version_info.txt` with current git tag version
- Updates `installer.iss` with current git tag version
- Stages the updated files for commit

**Trigger:** Automatically runs on every `git commit`

### 2. Release Script Integration

The `scripts/release.py` script includes automatic version updating:

**Command:** `python scripts/release.py --auto`

**What it does:**
1. Determines next version (from commits or specified bump type)
2. Updates version files via `update_version_files.py`
3. Commits all changes including updated version files
4. Creates git tag
5. Pushes to GitHub
6. Creates GitHub release

### 3. GitHub Actions CI/CD

The `.github/workflows/release.yml` workflow updates versions during builds:

**Trigger:** Push tag `v*.*.*` or manual workflow dispatch

**What it does:**
1. Extracts version from git tag
2. Updates `version_info.txt` with PowerShell regex
3. Updates `installer.iss` with PowerShell regex
4. Builds EXE with PyInstaller
5. Creates installer with Inno Setup
6. Creates GitHub release with artifacts

## Manual Version Updates

### Quick Update

Run the standalone script from the project root:

```powershell
python update_versions.py
```

This will:
- Read the current git tag version
- Update `version_info.txt`
- Update `installer.iss`
- Display confirmation messages

### Using the Version Update Script Directly

```powershell
python scripts/update_version_files.py
```

Same functionality as `update_versions.py` but runs from the scripts folder.

## Version File Details

### version_info.txt

Windows executable metadata file used by PyInstaller.

**Fields updated:**
- `filevers=(major, minor, patch, 0)` - Numeric version tuple
- `prodvers=(major, minor, patch, 0)` - Product version tuple
- `u'FileVersion', u'X.X.X'` - File version string
- `u'ProductVersion', u'X.X.X'` - Product version string

**Example:**
```python
filevers=(1, 0, 3, 0)
prodvers=(1, 0, 3, 0)
# ...
u'FileVersion', u'1.0.3'
u'ProductVersion', u'1.0.3'
```

### installer.iss

Inno Setup installer configuration.

**Field updated:**
- `#define AppVersion "X.X.X"` - Version string for installer

**Example:**
```inno
#define AppVersion "1.0.3"
```

### coc_report.spec

PyInstaller specification file.

**Auto-detection:** This file automatically detects the version from git tags at build time:

```python
version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'],
                                  text=True).strip()
version = version.lstrip('v')  # Remove 'v' prefix
```

**No manual updates needed!**

## Workflow Examples

### Example 1: Making a Bug Fix Release

```powershell
# Make your code changes
# Commit with conventional commit message
git add .
git commit -m "fix: correct BOM parsing issue"

# Pre-commit hook automatically updates version files
# Release script auto-detects it's a patch version
python scripts/release.py --auto

# Result: Versions updated, tagged as v1.0.3, released to GitHub
```

### Example 2: Manual Version Update Before Commit

```powershell
# Update version files to match current tag
python update_versions.py

# Check what was updated
git status

# Stage and commit
git add version_info.txt installer.iss
git commit -m "chore: update version files"
```

### Example 3: Forcing a Major Version Bump

```powershell
# Your commits don't indicate breaking changes but you want v2.0.0
python scripts/release.py --auto --bump major

# Result: Version bumped to v2.0.0, all files updated
```

## Troubleshooting

### Version Files Out of Sync

If version files don't match the git tag:

```powershell
# Reset to current tag version
python update_versions.py

# Verify
git status
git diff version_info.txt
git diff installer.iss
```

### Pre-Commit Hook Not Running

Check if the hook is executable and in the right location:

```powershell
# Verify hook exists
Test-Path .git/hooks/pre-commit

# Re-create hook if missing
Copy-Item .git/hooks/pre-commit.sample .git/hooks/pre-commit
# Then edit to run update_version_files.py
```

### Build Using Wrong Version

The `coc_report.spec` gets version from git tags. Ensure you have proper tags:

```powershell
# List tags
git tag -l

# Create a tag if missing
git tag -a v1.0.3 -m "Version 1.0.3"
git push --tags
```

## Version Number Format

This project uses **Semantic Versioning** (semver): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Git tag format:** `vMAJOR.MINOR.PATCH` (e.g., `v1.0.3`)

**File format:** `MAJOR.MINOR.PATCH` (e.g., `1.0.3`)

## Best Practices

1. **Always use the release script** for version bumps: `python scripts/release.py --auto`
2. **Use conventional commits** for auto-detection:
   - `fix:` → patch version (1.0.0 → 1.0.1)
   - `feat:` → minor version (1.0.0 → 1.1.0)
   - `BREAKING CHANGE:` → major version (1.0.0 → 2.0.0)
3. **Let the pre-commit hook work** - it keeps files in sync automatically
4. **Don't manually edit version numbers** unless absolutely necessary
5. **Run `update_versions.py` after creating tags manually** to sync files

## Integration with Build Process

```
┌─────────────────────────────────────────────────────────────┐
│                    Version Update Flow                       │
└─────────────────────────────────────────────────────────────┘

 1. Code Changes
    ↓
 2. git commit (triggers pre-commit hook)
    ↓
 3. Pre-commit hook → update_version_files.py
    ↓
 4. Version files updated (version_info.txt, installer.iss)
    ↓
 5. Files staged and committed
    ↓
 6. Release script creates tag → git push
    ↓
 7. GitHub Actions triggered on tag push
    ↓
 8. GitHub Actions updates versions (redundant, for safety)
    ↓
 9. Build EXE (coc_report.spec reads git tag)
    ↓
10. Build Installer (uses updated installer.iss)
    ↓
11. Create GitHub Release with artifacts
```

## Summary

- **Auto-update on commit:** Pre-commit hook keeps versions in sync
- **Auto-update on release:** Release script updates before tagging
- **Auto-update on CI/CD:** GitHub Actions ensures consistency
- **Manual override:** `update_versions.py` for manual synchronization
- **Spec file:** Self-updating via git commands

All version management is now automated - just commit and release!
