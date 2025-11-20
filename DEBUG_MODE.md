# Debug Mode Guide

## Overview

All COC report generation scripts now support a **debug mode** that provides detailed logging for troubleshooting issues.

## How to Enable Debug Mode

### Method 1: Using Debug Launchers (Recommended)

**Windows Batch:**
```cmd
.\create_report_debug.bat
```

**PowerShell:**
```powershell
.\create_report_debug.ps1
```

### Method 2: Command Line Arguments

**Direct Python:**
```cmd
python create_report.py --debug
python create_report.py -d
```

**Through Batch File:**
```cmd
.\create_report.bat --debug
```

**Through PowerShell:**
```powershell
.\create_report.ps1 --debug
```

## What Debug Mode Does

When debug mode is enabled:

1. **Detailed Console Output**: Shows step-by-step execution details
2. **Debug Log File**: Creates `coc_debug.log` in the workspace root
3. **File Detection Logging**: Shows exactly which files are found and where
4. **Metadata Extraction Logging**: Details version/variant extraction from BOM files
5. **Configuration Logging**: Shows all CONFIG values being used
6. **Error Stack Traces**: Full traceback information for troubleshooting

## Debug Log File

The debug log file (`coc_debug.log`) contains:
- Timestamps for each operation
- Line numbers where operations occur
- Full file paths being searched
- Metadata extraction results
- Configuration values
- Error details with stack traces

## Example Debug Output

```
2025-11-19 20:15:42 - DEBUG - [generate_coc_report.py:152] - auto_detect_config: workspace_path=C:\...\PSU2 V10 COC
2025-11-19 20:15:42 - DEBUG - [generate_coc_report.py:156] - auto_detect_config: input_dir=C:\...\input_files, exists=True
2025-11-19 20:15:42 - DEBUG - [generate_coc_report.py:157] - auto_detect_config: search_dir=C:\...\input_files
2025-11-19 20:15:42 - DEBUG - [generate_coc_report.py:165] - auto_detect_config: bom_files=['BT3413A-8 (Bill of Materials).xlsx', 'BT3413A-10 (Bill of Materials).xlsx']
```

## When to Use Debug Mode

Use debug mode when:
- ✅ Files are not being detected
- ✅ Version/variant information is incorrect
- ✅ Script fails with unclear error messages
- ✅ Investigating unexpected behavior
- ✅ Reporting issues for support

## Turning Off Debug Mode

Simply run the normal launchers without the `--debug` flag:
```cmd
.\create_report.bat
```

## Debug Log Cleanup

The `coc_debug.log` file is overwritten each time you run in debug mode. To preserve multiple debug sessions, rename the log file before running again.

## Privacy Note

Debug logs may contain file paths and configuration details from your workspace. Review the log file before sharing for support purposes.
