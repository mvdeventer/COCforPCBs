# COC Report Generator - Usage Guide

## Quick Start

Run the generator:
```powershell
python generate_coc_report.py
```

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

## Latest Report

Latest generated report:
- `COC_Report_PSU2_V8_to_V10_20251119_101040.docx`

## Analysis Results

From V8 → V10:
- **7 components added**
- **7 components removed**
- **50 components unchanged**
- **✓ SMD migration to top side detected**

## Customization

### For Different Versions
Edit file paths in `generate_coc_report.py`:
```python
bom_v8 = workspace / "BT3413A-8 (Bill of Materials).xlsx"
bom_v10 = workspace / "BT3413A-10 (Bill of Materials).xlsx"
```

### Add More Analysis
The tool can be extended to analyze:
- Cost changes between versions
- Weight/size comparisons
- Supplier changes
- Compliance certifications

## AI Model

**GitHub Copilot (Claude Sonnet 4.5)** powers this tool with:
- Excel file parsing
- PDF text extraction
- Image/schematic analysis (multimodal)
- Document generation
- Pattern recognition for SMD migration

## Troubleshooting

**PDF not found error?**
- Check filename spacing (e.g., `BT3411B-8(Assembly Drawing).PDF` vs `BT3411B-8 (Assembly Drawing).PDF`)
- Verify files are in the same folder as the script

**Missing dependencies?**
```powershell
pip install pandas openpyxl PyPDF2 python-docx PyMuPDF
```

## Next Steps

After reviewing the report:
1. Open linked PDFs to verify changes
2. Review BOM component details
3. Validate manufacturing improvements
4. Sign off on COC document
