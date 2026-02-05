"""
Helper script to deploy analyzer to GitHub Actions
"""

import subprocess
import os
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command"""
    print(f">>> {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True


def setup_github_repo():
    """Setup GitHub repository for cloud deployment"""
    
    print("="*70)
    print("GitHub Actions Cloud Deployment Setup")
    print("="*70)
    
    # Check if git is initialized
    if not Path(".git").exists():
        print("\n[1/5] Initializing git repository...")
        run_command("git init")
        run_command("git add .")
        run_command('git commit -m "Initial commit"')
    else:
        print("\n[1/5] Git repository already initialized")
    
    # Check for GitHub remote
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "github.com" not in result.stdout:
        print("\n[2/5] Adding GitHub remote...")
        print("Enter your GitHub repository URL (e.g., https://github.com/username/tour-analyzer)")
        repo_url = input("> ").strip()
        if repo_url:
            run_command(f"git remote add origin {repo_url}")
    else:
        print("\n[2/5] GitHub remote already configured")
    
    # Push code
    print("\n[3/5] Pushing code to GitHub...")
    run_command("git add .")
    run_command('git commit -m "Add analyzer and GitHub Actions workflow" || true')
    run_command("git push -u origin main || git push -u origin master")
    
    print("\n[4/5] Setup complete!")
    print("\n[5/5] Next steps:")
    print("   1. Go to https://github.com/YOUR_USERNAME/YOUR_REPO/actions")
    print("   2. Click 'Analyze Tour Websites'")
    print("   3. Click 'Run workflow'")
    print("   4. Wait 15 minutes")
    print("   5. Download 'final-analysis' artifact")
    
    return True


def estimate_time():
    """Estimate processing time on GitHub Actions"""
    print("\n" + "="*70)
    print("TIME ESTIMATE (GitHub Actions)")
    print("="*70)
    
    companies = 430
    batches = 10
    per_batch = companies // batches
    
    print(f"""
Configuration:
  - Total companies: {companies}
  - Parallel batches: {batches}
  - Companies per batch: {per_batch}
  - Time per batch: ~10-15 minutes
  
Expected Results:
  - All batches run in PARALLEL
  - Total time: ~15 minutes (not 6 hours!)
  - Free tier usage: ~150 minutes (of 2,000/month)
  
Cost: $0 (within free tier)
""")


def create_repo_instructions():
    """Show instructions for creating GitHub repo"""
    print("""
Create a new GitHub repository:

1. Go to https://github.com/new
2. Repository name: tour-analyzer
3. Make it Public or Private
4. Click "Create repository"
5. Copy the repository URL (https://github.com/YOURNAME/tour-analyzer)
6. Run this script again and paste the URL
""")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy to GitHub Actions')
    parser.add_argument('--setup', action='store_true', help='Setup GitHub repository')
    parser.add_argument('--estimate', action='store_true', help='Show time estimates')
    
    args = parser.parse_args()
    
    if args.estimate:
        estimate_time()
    elif args.setup:
        setup_github_repo()
    else:
        print("Usage:")
        print("  python deploy_to_github.py --estimate   # Show time estimates")
        print("  python deploy_to_github.py --setup      # Setup GitHub repo")
        print("\nTo deploy to cloud:")
        print("  1. Create GitHub repo at https://github.com/new")
        print("  2. Run: python deploy_to_github.py --setup")
        print("  3. Go to GitHub Actions tab")
        print("  4. Click 'Run workflow'")
