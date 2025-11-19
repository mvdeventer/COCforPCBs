# COC Report Generator - Usage Guide

## Quick Start

### Generate a COC Report

```powershell
python generate_coc_report.py
```

### Create a GitHub Release

```powershell
python scripts/release.py
```

**Pro Tip**: Press Enter at version prompt for automatic patch version bump!

## Auto-Detection Feature

The script **automatically detects** configuration from your files:

**What it extracts**:

- Product name from BOM filename (e.g., BT3413A)
- Version numbers (sorts numerically: 8 < 10)
- All file paths automatically matched

**Example**:

```text
Input files:
  BT3413A-8 (Bill of Materials).xlsx
  BT3413A-10 (Bill of Materials).xlsx

Auto-detected:
  Product: BT3413A
  Old Version: V8
  New Version: V10
```

## GitHub Release Workflow

### Step-by-Step

1. **Run Release Script**:

   ```powershell
   python scripts/release.py
   ```

2. **Archive Reports**:
   - Old reports moved to `reports_archive/YYYY/MM/`
   - Skips files in use (close Word first)
   - Organized by date

3. **Version Selection**:
   - Detects latest tag from GitHub
   - Choose bump type:
     - `1` = Patch (v1.0.1) - bug fixes
     - `2` = Minor (v1.1.0) - new features
     - `3` = Major (v2.0.0) - breaking changes
     - `4` = Custom version

4. **Changelog**:
   - Enter changes (one per line)
   - Empty line to finish
   - Auto-generates release notes

5. **Confirmation**:
   - Review summary
   - Confirm release (y/n)

6. **Automated Steps**:
   - ✅ Commits changes
   - ✅ Creates annotated tag
   - ✅ Pushes to GitHub
   - ✅ Creates GitHub release (if `gh` CLI installed)
   - ✅ Saves metadata JSON

### Release Script Features

**📦 Automatic Archiving**:

- Reports organized by year/month
- Structure: `reports_archive/2025/11/COC_Report_*.docx`
- Handles file-in-use errors gracefully

**📊 Version Management**:

- Reads latest tag from GitHub
- Semantic versioning (major.minor.patch)
- Custom version support

**📝 Release Notes**:

- Auto-generated from changelog
- Includes feature list
- Links to previous version

**🚀 GitHub Integration**:

- Pushes to master/main branch
- Creates annotated tags
- GitHub release with notes
- Requires `gh` CLI for releases

## What's Analyzed

### ✅ BOM Comparison
- **Added Components**: Parts present in V10 but not in V8
- **Removed Components**: Parts present in V8 but not in V10
- **Quantity Changes**: Same parts with different quantities

### ✅ Assembly Drawing Analysis
The tool now detects:
- **SMD Migration**: Components moved to top side for production efficiency
- **Component Placement**: Top side vs bottom side references
- **Manufacturing Type**: SMD vs through-hole component counts
- **Component Count**: Total designators found

### ✅ Schematic Analysis
- Extracts metadata and page counts
- Includes PDF links in report for easy access

## Report Features

### 📊 Professional Word Document
- Formatted tables with component details
- Clickable PDF links to source documents
- Assembly placement comparison tables
- Manufacturing improvement notes
- Complete change summary

### 🔗 PDF Links
The report includes hyperlinks to:
- Schematic PDFs (V8 and V10)
- Assembly Drawing PDFs (V8 and V10)

Click the links in the Word document to open the source PDFs directly.

## Manufacturing Insights

The tool specifically identifies:

**✓ SMD components migrated to top side**
- Improves production speed
- Increases manufacturing efficiency
- Reduces assembly time
- Simplifies PCB handling

## Using with Different Products

**No configuration needed!** The script auto-detects everything.

### Workflow for New Product

1. **Add Files**:
   - `NewProduct-1 (Bill of Materials).xlsx`
   - `NewProduct-2 (Bill of Materials).xlsx`
   - `NewProduct-1 (Schematic...).PDF`
   - `NewProduct-2 (Schematic...).PDF`
   - etc.

2. **Run Generator**:

   ```powershell
   python generate_coc_report.py
   ```

3. **Auto-Detection Output**:

   ```text
   AUTO-DETECTED CONFIGURATION
   Product Name: NewProduct
   Old Version: V1
   New Version: V2
   ...
   ```

4. **Complete Questionnaire**:
   - Fill in document creator info
   - Document change reasons
   - Add engineering summary

5. **Generate Report**:
   - Output: `COC_Report_NewProduct_V1_to_V2_YYYYMMDD_HHMMSS.docx`

## Troubleshooting

### COC Generator Issues

**PDF not found error?**

- Check filename spacing
- Verify files in same folder as script
- Check glob patterns match your filenames

**Wrong version detected?**

- Versions are sorted numerically (8 < 10)
- Use numeric versions in filenames
- Check filename pattern: `PRODUCT-VERSION (Bill...)`

**Missing dependencies?**

```powershell
pip install pandas openpyxl PyPDF2 python-docx PyMuPDF Pillow
```

### Release Script Issues

**Git errors?**

```powershell
# Reinitialize if needed
git init
git remote add origin https://github.com/USERNAME/REPO.git
```

**Push failed?**

- Check GitHub authentication
- Try: `git push -u origin master`
- Or: `git push -u origin main`

**GitHub release failed?**

- Install GitHub CLI: https://cli.github.com/
- Authenticate: `gh auth login`
- Try release script again

**File in use error?**

- Close Word documents before archiving
- Release script will skip locked files
- Manually move reports later if needed
