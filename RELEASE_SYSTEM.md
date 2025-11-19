# COC Report Generator - Release System

## Overview

Complete automated release system with GitHub Actions CI/CD, local builds, and intelligent version management.

## Quick Start

### Automated Release (Recommended)

```powershell
# Commit your changes
git add .
git commit -m "feat: add new feature"

# Run automated release
python scripts/release.py --auto

# GitHub Actions will automatically:
# - Build Windows EXE
# - Create installer
# - Generate release notes
# - Publish to GitHub Releases
```

### Local Build

```powershell
# Build EXE and installer locally
python scripts/build_local.py

# Output: dist/COC_Report_Generator_{version}/
```

## File Structure

```
COCforPCBs/
├── generate_coc_report.py          # Main application
├── coc_report.spec                  # PyInstaller build config
├── version_info.txt                 # Windows EXE metadata
├── installer.iss                    # Inno Setup installer script
├── requirements.txt                 # Python dependencies
├── CHANGELOG.md                     # Version history
│
├── scripts/
│   ├── release.py                   # GitHub release automation
│   ├── build_local.py               # Local EXE builder
│   └── README.md                    # Scripts documentation
│
├── .github/
│   └── workflows/
│       └── release.yml              # GitHub Actions CI/CD
│
└── dist/                            # Build output (generated)
    ├── COC_Report_Generator.exe
    └── installer/
        └── COC_Report_Generator_Setup_{version}.exe
```

## Version Management

### Semantic Versioning

- **Major** (x.0.0): Breaking changes
- **Minor** (0.x.0): New features
- **Patch** (0.0.x): Bug fixes

### Automatic Detection

The release system analyzes commit messages:

| Commit Message | Version Bump |
|---------------|--------------|
| `feat: add feature` | Minor (1.0.0 → 1.1.0) |
| `fix: bug fix` | Patch (1.0.0 → 1.0.1) |
| `BREAKING CHANGE: ...` | Major (1.0.0 → 2.0.0) |

### Manual Override

```powershell
# Specify bump type
python scripts/release.py --auto --bump major
python scripts/release.py --auto --bump minor
python scripts/release.py --auto --bump patch
```

## Release Commands

### Option 1: Fully Automated (Zero Prompts)

```powershell
python scripts/release.py --auto
```

- Auto-detects version from GitHub API
- Auto-determines bump type from commits
- Auto-generates changelog from git log
- Auto-commits and pushes
- Triggers GitHub Actions build

### Option 2: Manual Control

```powershell
python scripts/release.py
```

- Interactive version selection
- Manual changelog entry
- Confirmation prompts

### Option 3: Local Build Only

```powershell
python scripts/build_local.py
```

- Builds EXE locally
- Creates installer (if Inno Setup installed)
- No GitHub operations

## GitHub Actions Workflow

**Trigger**: Push tag matching `v*.*.*`

**Process**:
1. ✅ Checkout code
2. ✅ Setup Python 3.12
3. ✅ Install dependencies
4. ✅ Update version files
5. ✅ Build EXE with PyInstaller
6. ✅ Build installer with Inno Setup
7. ✅ Generate SHA256 checksums
8. ✅ Auto-generate release notes
9. ✅ Create GitHub Release
10. ✅ Upload EXE, installer, checksums

**Artifacts**:
- `COC_Report_Generator.exe` (standalone)
- `COC_Report_Generator_Setup_{version}.exe` (installer)
- `checksums.txt` (SHA256 hashes)

## Requirements

### Python Dependencies

```bash
pip install -r requirements.txt
```

- pandas>=2.1.0
- openpyxl>=3.1.0
- PyPDF2>=3.0.0
- python-docx>=1.0.0
- PyMuPDF>=1.23.0
- Pillow>=10.0.0

### Build Tools

**For Local Builds**:
- PyInstaller: `pip install pyinstaller`
- Inno Setup: [Download](https://jrsoftware.org/isdl.php) (optional)

**For GitHub Actions**: Everything installed automatically

## Commit Conventions

Use semantic commit messages for automatic version detection:

```bash
# Minor version bump (new features)
git commit -m "feat: add PDF comparison feature"
git commit -m "feature: support multiple formats"

# Patch version bump (fixes)
git commit -m "fix: correct BOM parsing"
git commit -m "docs: update README"
git commit -m "chore: update dependencies"

# Major version bump (breaking changes)
git commit -m "feat!: redesign API"
git commit -m "BREAKING CHANGE: remove deprecated methods"
```

## Release Workflow

### Standard Release

```powershell
# 1. Make changes
# 2. Commit with semantic message
git add .
git commit -m "feat: add new report format"

# 3. Run automated release
python scripts/release.py --auto

# 4. GitHub Actions builds and publishes automatically
# 5. Users download from GitHub Releases
```

### Hotfix Release

```powershell
# 1. Fix bug
git add .
git commit -m "fix: critical bug in BOM parser"

# 2. Quick patch release
python scripts/release.py --auto --bump patch

# 3. Automatic build and publish
```

### Major Release

```powershell
# 1. Breaking changes
git add .
git commit -m "BREAKING CHANGE: new config format"

# 2. Major version release
python scripts/release.py --auto --bump major

# 3. Update CHANGELOG.md with migration guide
```

## Testing

### Test Build Locally

```powershell
# Build without releasing
python scripts/build_local.py

# Test the EXE
.\dist\COC_Report_Generator.exe

# Test the installer
.\dist\installer\COC_Report_Generator_Setup_1.0.0.exe
```

### Test Release Process

```powershell
# Test without pushing
python scripts/release.py
# Review summary, then cancel (n)

# Test with auto mode (dry run by canceling push)
python scripts/release.py --auto
# Ctrl+C before push (optional)
```

## Troubleshooting

### Build Errors

**Problem**: PyInstaller not found
```powershell
pip install pyinstaller
```

**Problem**: Inno Setup not found
- Download: https://jrsoftware.org/isdl.php
- Or skip installer: build script will only create EXE

**Problem**: Git remote not configured
```powershell
git remote add origin https://github.com/Koolkop1@/COCforPCBs.git
```

### Release Errors

**Problem**: GitHub Actions fails
- Check workflow logs in GitHub Actions tab
- Verify all dependencies in requirements.txt
- Check version_info.txt syntax

**Problem**: No version detected
```powershell
# Create initial tag
git tag v1.0.0
git push origin v1.0.0
```

## Best Practices

1. **Always use semantic commits** for automatic version detection
2. **Test builds locally** before releasing
3. **Use `--auto` flag** for consistency
4. **Update CHANGELOG.md** for major releases
5. **Verify checksums** after release
6. **Keep requirements.txt updated**

## Support

- **Documentation**: See `scripts/README.md`
- **Issues**: GitHub Issues
- **Releases**: GitHub Releases page
