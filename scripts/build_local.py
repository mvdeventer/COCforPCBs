"""
Local Build Script for COC Report Generator
Creates standalone EXE and installer locally without GitHub Actions
"""

import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class LocalBuilder:
    def __init__(self):
        self.workspace = Path(__file__).parent.parent
        self.dist_dir = self.workspace / "dist"
        self.build_dir = self.workspace / "build"

    def run_command(self, cmd, shell=True, check=True):
        """Run a shell command"""
        try:
            print(f"→ {cmd}")
            result = subprocess.run(
                cmd,
                shell=shell,
                capture_output=True,
                text=True,
                check=check,
                cwd=self.workspace,
            )
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {e.stderr if e.stderr else str(e)}")
            if check:
                sys.exit(1)
            return None

    def get_version(self):
        """Get version from git tags or use default"""
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=False,
                cwd=self.workspace,
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return version, version.lstrip("v")
            else:
                return "v1.0.0", "1.0.0"
        except Exception:
            return "v1.0.0", "1.0.0"

    def update_version_files(self, version, clean_version):
        """Update version in all build files"""
        print(f"\n📝 Updating version to {version}...")

        # Parse version parts
        parts = clean_version.split(".")
        major = parts[0] if len(parts) > 0 else "1"
        minor = parts[1] if len(parts) > 1 else "0"
        patch = parts[2] if len(parts) > 2 else "0"

        # Update version_info.txt
        version_file = self.workspace / "version_info.txt"
        if version_file.exists():
            content = version_file.read_text(encoding="utf-8")
            content = re.sub(
                r"filevers=\(.*?\)", f"filevers=({major}, {minor}, {patch}, 0)", content
            )
            content = re.sub(
                r"prodvers=\(.*?\)", f"prodvers=({major}, {minor}, {patch}, 0)", content
            )
            content = re.sub(
                r"u'FileVersion', u'.*?'",
                f"u'FileVersion', u'{clean_version}'",
                content,
            )
            content = re.sub(
                r"u'ProductVersion', u'.*?'",
                f"u'ProductVersion', u'{clean_version}'",
                content,
            )
            version_file.write_text(content, encoding="utf-8")
            print(f"  ✓ Updated version_info.txt")

        # Update installer.iss
        installer_file = self.workspace / "installer.iss"
        if installer_file.exists():
            content = installer_file.read_text(encoding="utf-8")
            content = re.sub(
                r'#define AppVersion ".*?"',
                f'#define AppVersion "{clean_version}"',
                content,
            )
            installer_file.write_text(content, encoding="utf-8")
            print(f"  ✓ Updated installer.iss")

    def clean_build_dirs(self):
        """Clean previous build artifacts"""
        print("\n🧹 Cleaning build directories...")

        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"  ✓ Removed {dir_path.name}/")

        # Clean spec cache
        spec_cache = self.workspace / "__pycache__"
        if spec_cache.exists():
            shutil.rmtree(spec_cache)

    def build_exe(self):
        """Build executable with PyInstaller"""
        print("\n🔨 Building executable with PyInstaller...")

        # Check if PyInstaller is installed
        try:
            subprocess.run(
                ["pyinstaller", "--version"], capture_output=True, check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ PyInstaller not found. Installing...")
            self.run_command(f"{sys.executable} -m pip install pyinstaller")

        # Build with spec file
        spec_file = self.workspace / "coc_report.spec"
        if not spec_file.exists():
            print(f"❌ Spec file not found: {spec_file}")
            sys.exit(1)

        self.run_command(f"pyinstaller coc_report.spec --clean --noconfirm")

        # Check result
        exe_path = self.dist_dir / "COC_Report_Generator.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"  ✅ EXE built successfully ({size_mb:.2f} MB)")
            return exe_path
        else:
            print("  ❌ EXE build failed")
            sys.exit(1)

    def build_installer(self, version):
        """Build Windows installer with Inno Setup"""
        print("\n📦 Building installer with Inno Setup...")

        # Check if Inno Setup is installed
        iscc_paths = [
            Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
            Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
            Path(r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"),
            Path(r"C:\Program Files\Inno Setup 5\ISCC.exe"),
        ]

        iscc = None
        for path in iscc_paths:
            if path.exists():
                iscc = path
                break

        if not iscc:
            print("  ⚠️  Inno Setup not found. Skipping installer build.")
            print("  Download from: https://jrsoftware.org/isdl.php")
            return None

        # Build installer
        iss_file = self.workspace / "installer.iss"
        if not iss_file.exists():
            print(f"  ❌ Installer script not found: {iss_file}")
            return None

        self.run_command(f'"{iscc}" installer.iss', check=False)

        # Check result
        clean_version = version.lstrip("v")
        installer_path = (
            self.dist_dir
            / "installer"
            / f"COC_Report_Generator_Setup_{clean_version}.exe"
        )
        if installer_path.exists():
            size_mb = installer_path.stat().st_size / (1024 * 1024)
            print(f"  ✅ Installer built successfully ({size_mb:.2f} MB)")
            return installer_path
        else:
            print("  ⚠️  Installer build failed or not created")
            return None

    def create_checksums(self, exe_path, installer_path, version):
        """Create SHA256 checksums file"""
        print("\n🔐 Creating checksums...")

        import hashlib

        def sha256_file(filepath):
            sha256 = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()

        checksums = []

        # EXE checksum
        exe_hash = sha256_file(exe_path)
        checksums.append(f"{exe_path.name}")
        checksums.append(f"SHA256: {exe_hash}")
        checksums.append("")

        # Installer checksum
        if installer_path and installer_path.exists():
            installer_hash = sha256_file(installer_path)
            checksums.append(f"{installer_path.name}")
            checksums.append(f"SHA256: {installer_hash}")
            checksums.append("")

        # Write checksums file
        checksums_file = self.dist_dir / "checksums.txt"
        checksums_file.write_text("\n".join(checksums), encoding="utf-8")
        print(f"  ✅ Checksums saved to {checksums_file.name}")

        return checksums_file

    def create_release_package(self, version, exe_path, installer_path, checksums_file):
        """Create a release package with all artifacts"""
        print("\n📁 Creating release package...")

        clean_version = version.lstrip("v")
        release_dir = self.dist_dir / f"COC_Report_Generator_{clean_version}"
        release_dir.mkdir(parents=True, exist_ok=True)

        # Copy files to release directory
        shutil.copy2(exe_path, release_dir / exe_path.name)
        print(f"  ✓ Copied {exe_path.name}")

        if installer_path and installer_path.exists():
            shutil.copy2(installer_path, release_dir / installer_path.name)
            print(f"  ✓ Copied {installer_path.name}")

        shutil.copy2(checksums_file, release_dir / checksums_file.name)
        print(f"  ✓ Copied {checksums_file.name}")

        # Copy documentation
        for doc in ["README.md", "CHANGELOG.md", "LICENSE"]:
            doc_path = self.workspace / doc
            if doc_path.exists():
                shutil.copy2(doc_path, release_dir / doc)
                print(f"  ✓ Copied {doc}")

        print(f"\n  ✅ Release package created at: {release_dir}")
        return release_dir

    def run(self):
        """Execute complete build process"""
        print("=" * 60)
        print("🚀 LOCAL BUILD - COC Report Generator")
        print("=" * 60)

        # Get version
        version, clean_version = self.get_version()
        print(f"\n📌 Version: {version}")

        # Update version files
        self.update_version_files(version, clean_version)

        # Clean old builds
        self.clean_build_dirs()

        # Build EXE
        exe_path = self.build_exe()

        # Build installer (optional)
        installer_path = self.build_installer(version)

        # Create checksums
        checksums_file = self.create_checksums(exe_path, installer_path, version)

        # Create release package
        release_dir = self.create_release_package(
            version, exe_path, installer_path, checksums_file
        )

        # Summary
        print("\n" + "=" * 60)
        print("✅ BUILD COMPLETE")
        print("=" * 60)
        print(f"Version: {version}")
        print(f"Release package: {release_dir}")
        print(f"\nFiles:")
        print(f"  • {exe_path.name}")
        if installer_path and installer_path.exists():
            print(f"  • {installer_path.name}")
        print(f"  • {checksums_file.name}")
        print("\n💡 Tip: Run with --auto flag for automated GitHub release")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Build COC Report Generator locally")
    parser.add_argument(
        "--skip-clean", action="store_true", help="Skip cleaning build directories"
    )
    args = parser.parse_args()

    builder = LocalBuilder()

    try:
        if not args.skip_clean:
            builder.run()
        else:
            print("Skipping clean step as requested")
            builder.run()
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Build failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
