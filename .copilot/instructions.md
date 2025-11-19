# Copilot Instructions for COCforPCBs Repository

## Automatic Documentation Updates

When making ANY code changes to this repository, **ALWAYS** update the following documentation files:

### Required Documentation Files

1. **README.md** - Main repository documentation
   - Update if: Features change, new scripts added, workflow modified
   - Include: Installation, usage, examples

2. **USAGE_GUIDE.md** - Detailed usage instructions
   - Update if: User workflows change, new commands added, troubleshooting needed
   - Include: Step-by-step guides, examples, common issues

3. **IMAGE_FEATURE.md** - Advanced features documentation
   - Update if: New features added, workflows enhanced
   - Include: Feature descriptions, benefits, examples

4. **scripts/README.md** - Scripts folder documentation
   - Update if: New scripts added, script behavior changes
   - Include: Script descriptions, usage, parameters

## Scripts Folder

All automation scripts are located in `scripts/` folder:

- `scripts/release.py` - GitHub release automation

### When Adding New Scripts

1. Place script in `scripts/` folder
2. Update `scripts/README.md` with:
   - Script name and purpose
   - Usage instructions
   - Example commands
3. Update main `README.md` if user-facing
4. Update `USAGE_GUIDE.md` with workflow details

## Release Script Usage

### Location
`scripts/release.py`

### Features
- Auto-archives old reports to `reports_archive/YYYY/MM/`
- Auto-detects latest version from git tags
- Supports auto-version bump (press Enter or option 5)
- Creates GitHub releases with notes
- Saves release metadata

### Auto-Version Detection
When no version is specified (user presses Enter), the script:
1. Reads latest tag from git
2. Automatically increments patch version
3. Example: v1.0.1 → v1.0.2

### Running
```powershell
python scripts/release.py
```

## Code Change Workflow

When modifying code:

1. **Make code changes**
2. **Test changes**
3. **Update documentation**:
   - README.md (if user-facing)
   - USAGE_GUIDE.md (if workflow changes)
   - IMAGE_FEATURE.md (if features added)
   - scripts/README.md (if scripts modified)
4. **Run release script**:
   ```powershell
   python scripts/release.py
   ```
5. **Select version bump** (or press Enter for auto-patch)
6. **Enter changelog**
7. **Confirm release**

## Version Bumping Guidelines

- **Patch (auto)**: Bug fixes, documentation updates, small tweaks
- **Minor**: New features, enhancements, non-breaking changes
- **Major**: Breaking changes, major rewrites, API changes

## Documentation Standards

### Markdown Files
- Use clear headings
- Include code examples with syntax highlighting
- Add emojis for visual clarity (✅ ❌ 📊 🚀 etc.)
- Keep examples up-to-date with actual code

### Code Examples
Always show full commands:
```powershell
# Good
python scripts/release.py

# Bad
python release.py  # (wrong path!)
```

### File Paths
Use correct paths based on repository structure:
- Scripts: `scripts/`
- Reports: `reports_archive/YYYY/MM/`
- Main generator: `generate_coc_report.py` (root)

## Auto-Detection Features

The repository uses auto-detection for:
1. **Product names** - from BOM filenames
2. **Version numbers** - from BOM filenames (numerically sorted)
3. **Next release version** - from git tags (auto-patch)

Always document how auto-detection works when adding new features.

## Important Reminders

- ✅ Scripts are in `scripts/` folder, NOT root
- ✅ Always update documentation with code changes
- ✅ Test release script after significant changes
- ✅ Use auto-version (Enter) for quick releases
- ✅ Keep examples in sync with actual code behavior
