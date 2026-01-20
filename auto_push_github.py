#!/usr/bin/env python3
"""
HVAC Business Analyst Skill - Auto Push to GitHub
Automatically commits and pushes changes to GitHub
"""

import os
import sys
import subprocess
from datetime import datetime

def run_git_command(command):
    """Run git command and return result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def get_git_status():
    """Get git status"""
    success, stdout, stderr = run_git_command("git status --porcelain")
    if not success:
        return False, stderr
    return True, stdout

def get_branch_name():
    """Get current branch name"""
    success, stdout, stderr = run_git_command("git rev-parse --abbrev-ref HEAD")
    if success:
        return stdout.strip()
    return "main"

def add_files():
    """Add all files to git"""
    success, stdout, stderr = run_git_command("git add .")
    return success, stderr

def commit_changes(message):
    """Commit changes"""
    success, stdout, stderr = run_git_command(f'git commit -m "{message}"')
    return success, stderr

def push_to_github():
    """Push to GitHub"""
    branch = get_branch_name()
    success, stdout, stderr = run_git_command(f"git push origin {branch}")
    return success, stderr

def create_commit_message():
    """Create commit message based on changes"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"Auto-update: {timestamp}"

def main():
    """Main function"""
    print("=" * 60)
    print("HVAC Business Analyst - Auto GitHub Push")
    print("=" * 60)

    # Check git repository
    if not os.path.exists(".git"):
        print("❌ Not a git repository")
        return False

    # Get git status
    success, status = get_git_status()
    if not success:
        print(f"❌ Failed to get git status: {status}")
        return False

    if not status.strip():
        print("✅ No changes to commit")
        return True

    # Show changed files
    print("\n📝 Changed files:")
    for line in status.strip().split('\n'):
        print(f"  {line}")

    # Get commit message
    commit_msg = create_commit_message()
    print(f"\n💬 Commit message: {commit_msg}")

    # Add files
    print("\n📤 Adding files...")
    success, error = add_files()
    if not success:
        print(f"❌ Failed to add files: {error}")
        return False

    # Commit changes
    print("\n💾 Committing changes...")
    success, error = commit_changes(commit_msg)
    if not success:
        print(f"❌ Failed to commit: {error}")
        return False

    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    success, error = push_to_github()
    if not success:
        print(f"❌ Failed to push: {error}")
        return False

    print("\n" + "=" * 60)
    print("✅ Successfully pushed to GitHub!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
