#!/usr/bin/env python3
"""
COC Report Generator - Comprehensive Release Script

Fetches latest version from GitHub, auto-increments, updates all files,
creates commits, tags, builds executable and installer, and publishes releases.

Usage:
    python scripts/release.py              # Auto-increment and full release
    python scripts/release.py --patch      # Force patch (x.x.X)
    python scripts/release.py --minor      # Force minor (x.X.0)
    python scripts/release.py --major      # Force major (X.0.0)
    python scripts/release.py --version 1.1.0  # Specific version
    python scripts/release.py --dry-run    # Preview only
    python scripts/release.py --push-only  # Commit and push only (no build/version bump)
    python scripts/release.py --build-only # Build executable only (no git operations)
    python scripts/release.py --skip-push  # Skip git push operations
    python scripts/release.py --skip-build # Skip building executable/installer

Examples:
    python scripts/release.py --dry-run           # Preview changes
    python scripts/release.py --patch             # Quick patch release
    python scripts/release.py --version 1.1.0     # Specific version release
"""

import argparse
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path


class Spinner:
    """Animated spinner for progress indication"""

    def __init__(self, message="Processing..."):
        self.message = message
        self.spinning = False
        self.thread = None

    def spin(self):
        chars = "|/-\\"
        i = 0
        while self.spinning:
            sys.stdout.write(f"\r{self.message} {chars[i % len(chars)]}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        self.spinning = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self, final_message=""):
        self.spinning = False
        if self.thread:
            self.thread.join()
        if final_message:
            sys.stdout.write(f"\r{final_message}\n")
        else:
            sys.stdout.write(f"\r{self.message} Done\n")
        sys.stdout.flush()


def run(cmd, check=True):
    """Execute shell command and return output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        if result.stderr:
            print(f"[ERROR] {result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


def get_python_command():
    """Get the correct Python command to use (venv if available, otherwise system Python)"""
    venv_python = Path(".venv/Scripts/python.exe")
    if venv_python.exists():
        return str(venv_python)
    return "python"


def get_latest_github_tag():
    """Fetch latest version tag from GitHub"""
    try:
        tags = run("gh release list --limit 1", check=False)
        if tags:
            match = re.search(r"v(\d+\.\d+\.\d+)", tags)
            if match:
                return match.group(1)
    except Exception:
        pass

    # Fallback to git tags
    try:
        tags = run("git tag --sort=-v:refname", check=False)
        if tags:
            lines = tags.split("\n")
            for line in lines:
                match = re.search(r"v(\d+\.\d+\.\d+)", line)
                if match:
                    return match.group(1)
    except Exception:
        pass

    return "0.0.0"


def get_current_version():
    """Get current version from version_info.txt"""
    try:
        content = Path("version_info.txt").read_text(encoding="utf-8")
        match = re.search(r"Version:\s*v?(\d+\.\d+\.\d+)", content)
        return match.group(1) if match else "0.0.0"
    except Exception:
        return "0.0.0"


def analyze_commits(last_tag):
    """Analyze commits since last tag to determine version bump and categorize changes"""
    if last_tag == "0.0.0":
        commits = run('git log --pretty=format:"%s"', check=False).split("\n")
    else:
        commits = run(
            f'git log v{last_tag}..HEAD --pretty=format:"%s"', check=False
        ).split("\n")

    commits = [c for c in commits if c.strip()]
    if not commits:
        return "patch", [], [], []

    has_breaking = any("!" in c or "BREAKING" in c.upper() for c in commits)
    has_feat = any(c.lower().startswith("feat") for c in commits)

    bump_type = "major" if has_breaking else ("minor" if has_feat else "patch")

    features = [c for c in commits if c.lower().startswith("feat")]
    fixes = [c for c in commits if c.lower().startswith("fix")]
    other = [
        c
        for c in commits
        if not any(
            c.lower().startswith(x) for x in ["feat", "fix", "chore", "docs", "style"]
        )
    ]

    return bump_type, features, fixes, other


def bump_version(current, bump_type):
    """Increment version number based on bump type"""
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def update_file(file_path, old_ver, new_ver, dry_run=False):
    """Update version in a specific file"""
    if not Path(file_path).exists():
        return False

    content = Path(file_path).read_text(encoding="utf-8")
    original = content

    if file_path.endswith("version_info.txt"):
        content = re.sub(
            r"Version:\s*v?" + re.escape(old_ver),
            f"Version: v{new_ver}",
            content,
        )
    elif file_path.endswith("installer.iss"):
        content = re.sub(
            r"AppVersion=" + re.escape(old_ver), f"AppVersion={new_ver}", content
        )
        content = re.sub(
            r"AppVerName=COC Report Generator v" + re.escape(old_ver),
            f"AppVerName=COC Report Generator v{new_ver}",
            content,
        )
        content = re.sub(
            r"OutputBaseFilename=COC_Report_v" + re.escape(old_ver) + r"_Setup",
            f"OutputBaseFilename=COC_Report_v{new_ver}_Setup",
            content,
        )
    elif file_path.endswith("release_metadata.json"):
        content = re.sub(
            r'"version":\s*"' + re.escape(old_ver) + r'"',
            f'"version": "{new_ver}"',
            content,
        )

    if content != original and not dry_run:
        Path(file_path).write_text(content, encoding="utf-8")
        return True
    return content != original


def generate_notes(version, features, fixes, other):
    """Generate comprehensive release notes"""
    notes = f"""## Release v{version}

**Released:** {datetime.now().strftime('%B %d, %Y')}

"""
    if features:
        notes += "### [FEATURE] New Features\n\n"
        for f in features[:15]:
            clean_msg = re.sub(r"^feat(\([^)]+\))?:\s*", "", f)
            notes += f"- {clean_msg}\n"
        notes += "\n"

    if fixes:
        notes += "### [FIX] Bug Fixes\n\n"
        for f in fixes[:15]:
            clean_msg = re.sub(r"^fix(\([^)]+\))?:\s*", "", f)
            notes += f"- {clean_msg}\n"
        notes += "\n"

    if other:
        notes += "### [OTHER] Other Changes\n\n"
        for o in other[:10]:
            notes += f"- {o}\n"
        notes += "\n"

    notes += f"""---

### [DOWNLOAD] Installation

**Installer:** COC_Report_v{version}_Setup.exe (Recommended)
**Portable:** COC_Report.exe (Standalone)

### [FEATURES] Core Capabilities

- Certificate of Conformance (COC) report generation
- BOM comparison (added/removed/modified components)
- PDF analysis for schematics and assembly drawings
- Interactive GUI questionnaire for change documentation
- Professional Word document reports with company branding
- Debug mode with detailed logging
- File configuration system with persistent storage

### [SYSTEM] Requirements

- Windows 10/11 (64-bit)
- Microsoft Word
- Python 3.12+ (for development)

### [START] Quick Start

1. Download and run installer
2. Launch COC Report Generator
3. Select your BOM and drawing files
4. Complete the questionnaire
5. Generate professional COC report

---
*Built {datetime.now().strftime('%B %d, %Y')}*
"""
    return notes


def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="COC Report Generator Release Script")
    parser.add_argument("--patch", action="store_true", help="Patch increment")
    parser.add_argument("--minor", action="store_true", help="Minor increment")
    parser.add_argument("--major", action="store_true", help="Major increment")
    parser.add_argument("--version", type=str, help="Specific version")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    parser.add_argument("--skip-build", action="store_true", help="Skip building")
    parser.add_argument("--skip-push", action="store_true", help="Skip pushing")
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Only build exe/installer (no version bump or git ops)",
    )
    parser.add_argument(
        "--push-only",
        action="store_true",
        help="Commit and push current changes only (no version bump or build)",
    )
    args = parser.parse_args()

    current = get_current_version()
    new = current

    print("\n" + "=" * 80)
    print(" COC REPORT GENERATOR - RELEASE AUTOMATION ".center(80))
    print("=" * 80 + "\n")

    if args.dry_run:
        print("[DRY RUN] Preview mode - no changes will be made\n")

    if args.build_only:
        print("[BUILD ONLY] Skipping version bump and git operations\n")

    if args.push_only:
        print("[PUSH ONLY] Committing and pushing changes only\n")

    # Step 1: Get latest GitHub tag
    if not args.build_only and not args.push_only:
        print("[1/8] Fetching latest version from GitHub...")
        spinner = Spinner("Checking GitHub releases...")
        spinner.start()
        github_tag = get_latest_github_tag()
        spinner.stop(f"[OK] Latest GitHub: v{github_tag}, Current: v{current}\n")

        # Step 2: Determine new version
        print("[2/8] Determining new version...")
        if args.version:
            new = args.version
            print(f"       [OK] User-specified: v{new}\n")
        else:
            base_version = max(
                [github_tag, current], key=lambda v: list(map(int, v.split(".")))
            )

            if args.major:
                bump_type = "major"
            elif args.minor:
                bump_type = "minor"
            elif args.patch:
                bump_type = "patch"
            else:
                bump_type, _, _, _ = analyze_commits(base_version)

            new = bump_version(base_version, bump_type)
            print(f"       [OK] Auto-detected {bump_type}: v{new}\n")

    # Step 3: Analyze commits
    features, fixes, other = [], [], []
    if not args.build_only and not args.push_only:
        print("[3/8] Analyzing commits...")
        spinner = Spinner("Reading git history...")
        spinner.start()
        _, features, fixes, other = analyze_commits(current)
        total = len(features) + len(fixes) + len(other)
        spinner.stop(
            f"[OK] {total} commits ({len(features)} features, {len(fixes)} fixes)\n"
        )

    # Step 4: Update files
    if not args.build_only and not args.push_only:
        print("[4/8] Updating version files...")
        files = [
            "version_info.txt",
            "installer.iss",
            "release_metadata.json",
        ]
        for f in files:
            if update_file(f, current, new, args.dry_run):
                print(f"       [OK] {f}")
        print()

    # Step 5: Commit
    if args.push_only or (not args.build_only):
        step_num = "[1/2]" if args.push_only else "[5/8]"
        print(f"{step_num} Creating git commit...")
        if not args.dry_run:
            spinner = Spinner("Staging files...")
            spinner.start()
            run("git add -A")
            commit_msg = (
                f"chore: Release v{new}"
                if not args.push_only
                else "chore: Update changes"
            )
            run(f'git commit -m "{commit_msg}"')
            spinner.stop(f"[OK] Committed: {commit_msg}\n")
        else:
            print("       [SKIP] Dry run\n")

    # Step 6: Tag
    if not args.skip_push and not args.build_only and not args.push_only:
        print("[6/8] Creating git tag...")
        if not args.dry_run:
            run(f'git tag -a v{new} -m "Release v{new}"')
            print(f"       [OK] Tagged v{new}\n")
        else:
            print("       [SKIP] Dry run\n")

    # Step 7: Push
    if not args.skip_push and (args.push_only or not args.build_only):
        step_num = "[2/2]" if args.push_only else "[7/8]"
        print(f"{step_num} Pushing to GitHub...")
        if not args.dry_run:
            spinner = Spinner("Pushing branch and tags...")
            spinner.start()
            run("git push origin master", check=False)
            if not args.push_only:
                run("git push --tags", check=False)
            spinner.stop("[OK] Pushed\n")
        else:
            print("       [SKIP] Dry run\n")
    elif args.skip_push:
        print("[7/8] [SKIP] Push disabled\n")

    # Step 8: Build
    if not args.skip_build and not args.push_only:
        step_num = "[1/2]" if args.build_only else "[8/8]"
        print(f"{step_num} Building executable and installer...")
        if not args.dry_run:
            python_cmd = get_python_command()

            # Build executable
            spinner = Spinner("Building executable...")
            spinner.start()
            run(f"{python_cmd} build_exe.py")
            spinner.stop("[OK] Executable built\n")

            # Build installer
            spinner = Spinner("Building installer...")
            spinner.start()
            run(f"{python_cmd} build_installer.py")
            spinner.stop("[OK] Installer built\n")

            # Verify files exist
            exe_path = Path("dist/COC_Report.exe")
            installer_path = Path(f"installer/COC_Report_v{new}_Setup.exe")

            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"       Executable: COC_Report.exe ({size_mb:.2f} MB)")

            if installer_path.exists():
                size_mb = installer_path.stat().st_size / (1024 * 1024)
                print(
                    f"       Installer: COC_Report_v{new}_Setup.exe ({size_mb:.2f} MB)"
                )
            print()
        else:
            print("       [SKIP] Dry run\n")
    elif args.skip_build:
        print("[8/8] [SKIP] Build disabled\n")
    elif args.push_only:
        print("       [SKIP] Push-only mode\n")

    # Step 9: GitHub Release
    if not args.skip_push and not args.build_only and not args.push_only:
        print("[BONUS] Creating GitHub release...")
        if not args.dry_run:
            notes = generate_notes(new, features, fixes, other)
            Path("release_notes.txt").write_text(notes, encoding="utf-8")

            assets = []
            installer = Path(f"installer/COC_Report_v{new}_Setup.exe")
            exe = Path("dist/COC_Report.exe")

            if installer.exists():
                assets.append(f'"{installer}"')
            if exe.exists():
                assets.append(f'"{exe}"')

            try:
                spinner = Spinner("Uploading to GitHub...")
                spinner.start()
                if assets:
                    run(
                        f'gh release create v{new} {" ".join(assets)} --title "COC Report v{new}" --notes-file release_notes.txt'
                    )
                else:
                    run(
                        f'gh release create v{new} --title "COC Report v{new}" --notes-file release_notes.txt'
                    )
                spinner.stop("[OK] Released\n")
                Path("release_notes.txt").unlink()
            except Exception as e:
                spinner.stop(f"[ERROR] GitHub CLI failed: {e}\n")
                print("        Install gh cli: https://cli.github.com/\n")
        else:
            print("       [SKIP] Dry run\n")

    # Summary
    print("=" * 80)
    print(" RELEASE COMPLETE ".center(80))
    print("=" * 80)
    print(f"\nVersion: v{current} -> v{new}")
    if not args.dry_run and not args.build_only and not args.push_only:
        print(f"View: https://github.com/mvdeventer/COCforPCBs/releases/tag/v{new}\n")
    elif args.dry_run:
        print("\n[DRY RUN] No changes were made. Run without --dry-run to execute.\n")

    # Print total build time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    if minutes > 0:
        print(f"Total time: {minutes} min {seconds} sec\n")
    else:
        print(f"Total time: {seconds} sec\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Release aborted\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}\n")
        import traceback

        traceback.print_exc()
        sys.exit(1)
