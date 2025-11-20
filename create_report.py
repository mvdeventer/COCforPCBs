"""
Quick COC Report Generator Launcher
Run this script from the root directory to generate COC reports
Automatically ensures execution in virtual environment

Usage:
    python create_report.py          # Normal mode
    python create_report.py --debug  # Debug mode with detailed logging
    python create_report.py -d       # Debug mode (short form)
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

    print("=" * 60)
    print("VIRTUAL ENVIRONMENT SETUP")
    print("=" * 60)
    print()
    print("[INFO] Virtual environment not found. Creating one now...")
    print()

    # Create venv
    result = subprocess.run(
        [sys.executable, "-m", "venv", ".venv"], cwd=Path(__file__).parent, check=False
    )

    if result.returncode != 0:
        print("[ERROR] Failed to create virtual environment")
        print("Make sure Python is installed correctly")
        return False

    print("[OK] Virtual environment created")
    print()

    # Get venv pip
    if os.name == "nt":
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_pip = venv_dir / "bin" / "pip"

    # Upgrade pip
    print("[INFO] Upgrading pip...")
    subprocess.run([str(venv_pip), "install", "--upgrade", "pip"], check=False)

    # Install requirements
    requirements_file = Path(__file__).parent / "requirements.txt"
    if requirements_file.exists():
        print("[INFO] Installing dependencies from requirements.txt...")
        result = subprocess.run(
            [str(venv_pip), "install", "-r", str(requirements_file)], check=False
        )
        if result.returncode == 0:
            print("[OK] Dependencies installed")
        else:
            print("[WARNING] Some dependencies may not have installed correctly")
    else:
        print("[WARNING] requirements.txt not found")
        print("[INFO] Installing core dependencies...")
        subprocess.run(
            [
                str(venv_pip),
                "install",
                "pandas",
                "openpyxl",
                "PyPDF2",
                "python-docx",
                "PyMuPDF",
                "Pillow",
            ],
            check=False,
        )

    print()
    print("[SUCCESS] Virtual environment setup complete!")
    print()

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
        # Try to set up venv automatically
        if setup_venv():
            venv_python = get_venv_python()
            if not venv_python:
                print("[ERROR] Virtual environment setup failed")
                sys.exit(1)
        else:
            print("[ERROR] Could not create virtual environment")
            print()
            response = input("Continue anyway without venv? (y/N): ")
            if response.lower() != "y":
                sys.exit(1)
            return False

    print("Restarting in virtual environment...")
    print()

    # Re-run this script using venv Python, preserving command-line arguments
    result = subprocess.run(
        [str(venv_python), __file__] + sys.argv[1:], cwd=Path(__file__).parent
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    # Ensure we're in venv
    ensure_venv()

    # Add current directory to path
    sys.path.insert(0, str(Path(__file__).parent))

    # Import and run the main report generator
    from generate_coc_report import main

    print("=" * 60)
    print("COC REPORT GENERATOR")
    print("=" * 60)

    if is_venv_active():
        print("[OK] Running in virtual environment")
    else:
        print("[WARNING] Running in global Python environment")

    # Check for debug mode
    if "--debug" in sys.argv or "-d" in sys.argv:
        print("[DEBUG] Debug mode enabled - detailed logging active")

    print("=" * 60)
    print()

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Report generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
