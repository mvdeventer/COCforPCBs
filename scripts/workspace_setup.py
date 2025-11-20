"""
Workspace Setup Script
Automatically runs when workspace opens
- Sets up virtual environment
- Installs dependencies
- Updates version files to match git tags
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, capture=False, cwd=None):
    """Run a command and return success status"""
    try:
        if capture:
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=False, cwd=cwd
            )
            return result.returncode == 0, result.stdout
        else:
            result = subprocess.run(cmd, check=False, cwd=cwd)
            return result.returncode == 0, None
    except Exception as e:
        print(f"[ERROR] Command failed: {e}")
        return False, None


def setup_venv():
    """Set up virtual environment if needed"""
    workspace = Path(__file__).parent.parent
    venv_dir = workspace / ".venv"

    print("=" * 60)
    print("WORKSPACE SETUP - Virtual Environment")
    print("=" * 60)
    print()

    if venv_dir.exists():
        print("[OK] Virtual environment already exists at .venv")
        return True

    print("[INFO] Creating virtual environment...")
    success, _ = run_command([sys.executable, "-m", "venv", str(venv_dir)])

    if not success:
        print("[ERROR] Failed to create virtual environment")
        return False

    print("[OK] Virtual environment created")

    # Get venv pip
    if os.name == "nt":
        venv_pip = venv_dir / "Scripts" / "pip.exe"
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_pip = venv_dir / "bin" / "pip"
        venv_python = venv_dir / "bin" / "python"

    # Upgrade pip
    print("[INFO] Upgrading pip...")
    run_command([str(venv_pip), "install", "--upgrade", "pip"], capture=True)

    # Install requirements
    requirements = workspace / "requirements.txt"
    if requirements.exists():
        print("[INFO] Installing dependencies from requirements.txt...")
        success, _ = run_command(
            [str(venv_pip), "install", "-r", str(requirements)], cwd=workspace
        )
        if success:
            print("[OK] Dependencies installed")
        else:
            print("[WARNING] Some dependencies may have failed to install")
    else:
        print("[WARNING] requirements.txt not found")
        print("[INFO] Installing core dependencies...")
        packages = ["pandas", "openpyxl", "PyPDF2", "python-docx", "PyMuPDF", "Pillow"]
        run_command([str(venv_pip), "install"] + packages)

    print()
    return True


def update_version_files():
    """Update version files to match git tags"""
    workspace = Path(__file__).parent.parent

    print("=" * 60)
    print("WORKSPACE SETUP - Version Files")
    print("=" * 60)
    print()

    # Get current git tag
    success, output = run_command(
        ["git", "describe", "--tags", "--abbrev=0"], capture=True, cwd=workspace
    )

    if not success or not output:
        print("[INFO] No git tags found, skipping version update")
        print()
        return True

    version_tag = output.strip()
    version_clean = version_tag.lstrip("v")

    print(f"[INFO] Current git tag: {version_tag}")
    print(f"[INFO] Clean version: {version_clean}")
    print()

    # Update version_info.txt
    version_info_file = workspace / "version_info.txt"
    if version_info_file.exists():
        import re

        content = version_info_file.read_text(encoding="utf-8")

        # Parse version parts
        parts = version_clean.split(".")
        major = parts[0] if len(parts) > 0 else "1"
        minor = parts[1] if len(parts) > 1 else "0"
        patch = parts[2] if len(parts) > 2 else "0"

        # Update version numbers
        content = re.sub(
            r"filevers=\(.*?\)", f"filevers=({major}, {minor}, {patch}, 0)", content
        )
        content = re.sub(
            r"prodvers=\(.*?\)", f"prodvers=({major}, {minor}, {patch}, 0)", content
        )
        content = re.sub(
            r"u'FileVersion', u'.*?'", f"u'FileVersion', u'{version_clean}'", content
        )
        content = re.sub(
            r"u'ProductVersion', u'.*?'",
            f"u'ProductVersion', u'{version_clean}'",
            content,
        )

        version_info_file.write_text(content, encoding="utf-8")
        print(f"[OK] Updated version_info.txt to {version_clean}")

    # Update installer.iss
    installer_file = workspace / "installer.iss"
    if installer_file.exists():
        import re

        content = installer_file.read_text(encoding="utf-8")
        content = re.sub(
            r'#define AppVersion ".*?"',
            f'#define AppVersion "{version_clean}"',
            content,
        )
        installer_file.write_text(content, encoding="utf-8")
        print(f"[OK] Updated installer.iss to {version_clean}")

    print()
    return True


def check_git_config():
    """Verify git configuration"""
    workspace = Path(__file__).parent.parent

    print("=" * 60)
    print("WORKSPACE SETUP - Git Configuration")
    print("=" * 60)
    print()

    # Check if git repo exists
    git_dir = workspace / ".git"
    if not git_dir.exists():
        print("[WARNING] Not a git repository")
        print()
        return False

    # Check remote
    success, output = run_command(
        ["git", "remote", "get-url", "origin"], capture=True, cwd=workspace
    )

    if success and output:
        print(f"[OK] Git remote: {output.strip()}")
    else:
        print("[WARNING] No git remote configured")

    # Check current branch
    success, output = run_command(
        ["git", "branch", "--show-current"], capture=True, cwd=workspace
    )

    if success and output:
        print(f"[OK] Current branch: {output.strip()}")

    print()
    return True


def main():
    """Main setup routine"""
    print()
    print("=" * 60)
    print("COC REPORT GENERATOR - WORKSPACE SETUP")
    print("=" * 60)
    print()

    # Setup venv
    if not setup_venv():
        print("[ERROR] Virtual environment setup failed")
        return 1

    # Check git
    check_git_config()

    # Update version files
    update_version_files()

    print("=" * 60)
    print("[SUCCESS] WORKSPACE SETUP COMPLETE")
    print("=" * 60)
    print()
    print("Ready to use:")
    print("  - Virtual environment: .venv")
    print("  - Run reports: python create_report.py")
    print("  - Build EXE: python build_exe.py")
    print("  - Build installer: python build_installer.py")
    print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INFO] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
