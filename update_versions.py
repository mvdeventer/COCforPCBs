"""
Update Version Files
Standalone script to manually update all version files to match current git tag
Can be run before commits to ensure consistency
"""

import os
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

    # No venv found, continue anyway for version update
    return False


# Ensure we're in venv
ensure_venv()

# Add scripts directory to path
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

try:
    from update_version_files import main

    print(
        "This will update version_info.txt and installer.iss to match the current git tag"
    )
    print()

    sys.exit(main())
except Exception as e:
    print(f"[ERROR] {e}")
    sys.exit(1)
