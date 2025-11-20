"""
Build Installer
Ensures execution in virtual environment
Builds EXE then creates installer with Inno Setup
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


def find_inno_setup():
    """Find Inno Setup compiler"""
    possible_paths = [
        Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
        Path(r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"),
        Path(r"C:\Program Files\Inno Setup 5\ISCC.exe"),
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def build_exe():
    """Build EXE first"""
    build_script = Path(__file__).parent / "build_exe.py"

    print("=" * 60)
    print("STEP 1: Building EXE")
    print("=" * 60)
    print()

    result = subprocess.run(
        [sys.executable, str(build_script)], cwd=Path(__file__).parent, check=False
    )

    return result.returncode == 0


def build_installer():
    """Build installer with Inno Setup"""
    iss_file = Path(__file__).parent / "installer.iss"

    if not iss_file.exists():
        print(f"[ERROR] Installer script not found: {iss_file}")
        return False

    print()
    print("=" * 60)
    print("STEP 2: Building Installer")
    print("=" * 60)
    print()

    # Find Inno Setup
    iscc = find_inno_setup()

    if not iscc:
        print("[ERROR] Inno Setup not found")
        print()
        print("Install Inno Setup from: https://jrsoftware.org/isdl.php")
        print("Or install via Chocolatey: choco install innosetup")
        print()
        return False

    print(f"[FILE] Installer script: {iss_file.name}")
    print(f"[TOOL] Inno Setup: {iscc}")
    print()
    print("[BUILD] Building installer...")
    print()

    # Run Inno Setup compiler with verbose output
    result = subprocess.run(
        [str(iscc), "/V9", str(iss_file)], cwd=Path(__file__).parent, check=False
    )

    if result.returncode == 0:
        # Find the installer
        dist_installer = Path(__file__).parent / "dist" / "installer"
        if dist_installer.exists():
            installers = list(dist_installer.glob("*.exe"))
            if installers:
                installer_path = installers[0]
                size = installer_path.stat().st_size / (1024 * 1024)
                print()
                print("=" * 60)
                print("[SUCCESS] BUILD SUCCESSFUL")
                print("=" * 60)
                print()
                print(f"[INSTALLER] Location: {installer_path}")
                print(f"[SIZE] {size:.2f} MB")
                print()
                return True

        print()
        print("[WARNING] Build completed but installer not found at expected location")
        return False
    else:
        print()
        print("[ERROR] Installer build failed")
        return False


if __name__ == "__main__":
    # Ensure we're in venv
    ensure_venv()

    print("=" * 60)
    print("COMPLETE BUILD: EXE + INSTALLER")
    print("=" * 60)
    print()

    # Build EXE first
    if not build_exe():
        print()
        print("[ERROR] EXE build failed, aborting installer build")
        sys.exit(1)

    # Build installer
    success = build_installer()

    if success:
        print()
        print("[SUCCESS] Complete build finished successfully!")
        print()

    sys.exit(0 if success else 1)
