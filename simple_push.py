import os
import subprocess

print("=" * 60)
print("HVAC Business Analyst - Auto GitHub Push")
print("=" * 60)

# Check git status
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
status = result.stdout

if not status.strip():
    print("No changes to commit")
else:
    print("Changed files:")
    for line in status.strip().split('\n'):
        print(f"  {line}")

# Add files
print("\nAdding files...")
subprocess.run(["git", "add", "."])

# Commit
import datetime
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
commit_msg = f"Update: {timestamp}"

print(f"Committing with message: {commit_msg}")
result = subprocess.run(["git", "commit", "-m", commit_msg])

if result.returncode == 0:
    print("Commit successful")
    
    # Push
    print("Pushing to GitHub...")
    result = subprocess.run(["git", "push", "origin", "main"])
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("Successfully pushed to GitHub!")
        print("=" * 60)
    else:
        print("Push failed")
else:
    print("Commit failed")
