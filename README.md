# COC Report Generator for PSU2

Automated Certificate of Conformity (COC) report generator that compares different versions of BOMs and analyzes schematics/assembly drawings.

## Features

✅ **BOM Comparison**
- Identifies added components
- Identifies removed components
- Detects quantity changes
- Compares part numbers and descriptions

✅ **Document Analysis**
- Analyzes schematic PDFs
- Analyzes assembly drawing PDFs
- Extracts text and metadata

✅ **Professional Report Generation**
- Creates formatted Word documents
- Includes tables and summaries
- Timestamps and version tracking

## Files Analyzed

### Version 8 (Baseline)
- `BT3413A-8 (Bill of Materials).xlsx`
- `BT3415B-8(Schematic Circuit Diagram).PDF`
- `BT3411B-8 (Assembly Drawing).PDF`

### Version 10 (New)
- `BT3413A-10 (Bill of Materials).xlsx`
- `BT3415B-10 (Schematic Circuit Diagram).PDF`
- `BT3411B-10 (Assembly Drawing).PDF`

## How to Use

### Quick Run
Simply run the Python script:
```powershell
python generate_coc_report.py
```

### Output
The script generates a Word document:
- Format: `COC_Report_PSU2_V8_to_V10_YYYYMMDD_HHMMSS.docx`
- Location: Same folder as the script
- Contains: Complete COC report with all changes

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

### Python Packages (Already Installed)
- pandas
- openpyxl
- PyPDF2
- python-docx
- pillow

### Manual Review Recommended

While the tool automates BOM comparison, **manual review is recommended for**:
- Circuit topology changes in schematics
- Component placement changes in assembly drawings
- Electrical performance impacts
- Safety/compliance implications

## Customization

To analyze different versions, update the file paths in `generate_coc_report.py`:
```python
bom_v8 = workspace / "BT3413A-8 (Bill of Materials).xlsx"
bom_v10 = workspace / "BT3413A-10 (Bill of Materials).xlsx"
# ... etc
```

## AI Model Used

This tool was created using **GitHub Copilot (Claude Sonnet 4.5)** which can:
- Analyze Excel and PDF files
- Compare document versions
- Process images and schematics
- Generate structured reports

## Support

For issues or enhancements, modify the Python script or ask GitHub Copilot for assistance.
