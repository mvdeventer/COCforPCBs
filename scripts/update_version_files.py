"""
Pre-commit script to update version files before Git commit
Updates version_info.txt, installer.iss, and other version-dependent files
"""

import io
import re
import subprocess
import sys
from pathlib import Path

# Force UTF-8 encoding for stdout/stderr on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_latest_version():
    """Get latest version from git tags"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            return version, version.lstrip("v")
        else:
            return "v1.0.2", "1.0.2"
    except Exception:
        return "v1.0.2", "1.0.2"


def update_version_info(clean_version):
    """Update version_info.txt with current version"""
    version_file = Path("version_info.txt")
    if not version_file.exists():
        print(f"[WARNING] {version_file} not found")
        return False

    # Parse version parts
    parts = clean_version.split(".")
    major = parts[0] if len(parts) > 0 else "1"
    minor = parts[1] if len(parts) > 1 else "0"
    patch = parts[2] if len(parts) > 2 else "0"

    content = version_file.read_text(encoding="utf-8")

    # Update version numbers
    content = re.sub(
        r"filevers=\(.*?\)", f"filevers=({major}, {minor}, {patch}, 0)", content
    )
    content = re.sub(
        r"prodvers=\(.*?\)", f"prodvers=({major}, {minor}, {patch}, 0)", content
    )
    content = re.sub(
        r"u'FileVersion', u'.*?'", f"u'FileVersion', u'{clean_version}'", content
    )
    content = re.sub(
        r"u'ProductVersion', u'.*?'", f"u'ProductVersion', u'{clean_version}'", content
    )

    version_file.write_text(content, encoding="utf-8")
    print(f"[OK] Updated {version_file}")
    return True


def update_installer_iss(clean_version):
    """Update installer.iss with current version"""
    installer_file = Path("installer.iss")
    if not installer_file.exists():
        print(f"[WARNING] {installer_file} not found")
        return False

    content = installer_file.read_text(encoding="utf-8")
    content = re.sub(
        r'#define AppVersion ".*?"', f'#define AppVersion "{clean_version}"', content
    )
    installer_file.write_text(content, encoding="utf-8")
    print(f"[OK] Updated {installer_file}")
    return True


def update_changelog(version):
    """Update CHANGELOG.md with unreleased changes"""
    changelog_file = Path("CHANGELOG.md")
    if not changelog_file.exists():
        print(f"[WARNING] {changelog_file} not found")
        return False

    content = changelog_file.read_text(encoding="utf-8")

    # Check if there's already an entry for this version
    if f"## [{version.lstrip('v')}]" in content:
        print(f"[OK] CHANGELOG.md already has entry for {version}")
        return True

    print(f"[INFO] CHANGELOG.md - manual update recommended for {version}")
    return True


def stage_updated_files():
    """Stage the updated version files for commit"""
    files_to_stage = [
        "version_info.txt",
        "installer.iss",
    ]

    for file in files_to_stage:
        if Path(file).exists():
            subprocess.run(["git", "add", file], check=False)
            print(f"[STAGED] {file}")


def main():
    print("=" * 60)
    print("PRE-COMMIT: Updating version files")
    print("=" * 60)
    print()

    # Get current version
    version, clean_version = get_latest_version()
    print(f"[VERSION] Current version: {version}")
    print()

    # Update all version files
    updated = []

    if update_version_info(clean_version):
        updated.append("version_info.txt")

    if update_installer_iss(clean_version):
        updated.append("installer.iss")

    update_changelog(version)

    # Stage updated files
    if updated:
        print()
        stage_updated_files()

    print()
    print("=" * 60)
    print("[SUCCESS] Version files updated")
    print("=" * 60)
    print()
    print(f"Files updated: {', '.join(updated)}")
    print()
    print("[TIP] These files have been staged for commit")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
