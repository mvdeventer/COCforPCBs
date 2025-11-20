"""
Quick reference guide for version management
Run this script to see current version status
"""

import os
import re
import subprocess
import sys
from pathlib import Path


def is_venv_active():
    """Check if we're running in a virtual environment"""
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def get_venv_python():
    """Get the path to the venv Python executable"""
    venv_dir = Path(__file__).parent / ".venv"

    if os.name == "nt":  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:  # Unix/Linux/Mac
        python_exe = venv_dir / "bin" / "python"

    return python_exe if python_exe.exists() else None


def setup_venv():
    """Set up virtual environment if it doesn't exist"""
    venv_dir = Path(__file__).parent / ".venv"

    if venv_dir.exists():
        return True

    print("[INFO] Creating virtual environment...")
    result = subprocess.run(
        [sys.executable, "-m", "venv", ".venv"], cwd=Path(__file__).parent, check=False
    )

    if result.returncode != 0:
        return False

    if os.name == "nt":
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_pip = venv_dir / "bin" / "pip"

    subprocess.run(
        [str(venv_pip), "install", "--upgrade", "pip"], check=False, capture_output=True
    )

    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        subprocess.run(
            [str(venv_pip), "install", "-r", str(requirements_file)],
            check=False,
            capture_output=True,
        )

    return True


def ensure_venv():
    """Ensure we're running in the virtual environment"""
    if is_venv_active():
        return True

    venv_python = get_venv_python()

    if not venv_python:
        if setup_venv():
            venv_python = get_venv_python()

    if venv_python:
        # Re-run this script using venv Python
        result = subprocess.run(
            [str(venv_python), __file__], cwd=Path(__file__).parent, check=False
        )
        sys.exit(result.returncode)

    # No venv found, continue anyway for version check
    return False


def get_git_tag_version():
    """Get version from git tags"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "No tags found"


def get_version_from_file(filepath, pattern):
    """Extract version from a file using regex"""
    try:
        content = Path(filepath).read_text(encoding="utf-8")
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    except Exception as e:
        return f"Error: {e}"
    return "Not found"


def main():
    print("=" * 70)
    print("VERSION STATUS CHECK")
    print("=" * 70)
    print()

    # Git tag version
    git_version = get_git_tag_version()
    print(f"[GIT] Git Tag Version:        {git_version}")
    print()

    # version_info.txt
    version_info_pattern = r"u'FileVersion', u'([0-9.]+)'"
    version_info = get_version_from_file("version_info.txt", version_info_pattern)
    print(f"[FILE] version_info.txt:       {version_info}")

    # installer.iss
    installer_pattern = r'#define AppVersion "([0-9.]+)"'
    installer_version = get_version_from_file("installer.iss", installer_pattern)
    print(f"[FILE] installer.iss:          {installer_version}")

    print()
    print("=" * 70)

    # Check if all versions match
    git_clean = git_version.lstrip("v")
    all_match = git_clean == version_info == installer_version

    if all_match:
        print("[OK] All versions are in sync!")
    else:
        print("[WARNING] Versions are NOT in sync!")
        print()
        print("To fix this, run:")
        print("  python update_versions.py")

    print("=" * 70)
    print()

    # Show available commands
    print("AVAILABLE COMMANDS:")
    print()
    print("  python update_versions.py")
    print("    └─ Sync all version files to match git tag")
    print()
    print("  python scripts/release.py --auto")
    print("    └─ Create new release (auto-detects version bump)")
    print()
    print("  python scripts/release.py --auto --bump major")
    print("    └─ Force major version bump (e.g., v1.0.0 → v2.0.0)")
    print()
    print("  git commit -m 'feat: new feature'")
    print("    └─ Commit with auto version update (pre-commit hook)")
    print()

    print("For full documentation, see VERSION_MANAGEMENT.md")
    print()


if __name__ == "__main__":
    ensure_venv()
    main()
