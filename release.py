"""
GitHub Release Script
Automates version detection, commit, tagging, and release to GitHub
Organizes old reports into archive folders
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class GitHubReleaseManager:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.version = None
        self.previous_version = None
        self.changelog = []
        
    def run_command(self, cmd, capture_output=True, check=True):
        """Run a shell command and return output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=check,
                cwd=self.workspace
            )
            return result.stdout.strip() if capture_output else ""
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {e.stderr if e.stderr else str(e)}")
            return None

    def check_git_repo(self):
        """Check if git repository exists, initialize if not"""
        git_dir = self.workspace / ".git"
        if not git_dir.exists():
            print("📁 Initializing git repository...")
            self.run_command("git init")
            print("✅ Git repository initialized")
            return False
        return True

    def get_remote_url(self):
        """Get the GitHub remote URL"""
        remote = self.run_command("git remote get-url origin", check=False)
        return remote if remote else None

    def setup_remote(self):
        """Setup GitHub remote if not configured"""
        remote_url = self.get_remote_url()
        
        if not remote_url:
            print("\n🔗 GitHub Remote Setup")
            print("=" * 60)
            print("Please provide your GitHub repository information:")
            username = input("GitHub username: ").strip().replace('@', '')
            repo_name = input("Repository name: ").strip()
            
            if not username or not repo_name:
                print("❌ Username and repository name are required")
                return False
            
            remote_url = f"https://github.com/{username}/{repo_name}.git"
            
            # Remove existing origin if it exists with wrong URL
            self.run_command("git remote remove origin", check=False)
            
            self.run_command(f'git remote add origin "{remote_url}"')
            print(f"✅ Remote added: {remote_url}")
        else:
            print(f"✅ Remote configured: {remote_url}")
        
        return True

    def get_latest_tag(self):
        """Get the latest version tag from git"""
        tags = self.run_command("git tag --sort=-v:refname", check=False)
        if tags:
            latest = tags.split('\n')[0]
            print(f"📌 Latest tag: {latest}")
            return latest
        print("📌 No existing tags found")
        return None

    def parse_version(self, version_str):
        """Parse version string (e.g., 'v1.2.3' -> [1, 2, 3])"""
        if not version_str:
            return [0, 0, 0]
        
        match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', version_str)
        if match:
            return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
        return [0, 0, 0]

    def increment_version(self, version_str, bump_type='patch'):
        """Increment version number (major.minor.patch)"""
        major, minor, patch = self.parse_version(version_str)
        
        if bump_type == 'major':
            major += 1
            minor = 0
            patch = 0
        elif bump_type == 'minor':
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        return f"v{major}.{minor}.{patch}"

    def get_new_version(self):
        """Determine new version number"""
        latest_tag = self.get_latest_tag()
        
        print("\n📊 Version Selection")
        print("=" * 60)
        if latest_tag:
            print(f"Current version: {latest_tag}")
            print("\nVersion bump options:")
            print(f"  1. Patch  : {self.increment_version(latest_tag, 'patch')} (bug fixes)")
            print(f"  2. Minor  : {self.increment_version(latest_tag, 'minor')} (new features)")
            print(f"  3. Major  : {self.increment_version(latest_tag, 'major')} (breaking changes)")
            print(f"  4. Custom : Enter your own version")
        else:
            print("No previous version found. Starting fresh.")
            print("\nVersion options:")
            print("  1. Start with v1.0.0")
            print("  2. Custom version")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if latest_tag:
            if choice == '1':
                return self.increment_version(latest_tag, 'patch')
            elif choice == '2':
                return self.increment_version(latest_tag, 'minor')
            elif choice == '3':
                return self.increment_version(latest_tag, 'major')
            elif choice == '4':
                custom = input("Enter version (e.g., v1.2.3): ").strip()
                if not custom.startswith('v'):
                    custom = 'v' + custom
                return custom
            else:
                return self.increment_version(latest_tag, 'patch')
        else:
            if choice == '1':
                return "v1.0.0"
            else:
                custom = input("Enter version (e.g., v1.0.0): ").strip()
                if not custom.startswith('v'):
                    custom = 'v' + custom
                return custom

    def archive_old_reports(self):
        """Move old COC reports to archive folder"""
        print("\n📦 Archiving Old Reports")
        print("=" * 60)
        
        archive_dir = self.workspace / "reports_archive"
        archive_dir.mkdir(exist_ok=True)
        
        # Find all COC report files
        report_files = list(self.workspace.glob("COC_Report_*.docx"))
        
        if not report_files:
            print("No reports found to archive")
            return 0
        
        archived_count = 0
        skipped_count = 0
        
        for report in report_files:
            try:
                # Extract timestamp from filename
                match = re.search(r'(\d{8})_(\d{6})', report.name)
                if match:
                    date_str = match.group(1)  # YYYYMMDD
                    year = date_str[:4]
                    month = date_str[4:6]
                    
                    # Create year/month folder structure
                    dest_dir = archive_dir / year / month
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    
                    dest_path = dest_dir / report.name
                    report.rename(dest_path)
                    print(f"  ✓ Archived: {report.name} → {year}/{month}/")
                    archived_count += 1
                else:
                    # No timestamp, just move to archive root
                    dest_path = archive_dir / report.name
                    report.rename(dest_path)
                    print(f"  ✓ Archived: {report.name}")
                    archived_count += 1
            except PermissionError:
                print(f"  ⚠ Skipped (file in use): {report.name}")
                skipped_count += 1
            except Exception as e:
                print(f"  ⚠ Error archiving {report.name}: {e}")
                skipped_count += 1
        
        if archived_count > 0:
            print(f"✅ Archived {archived_count} report(s)")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} report(s) (close Word documents and try again)")
        
        return archived_count

    def get_git_status(self):
        """Get current git status"""
        status = self.run_command("git status --porcelain")
        return status

    def collect_changelog(self):
        """Collect changelog information from user"""
        print("\n📝 Changelog")
        print("=" * 60)
        print("Enter changes for this release (one per line, empty line to finish):")
        
        changes = []
        while True:
            line = input("  • ").strip()
            if not line:
                break
            changes.append(line)
        
        if not changes:
            changes = ["General improvements and bug fixes"]
        
        self.changelog = changes
        return changes

    def generate_release_notes(self):
        """Generate release notes"""
        notes = f"# Release {self.version}\n\n"
        notes += f"**Release Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        if self.previous_version:
            notes += f"**Previous Version**: {self.previous_version}\n\n"
        
        notes += "## Changes\n\n"
        for change in self.changelog:
            notes += f"- {change}\n"
        
        notes += "\n## Features\n\n"
        notes += "- Auto-detection of product and versions from BOM filenames\n"
        notes += "- BOM comparison (added/removed/modified components)\n"
        notes += "- PDF analysis for schematics and assembly drawings\n"
        notes += "- Interactive GUI questionnaire for change documentation\n"
        notes += "- Professional Word document reports with company branding\n"
        
        return notes

    def commit_changes(self):
        """Commit all changes"""
        print("\n💾 Committing Changes")
        print("=" * 60)
        
        status = self.get_git_status()
        if not status:
            print("⚠️  No changes to commit")
            return False
        
        print("Changes to commit:")
        print(status)
        
        # Add all changes
        self.run_command("git add .")
        
        # Get commit message
        print("\nCommit message:")
        commit_msg = input(f"  [{self.version}] ").strip()
        if not commit_msg:
            commit_msg = f"{self.version} - " + ", ".join(self.changelog[:3])
        else:
            commit_msg = f"{self.version} - {commit_msg}"
        
        # Commit
        result = self.run_command(f'git commit -m "{commit_msg}"')
        if result is not None:
            print(f"✅ Changes committed: {commit_msg}")
            return True
        
        return False

    def create_tag(self):
        """Create annotated git tag"""
        print("\n🏷️  Creating Tag")
        print("=" * 60)
        
        tag_message = f"Release {self.version}\n\n" + "\n".join(f"- {c}" for c in self.changelog)
        
        result = self.run_command(f'git tag -a {self.version} -m "{tag_message}"')
        if result is not None:
            print(f"✅ Tag created: {self.version}")
            return True
        
        return False

    def push_to_github(self):
        """Push commits and tags to GitHub"""
        print("\n🚀 Pushing to GitHub")
        print("=" * 60)
        
        # Check if remote exists
        if not self.get_remote_url():
            print("❌ No remote configured")
            return False
        
        # Push commits
        print("Pushing commits...")
        result = self.run_command("git push origin master", check=False)
        if result is None:
            # Try main branch
            print("Trying main branch...")
            result = self.run_command("git push origin main", check=False)
            if result is None:
                print("⚠️  Push failed. You may need to authenticate or set upstream branch.")
                print("   Try: git push -u origin master")
                return False
        
        print("✅ Commits pushed")
        
        # Push tags
        print("Pushing tags...")
        result = self.run_command("git push --tags", check=False)
        if result is not None:
            print("✅ Tags pushed")
        else:
            print("⚠️  Tag push failed")
        
        return True

    def create_github_release(self):
        """Create GitHub release using gh CLI"""
        print("\n🎉 Creating GitHub Release")
        print("=" * 60)
        
        # Check if gh CLI is installed
        gh_check = self.run_command("gh --version", check=False)
        if gh_check is None:
            print("⚠️  GitHub CLI (gh) not installed")
            print("   Install from: https://cli.github.com/")
            print("   Release tag created, but GitHub release not created")
            return False
        
        print(f"GitHub CLI version: {gh_check.split()[2]}")
        
        # Generate release notes
        notes = self.generate_release_notes()
        
        # Save notes to temp file
        notes_file = self.workspace / "release_notes.md"
        notes_file.write_text(notes, encoding='utf-8')
        
        # Create release
        cmd = f'gh release create {self.version} --title "Release {self.version}" --notes-file release_notes.md'
        result = self.run_command(cmd, check=False)
        
        # Clean up
        notes_file.unlink()
        
        if result is not None:
            print(f"✅ GitHub release created: {self.version}")
            return True
        else:
            print("⚠️  GitHub release creation failed")
            print("   You may need to authenticate: gh auth login")
            return False

    def save_release_metadata(self):
        """Save release metadata to JSON file"""
        metadata_file = self.workspace / "release_metadata.json"
        
        metadata = {
            "version": self.version,
            "previous_version": self.previous_version,
            "release_date": datetime.now().isoformat(),
            "changelog": self.changelog,
        }
        
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        print(f"✅ Release metadata saved to {metadata_file.name}")

    def run_release_process(self):
        """Execute complete release process"""
        print("\n" + "=" * 60)
        print("🚀 GITHUB RELEASE MANAGER")
        print("=" * 60)
        
        # Step 1: Check git repo
        repo_exists = self.check_git_repo()
        
        # Step 2: Setup remote if needed
        if not self.setup_remote():
            print("❌ Release cancelled")
            return
        
        # Step 3: Archive old reports
        self.archive_old_reports()
        
        # Step 4: Get version information
        self.previous_version = self.get_latest_tag()
        self.version = self.get_new_version()
        
        print(f"\n🎯 Target version: {self.version}")
        
        # Step 5: Collect changelog
        self.collect_changelog()
        
        # Step 6: Show summary and confirm
        print("\n" + "=" * 60)
        print("📋 RELEASE SUMMARY")
        print("=" * 60)
        print(f"Version: {self.version}")
        if self.previous_version:
            print(f"Previous: {self.previous_version}")
        print(f"\nChanges:")
        for change in self.changelog:
            print(f"  • {change}")
        
        confirm = input("\n✓ Proceed with release? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Release cancelled")
            return
        
        # Step 7: Commit changes
        committed = self.commit_changes()
        
        # Step 8: Create tag
        if committed or self.get_git_status():
            self.create_tag()
        
        # Step 9: Save metadata
        self.save_release_metadata()
        
        # Step 10: Push to GitHub
        pushed = self.push_to_github()
        
        # Step 11: Create GitHub release (if gh CLI available)
        if pushed:
            self.create_github_release()
        
        print("\n" + "=" * 60)
        print("✅ RELEASE PROCESS COMPLETE")
        print("=" * 60)
        print(f"Version {self.version} released successfully!")
        
        remote_url = self.get_remote_url()
        if remote_url:
            repo_path = remote_url.replace('.git', '').replace('https://github.com/', '')
            print(f"\n🔗 View release: https://github.com/{repo_path}/releases/tag/{self.version}")


def main():
    workspace = Path(__file__).parent
    manager = GitHubReleaseManager(workspace)
    
    try:
        manager.run_release_process()
    except KeyboardInterrupt:
        print("\n\n❌ Release cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
