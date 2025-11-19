# COC Report - Advanced Features

## ✅ Latest Enhancements

### v1.0.1 - Auto-Detection & Release Automation

- **Auto-detects** product name and versions from BOM filenames
- **GitHub release script** with automatic archiving
- **Interactive versioning** with changelog collection
- **Semantic versioning** support (major.minor.patch)

### v1.0.0 - Image Embedding

The COC report includes **embedded PDF images** directly in the Word document!

## Release Management

### Creating Releases

Use the automated release script:

```powershell
python scripts/release.py
```

**Quick Release**: Press Enter for auto-patch version bump!

**Features**:

- Archives old reports by date
- Auto-detects latest version from GitHub
- Interactive version bumping
- Changelog collection
- GitHub release creation
- Metadata tracking

### Report Archive Structure

```text
reports_archive/
└── 2025/
    └── 11/
        ├── COC_Report_BT3413A_V8_to_V10_20251119_125449.docx
        ├── COC_Report_PSU2_V8_to_V10_20251119_123142.docx
        └── ...
```

### Version History

Reports are automatically named with:

- Product name (auto-detected)
- Version comparison
- Timestamp

Example: `COC_Report_BT3413A_V8_to_V10_20251119_125449.docx`

## What's Included in the Report

### 📊 Document Sections

1. **Document Information**
   - Product details
   - Version comparison
   - Report timestamp

2. **BOM Changes** (with tables)
   - Added components
   - Removed components
   - Modified quantities

3. **Schematic Analysis** (with embedded images)
   - PDF links to V8 and V10 schematics
   - **📷 Page 1 of V8 schematic (embedded image)**
   - **📷 Page 1 of V10 schematic (embedded image)**

4. **Assembly Drawing Analysis** (with embedded images)
   - PDF links to V8 and V10 assembly drawings
   - Component placement comparison table
   - Manufacturing improvements notes
   - **📷 Page 1 of V8 assembly drawing (embedded image)**
   - **📷 Page 1 of V10 assembly drawing (embedded image)**

5. **Summary**
   - Total changes count

## Features

### 🖼️ Embedded Images
- High-quality PNG renders of PDF first pages
- 6-inch width for readability
- Automatically cleaned up after embedding
- No external image files to manage

### 🔗 Clickable Links
- Hyperlinks to all source PDFs
- Easy access to full documents

### 📈 Smart Analysis
- Detects SMD migration to top side
- Component placement tracking
- Manufacturing efficiency improvements

## Workflow

### 1. Generate COC Report

```powershell
python generate_coc_report.py
```

The script will:

1. **Auto-detect** product name and versions from filenames
2. Compare BOMs
3. Analyze assembly drawings
4. Convert PDF pages to images
5. Launch GUI questionnaire
6. Embed images in Word report
7. Add hyperlinks to source PDFs
8. Generate complete COC document

### 2. Create GitHub Release

```powershell
python scripts/release.py
```

The script will:

1. **Archive** old reports to `reports_archive/YYYY/MM/`
2. **Detect** latest version from GitHub tags
3. **Prompt** for version bump (patch/minor/major)
4. **Collect** changelog entries
5. **Commit** changes with version tag
6. **Push** to GitHub
7. **Create** GitHub release with notes

## For Copilot Users

To create releases:

1. **Install GitHub CLI** (optional but recommended):

   ```powershell
   # Download from: https://cli.github.com/
   gh auth login
   ```

2. **Run release script**:

   ```powershell
   python release.py
   ```

3. **Follow prompts**:
   - Select version bump type
   - Enter changelog items
   - Confirm release

4. **Result**:
   - Code committed and tagged
   - Reports archived by date
   - GitHub release created
   - Release notes generated

The release script handles all Git operations automatically!

## Image Quality

Images are rendered at:
- **2x zoom** for high quality
- **PNG format** for clarity
- **6.0 inches width** in the document

## Customization Options

### Change Image Size
Edit in `generate_coc_report.py`:
```python
doc.add_picture(str(img_path), width=Inches(6.0))  # Change 6.0 to desired width
```

### Add More Pages
Modify to include additional pages:
```python
# Add page 2
img_path = self.pdf_page_to_image(self.pdf_paths['schematic_v10'], 1)  # page_num=1
```

### Adjust Image Quality
Change zoom level in `pdf_page_to_image`:
```python
zoom = 2  # Increase for higher quality (e.g., 3 or 4)
```

## Benefits

✅ **Visual comparison** - See schematics and layouts side-by-side
✅ **Self-contained report** - All images embedded in one file
✅ **Professional presentation** - High-quality renders
✅ **Easy sharing** - Single Word document with everything
✅ **Automatic cleanup** - No temporary files left behind

## Technical Details

**Libraries Used**:
- `PyMuPDF (fitz)` - PDF rendering
- `Pillow (PIL)` - Image processing
- `python-docx` - Word document generation

**Process**:
1. Opens PDF with PyMuPDF
2. Renders page to high-res pixmap
3. Converts to PNG via PIL
4. Embeds in Word document
5. Deletes temporary image file

## Run the Generator

```powershell
python generate_coc_report.py
```

The script will:
1. Compare BOMs
2. Analyze assembly drawings
3. Convert PDF pages to images
4. Embed images in Word report
5. Add hyperlinks to source PDFs
6. Generate complete COC document
