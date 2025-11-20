# Input File Configuration Guide

## Overview

The COC Report Generator now supports manual file selection with persistent configuration. Select your 6 input files once, and they'll be remembered for all future runs.

## Quick Start

### First Time Setup

1. Run the configuration tool:
   ```cmd
   .\configure_files.bat
   ```

2. In the GUI dialog, browse and select all 6 files:
   - Old BOM (Excel)
   - New BOM (Excel)
   - Old Schematic (PDF)
   - New Schematic (PDF)
   - Old Assembly Drawing (PDF)
   - New Assembly Drawing (PDF)

3. Click "Save & Continue"

4. Your configuration is saved to `input_files_config.json`

### Running Reports

After configuration, simply run:
```cmd
.\create_report.bat
```

The script will automatically use your configured files!

## Configuration File

### Location
`input_files_config.json` in the workspace root

### Format
```json
{
  "bom_old": "C:\\...\\BT3413A-8 (Bill of Materials).xlsx",
  "bom_new": "C:\\...\\BT3413A-10 (Bill of Materials).xlsx",
  "schematic_old": "C:\\...\\BT3415B-8(Schematic Circuit Diagram).PDF",
  "schematic_new": "C:\\...\\BT3415B-10 (Schematic Circuit Diagram).PDF",
  "assembly_old": "C:\\...\\BT3411B-8(Assembly Drawing).PDF",
  "assembly_new": "C:\\...\\BT3411B-10 (Assembly Drawing).PDF",
  "last_updated": "2025-11-19T20:30:00"
}
```

### Git Integration

The configuration file is **tracked in git** so it can be:
- ✅ Committed with your project
- ✅ Shared across team members
- ✅ Restored from previous commits
- ✅ Versioned alongside code changes

## Command Line Options

### Configure Files
```cmd
python create_report.py --configure
# or
python create_report.py -c
```
Opens the file selector dialog.

### Force Auto-Detection
If you have a config file but want to use auto-detection instead:
1. Delete or rename `input_files_config.json`
2. Run normally: `.\create_report.bat`

Or click "Auto-Detect Files" in the configuration dialog.

## File Selection Dialog Features

- **Browse Buttons**: Easy file selection with file type filters
- **Pre-filled Values**: Shows previously configured files
- **Validation**: Ensures all 6 files are selected before saving
- **Existence Check**: Verifies files exist before saving
- **Auto-Detect Option**: Skip manual selection and use directory scanning

## Workflow Integration

### For New Projects

1. Place input files in `input_files/` directory
2. Run `.\configure_files.bat`
3. Select files and save
4. Commit `input_files_config.json`:
   ```cmd
   git add input_files_config.json
   git commit -m "Configure input files for COC report"
   ```

### For Existing Projects

Pull the repository and the configuration comes with it!
```cmd
git pull
.\create_report.bat  # Uses committed configuration
```

### Updating Files

When files change (new versions):
1. Run `.\configure_files.bat`
2. Select new files
3. Save and commit:
   ```cmd
   git add input_files_config.json
   git commit -m "Update input files to V11"
   ```

## Fallback Behavior

The script uses this priority order:

1. **Manual Configuration** (`input_files_config.json`) - if exists
2. **Auto-Detection** - scans `input_files/` directory
3. **Workspace Root** - scans workspace if no `input_files/` folder

## Troubleshooting

### Configuration Not Saving
- Check file permissions in workspace directory
- Run with `--debug` to see detailed error messages

### Files Not Found
- Verify absolute paths in `input_files_config.json`
- Use "Browse" buttons to ensure correct paths
- Files may have been moved - reconfigure

### Want Fresh Auto-Detection
- Click "Auto-Detect Files" in the dialog
- Or delete `input_files_config.json`

## Benefits

✅ **Explicit Control**: Choose exactly which files to use
✅ **Persistent**: Configuration remembered between sessions
✅ **Shareable**: Commit config to share with team
✅ **Flexible**: Mix files from different locations
✅ **Validated**: Ensures all required files are selected
✅ **Fast**: No need to reconfigure every time
✅ **Versioned**: Track file configurations in git history
