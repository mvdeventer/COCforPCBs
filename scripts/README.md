# Scripts Folder

This folder contains automation scripts for the COC Report Generator project.

## Available Scripts

### release.py

GitHub release automation script with intelligent version detection and automated release note generation.

**Purpose**: Automate the entire release process including version detection from GitHub, automatic changelog generation, git operations, and GitHub release creation with EXE builds.

**Location**: `scripts/release.py`

**Usage**:

```powershell
# Fully automated mode (recommended)
python scripts/release.py --auto

# Manual mode with prompts
python scripts/release.py

# Specify version bump type
python scripts/release.py --auto --bump minor
python scripts/release.py --bump major
```

**Features**:

- **🤖 GitHub API Integration**: Fetches latest release from GitHub API
- **📊 Smart Version Detection**: Auto-detects version bump type from commit messages
  - `feat:` or `feature:` → Minor version bump
  - `BREAKING CHANGE` or `!:` → Major version bump
  - Other commits → Patch version bump
- **📝 Auto-Generated Changelog**: Extracts commit messages since last release
- **📦 Automatic Report Archiving**: Moves old COC reports to `reports_archive/YYYY/MM/`
- **✅ Git Integration**: Commits, tags, and pushes automatically
- **🎉 GitHub Releases**: Creates GitHub release with auto-generated notes
- **💾 Metadata Tracking**: Saves release information to `release_metadata.json`

**Version Bump Detection**:

The script analyzes commit messages to determine the appropriate version bump:

| Commit Pattern | Version Bump | Example |
|---------------|--------------|---------|
| `feat:` or `feature:` | Minor | v1.0.0 → v1.1.0 |
| `BREAKING CHANGE` or `!:` | Major | v1.0.0 → v2.0.0 |
| `fix:`, `docs:`, etc. | Patch | v1.0.0 → v1.0.1 |

**Command Options**:

- `--auto`: Fully automated mode (no prompts)
- `--bump {major,minor,patch}`: Override auto-detection

**Workflow**:

```text
AUTO MODE:
1. Run → python scripts/release.py --auto
2. Fetch latest GitHub release → v1.0.1
3. Analyze commits → Detect "feat:" commits
4. Auto-bump version → v1.1.0
5. Generate changelog → From commit messages
6. Commit & tag → git operations
7. Push to GitHub → Trigger CI/CD
8. GitHub Actions builds EXE → Automated
9. Create release → With binaries attached

MANUAL MODE:
1. Run → python scripts/release.py
2. Select version bump → Interactive menu
3. Enter changelog → Line by line
4. Review summary → Confirm
5. Execute release → Push to GitHub
```

### build_local.py

Local build script for creating standalone EXE and Windows installer.

**Purpose**: Build COC Report Generator executable and installer locally without GitHub Actions.

**Location**: `scripts/build_local.py`

**Usage**:

```powershell
# Build everything (EXE + installer)
python scripts/build_local.py

# Skip cleaning build directories
python scripts/build_local.py --skip-clean
```

**Features**:

- **🔨 PyInstaller Build**: Creates standalone EXE from Python script
- **📦 Inno Setup Installer**: Builds Windows installer with version info
- **📝 Auto-Version Update**: Updates version_info.txt and installer.iss
- **🔐 Checksum Generation**: Creates SHA256 checksums for verification
- **📁 Release Package**: Bundles EXE, installer, docs, and checksums

**Requirements**:

- Python 3.12+
- PyInstaller: `pip install pyinstaller`
- Inno Setup (optional): [Download](https://jrsoftware.org/isdl.php)

**Output**:

```text
dist/
├── COC_Report_Generator_{version}/
│   ├── COC_Report_Generator.exe
│   ├── COC_Report_Generator_Setup_{version}.exe
│   ├── checksums.txt
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
```

**Workflow**:

```text
1. Detect version from git tags
2. Update version_info.txt and installer.iss
3. Clean old build artifacts
4. Build EXE with PyInstaller
5. Build installer with Inno Setup (if available)
6. Generate SHA256 checksums
7. Create release package folder
8. Copy all files to release folder
```

## Build Configuration Files

### coc_report.spec

PyInstaller specification file defining how the EXE is built.

**Features**:
- Auto-detects version from git tags
- Includes company logo and documentation
- Optimized for Windows with UPX compression
- Includes version_info.txt for Windows metadata

### version_info.txt

Windows executable version information (file properties).

**Updated by**:
- `build_local.py` (local builds)
- GitHub Actions (CI/CD builds)

### installer.iss

Inno Setup script for creating Windows installer.

**Features**:
- Modern wizard UI
- Desktop icon option
- Uninstaller included
- Version-specific output filename

## GitHub Actions Workflow

### .github/workflows/release.yml

Automated build and release on tag push.

**Triggers**:
- Push tag matching `v*.*.*` (e.g., v1.0.0)
- Manual workflow dispatch

**Process**:
1. Checkout code
2. Set up Python 3.12
3. Install dependencies
4. Update version files
5. Build EXE with PyInstaller
6. Install Inno Setup
7. Build Windows installer
8. Generate checksums
9. Generate release notes from commits
10. Create GitHub release with binaries

**Usage**:

```powershell
# Option 1: Use release script (recommended)
python scripts/release.py --auto

# Option 2: Manual tag push
git tag v1.0.0
git push origin v1.0.0
```

## Adding New Scripts

When adding new scripts to this folder:

1. **Create script** in `scripts/` folder
2. **Update this README** with:
   - Script name and purpose
   - Usage instructions
   - Examples
3. **Update main README.md** if user-facing
4. **Run release script** to version the changes:
   ```powershell
   python scripts/release.py --auto
   ```

## Folder Structure

```text
scripts/
├── release.py           # GitHub release automation
├── build_local.py       # Local EXE/installer build
└── README.md           # This file

Root level:
├── coc_report.spec      # PyInstaller configuration
├── version_info.txt     # Windows EXE metadata
├── installer.iss        # Inno Setup installer script
├── requirements.txt     # Python dependencies
└── .github/
    └── workflows/
        └── release.yml  # GitHub Actions CI/CD
```

## Best Practices

- **Always use `--auto` flag** for automated releases
- **Use semantic versioning** in commit messages:
  - `feat:` for new features (minor bump)
  - `fix:` for bug fixes (patch bump)
  - `BREAKING CHANGE:` for breaking changes (major bump)
- **Test builds locally** before pushing tags
- **Run from repository root**: `python scripts/scriptname.py`
- **Keep version files in sync** (automated by scripts)

## Release Process Comparison

| Method | When to Use | Command |
|--------|-------------|---------|
| **Automated GitHub** | Production releases | `python scripts/release.py --auto` |
| **Manual GitHub** | Complex releases | `python scripts/release.py` |
| **Local Build** | Testing, offline | `python scripts/build_local.py` |
