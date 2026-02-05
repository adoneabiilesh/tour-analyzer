#!/usr/bin/env python3
"""
Setup script for GitHub Actions deployment
Automates git initialization and pushing to GitHub
"""

import subprocess
import sys
import os
from pathlib import Path


def run_cmd(cmd, description=""):
    """Run shell command and show output"""
    if description:
        print(f"\n>>> {description}")
    print(f"Running: {cmd}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    return result.returncode == 0


def check_git_installed():
    """Check if git is installed"""
    result = subprocess.run("git --version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Git is not installed!")
        print("Download from: https://git-scm.com/downloads")
        return False
    print(f"[OK] Git found: {result.stdout.strip()}")
    return True


def main():
    print("="*70)
    print("GitHub Actions Setup Helper")
    print("="*70)
    
    # Check git
    if not check_git_installed():
        return 1
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"\nCurrent directory: {current_dir}")
    
    # Check if dataset exists
    dataset_path = Path("../dataset_crawler-google-places_2026-01-22_05-33-25-536.json")
    if not dataset_path.exists():
        dataset_path = Path("dataset_crawler-google-places_2026-01-22_05-33-25-536.json")
    
    if dataset_path.exists():
        print(f"[OK] Dataset found at: {dataset_path}")
        # Copy to current directory if needed
        if dataset_path.parent.name != current_dir.name:
            print("Copying dataset to current folder...")
            import shutil
            shutil.copy(dataset_path, ".")
            print("[OK] Dataset copied")
    else:
        print("[!] Dataset not found. Please copy it manually.")
    
    # Initialize git if not already
    if not Path(".git").exists():
        print("\n[1/5] Initializing git repository...")
        if not run_cmd("git init", "Creating git repo"):
            return 1
    else:
        print("\n[1/5] Git repository already exists")
    
    # Add all files
    print("\n[2/5] Adding files to git...")
    run_cmd("git add .", "Adding files")
    
    # Commit
    print("\n[3/5] Committing...")
    run_cmd('git commit -m "Add website analyzer for GitHub Actions"', "Creating commit")
    
    # Check for remote
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "github.com" not in result.stdout:
        print("\n[4/5] Adding GitHub remote...")
        print("\n*** IMPORTANT ***")
        print("Create a repository on GitHub first:")
        print("1. Go to: https://github.com/new")
        print("2. Name it: tour-analyzer")
        print("3. Click 'Create repository'")
        print("\nThen paste the repository URL below:")
        print("(Example: https://github.com/johndoe/tour-analyzer)")
        
        repo_url = input("\nRepository URL: ").strip()
        
        if not repo_url:
            print("No URL provided. Setup incomplete.")
            return 1
        
        if not run_cmd(f"git remote add origin {repo_url}", "Adding remote"):
            return 1
    else:
        print("\n[4/5] GitHub remote already configured")
    
    # Push
    print("\n[5/5] Pushing to GitHub...")
    
    # Try main first, then master
    if not run_cmd("git push -u origin main", "Pushing to main branch"):
        print("Trying 'master' branch...")
        if not run_cmd("git push -u origin master", "Pushing to master branch"):
            print("[!] Push failed. You may need to:")
            print("  1. Check your GitHub credentials")
            print("  2. Try manually: git push -u origin main")
            return 1
    
    # Success
    print("\n" + "="*70)
    print("SUCCESS! Repository pushed to GitHub")
    print("="*70)
    
    # Get remote URL for instructions
    result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
    repo_url = result.stdout.strip()
    
    # Convert SSH to HTTPS URL if needed
    if repo_url.startswith("git@github.com:"):
        repo_url = repo_url.replace("git@github.com:", "https://github.com/")
        repo_url = repo_url.replace(".git", "")
    
    print(f"\nRepository: {repo_url}")
    print(f"Actions URL: {repo_url}/actions")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("\n1. Go to your repository on GitHub")
    print(f"   {repo_url}")
    print("\n2. Click the 'Actions' tab")
    print("\n3. Click 'Analyze Tour Websites'")
    print("\n4. Click 'Run workflow' → 'Run workflow'")
    print("\n5. Wait ~15 minutes for completion")
    print("\n6. Download the 'final-analysis' artifact")
    
    print("\n" + "="*70)
    print("Done! Your analysis will run in the cloud.")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
