# COC Report Generator

Automated Certificate of Conformity (COC) report generator that compares different versions of BOMs and analyzes schematics/assembly drawings. Automatically detects product names and versions from filenames.

## Features

✅ **Auto-Detection**
- Automatically detects product name from BOM filenames
- Auto-detects version numbers (sorts numerically)
- No manual configuration needed
- Works with any product/version naming

✅ **BOM Comparison**
- Identifies added components
- Identifies removed components
- Detects quantity changes
- Compares part numbers and descriptions

✅ **Document Analysis**
- Analyzes schematic PDFs
- Analyzes assembly drawing PDFs
- Extracts text and metadata
- Embeds PDF images in report

✅ **Professional Report Generation**
- Creates formatted Word documents with company branding
- Interactive GUI questionnaire for change documentation
- Includes tables, summaries, and signature blocks
- Headers/footers with page numbers
- Timestamps and version tracking

## File Naming Convention

The script **automatically detects** product and versions from BOM filenames:

**Pattern**: `PRODUCT-VERSION (Bill of Materials).xlsx`

**Example**:

- `BT3413A-8 (Bill of Materials).xlsx` → Product: BT3413A, Version: V8
- `BT3413A-10 (Bill of Materials).xlsx` → Product: BT3413A, Version: V10

**Supported Files**:

- BOMs: `*Bill of Materials*.xlsx`
- Schematics: `*Schematic*.PDF`
- Assembly: `*Assembly*.PDF`

Files are automatically sorted by version number (8 < 10)

## How to Use

### Quick Start (Recommended)

```powershell
# Generate COC report (automatically uses venv)
python create_report.py
```

### 1. Generate COC Report

**Option A: Use Quick Launcher (Auto-Venv)**
```powershell
python create_report.py
```

**Option B: Run Directly**
```powershell
python generate_coc_report.py
```

The script will:

1. Auto-detect product name and versions from BOM file contents
2. Compare BOMs and analyze PDFs
3. Launch GUI questionnaire for change documentation
4. Generate professional Word report

**Output**: `coc_reports/COC_Report_PRODUCT_VOLD_to_VNEW_YYYYMMDD_HHMMSS.docx`

### 2. Build Executables

**Build EXE Only:**
```powershell
python build_exe.py
```

**Build Complete Installer:**
```powershell
python build_installer.py
```

Both scripts automatically use the virtual environment.

**Output:**
- `dist/COC_Report_Generator.exe`
- `dist/installer/COC_Report_Generator_Setup_X.X.X.exe`

### 3. Release to GitHub

Create versioned releases with automatic version management:

```powershell
# Fully automated release
python scripts/release.py --auto
```

The release script will:

1. ✅ Analyze commits to determine version bump
2. ✅ Update version files automatically
3. ✅ Commit changes with version tag
4. ✅ Push to GitHub repository
5. ✅ Create GitHub release with notes (if `gh` CLI installed)

**Version Management**:

- `fix:` commits → **Patch** (v1.0.1): Bug fixes
- `feat:` commits → **Minor** (v1.1.0): New features
- `BREAKING CHANGE:` → **Major** (v2.0.0): Breaking changes

## Report Contents

1. **Document Information**
   - Product name
   - Version comparison
   - Report date and time
   - Generator info

2. **BOM Changes**
   - Added components (with part numbers, descriptions, quantities)
   - Removed components
   - Modified quantities

3. **Schematic Analysis**
   - Files analyzed
   - Page counts
   - Manual review notes

4. **Assembly Drawing Analysis**
   - Files analyzed
   - Layout change notes

5. **Summary**
   - Total changes count
   - Quick overview

## Requirements

### Python Packages

```bash
pip install pandas openpyxl PyPDF2 python-docx PyMuPDF Pillow
```

### Optional: GitHub CLI (for releases)

```bash
# Install from: https://cli.github.com/
gh auth login
```

### Manual Review Recommended

While the tool automates BOM comparison, **manual review is recommended for**:
- Circuit topology changes in schematics
- Component placement changes in assembly drawings
- Electrical performance impacts
- Safety/compliance implications

## Reusing for Different Products

**No code changes needed!** Just place your files in the folder:

1. Add two BOM files: `PRODUCT-VER1 (Bill of Materials).xlsx`
2. Add schematic PDFs: `PRODUCT-VER1 (Schematic...).PDF`
3. Add assembly PDFs: `PRODUCT-VER1 (Assembly...).PDF`
4. Run: `python generate_coc_report.py`

The CONFIG is automatically populated from filenames.

## Repository Structure

```text
COCforPCBs/
├── generate_coc_report.py       # Main COC generator
├── scripts/                      # Automation scripts
│   ├── release.py               # GitHub release automation
│   └── README.md                # Scripts documentation
├── reports_archive/              # Archived reports by date
│   └── 2025/
│       └── 11/
│           └── COC_Report_*.docx
├── .copilot/                     # Copilot instructions
│   └── instructions.md          # Auto-update guidelines
├── LHA_logo.png                  # Company logo
├── *.xlsx                        # BOM files
├── *.PDF                         # Schematic/Assembly PDFs
└── README.md                     # This file
```

## Version History

See [Releases](https://github.com/Koolkop1@/COCforPCBs/releases) for version history.

**Current Version**: v1.0.1

- Auto-detection of product/versions from filenames
- GitHub release automation with archiving
- Interactive GUI questionnaire
- Professional report generation with branding

## AI Model Used

This tool was created using **GitHub Copilot (Claude Sonnet 4.5)** which can:

- Analyze Excel and PDF files
- Compare document versions
- Process images and schematics
- Generate structured reports
- Auto-detect patterns in filenames

## Contributing

To contribute:

1. Fork the repository
2. Make your changes
3. Commit your changes (version files are auto-updated via pre-commit hook)
4. Update relevant documentation (see `.copilot/instructions.md`)
5. Run `python scripts/release.py --auto` to create a versioned release
6. Submit pull request

**Version Management**:
- Version files (`version_info.txt`, `installer.iss`) are automatically updated before each commit
- See [VERSION_MANAGEMENT.md](VERSION_MANAGEMENT.md) for details
- Pre-commit hook ensures consistency across all version files

**Note**: Copilot will automatically remind you to update documentation files when making code changes.

## Support

For issues or enhancements:

- Open an issue on GitHub
- Ask GitHub Copilot for assistance
- Check existing releases and documentation
