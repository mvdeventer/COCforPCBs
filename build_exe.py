"""
Build EXE from Spec File
Ensures execution in virtual environment
Runs PyInstaller with coc_report.spec
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

    print("[OK] Virtual environment created")
    return True


def ensure_venv():
    """Ensure we're running in the virtual environment"""
    if is_venv_active():
        return True

    print("=" * 60)
    print("VIRTUAL ENVIRONMENT CHECK")
    print("=" * 60)
    print()

    venv_python = get_venv_python()

    if not venv_python:
        if setup_venv():
            venv_python = get_venv_python()
        if not venv_python:
            print("[ERROR] Virtual environment setup failed")
            sys.exit(1)

    print("[INFO] Restarting in virtual environment...")
    print()  # Re-run this script using venv Python
    result = subprocess.run(
        [str(venv_python), __file__], cwd=Path(__file__).parent, check=False
    )
    sys.exit(result.returncode)


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller

        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller in venv"""
    print("[INFO] PyInstaller not found, installing...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pyinstaller"], check=False
    )
    return result.returncode == 0


def build_exe():
    """Build EXE using PyInstaller spec file"""
    spec_file = Path(__file__).parent / "coc_report.spec"

    if not spec_file.exists():
        print(f"[ERROR] Spec file not found: {spec_file}")
        return False

    print("=" * 60)
    print("BUILDING EXE WITH PYINSTALLER")
    print("=" * 60)
    print()
    print(f"[FILE] Spec file: {spec_file.name}")
    print(f"[PYTHON] {sys.executable}")
    print(f"[VENV] Virtual env: {is_venv_active()}")
    print()
    print("=" * 60)
    print()

    # Check PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("[ERROR] Failed to install PyInstaller")
            return False

    # Run PyInstaller
    print("[BUILD] Cleaning previous build artifacts...")
    import shutil

    build_dir = Path(__file__).parent / "build"
    dist_dir = Path(__file__).parent / "dist"

    # Clean build directory with error handling
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir, ignore_errors=True)
        except Exception as e:
            print(f"[WARNING] Could not fully clean build directory: {e}")

    # Clean dist directory
    if dist_dir.exists():
        try:
            shutil.rmtree(dist_dir, ignore_errors=True)
        except Exception as e:
            print(f"[WARNING] Could not fully clean dist directory: {e}")

    print("[BUILD] Building EXE...")
    print()

    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(spec_file), "--noconfirm"],
        cwd=Path(__file__).parent,
        check=False,
    )

    if result.returncode == 0:
        exe_path = Path(__file__).parent / "dist" / "COC_Report_Generator.exe"
        if exe_path.exists():
            size = exe_path.stat().st_size / (1024 * 1024)
            print()
            print("=" * 60)
            print("[SUCCESS] BUILD SUCCESSFUL")
            print("=" * 60)
            print()
            print(f"[EXE] Location: {exe_path}")
            print(f"[SIZE] {size:.2f} MB")
            print()
            return True
        else:
            print()
            print("[WARNING] Build completed but EXE not found at expected location")
            return False
    else:
        print()
        print("[ERROR] Build failed")
        return False


if __name__ == "__main__":
    # Ensure we're in venv
    ensure_venv()

    # Build EXE
    success = build_exe()
    sys.exit(0 if success else 1)
