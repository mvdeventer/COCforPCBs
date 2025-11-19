# Changelog

All notable changes to the COC Report Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub API integration for automatic release detection
- Intelligent version bump detection from commit messages
- Automated changelog generation from git commits
- PyInstaller spec file for building standalone EXE
- Windows installer script using Inno Setup
- GitHub Actions workflow for automated builds and releases
- Local build script (`scripts/build_local.py`) for offline builds
- SHA256 checksum generation for releases
- Version info file for Windows EXE metadata
- Requirements.txt for dependency management

### Changed
- `release.py` now supports `--auto` flag for fully automated releases
- `release.py` now supports `--bump` flag to specify version bump type
- Version detection now uses GitHub API as primary source
- Changelog collection now auto-generates from commit messages

### Improved
- Release process is now completely hands-free with `--auto` flag
- Version bumping follows semantic versioning based on commit conventions
- Documentation updated with comprehensive build and release instructions

## [1.0.1] - 2025-11-19

### Changed
- Moved release script to `scripts/` folder
- Updated all documentation with new script location

### Added
- Copilot instructions for automatic documentation updates

## [1.0.0] - 2025-11-19

### Added
- Initial release of COC Report Generator
- Automatic detection of product name and versions from BOM filenames
- BOM comparison (added/removed/modified components)
- PDF analysis for schematics and assembly drawings
- Interactive GUI questionnaire for change documentation
- Professional Word document reports with company branding
- Company logo and header/footer integration
- Engineering summary with total pages field
- Auto-populated configuration from file naming conventions

### Features
- Regex-based product and version detection
- Numerical version sorting (V8 before V10)
- File path auto-detection
- Professional report formatting with modern styles
- Comprehensive change tracking and documentation

---

## Release Types

- **Major** (x.0.0): Breaking changes, significant new features
- **Minor** (0.x.0): New features, enhancements, backward compatible
- **Patch** (0.0.x): Bug fixes, minor improvements

## Commit Conventions

Use these prefixes in commit messages for automatic version detection:

- `feat:` or `feature:` → Minor version bump
- `fix:` → Patch version bump
- `docs:` → Patch version bump
- `BREAKING CHANGE:` or `!:` → Major version bump
- `chore:`, `refactor:`, `style:`, `test:` → Patch version bump

## Links

- [Repository](https://github.com/Koolkop1@/COCforPCBs)
- [Issues](https://github.com/Koolkop1@/COCforPCBs/issues)
- [Releases](https://github.com/Koolkop1@/COCforPCBs/releases)
