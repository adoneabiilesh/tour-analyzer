# Quick Start: Run on GitHub Actions (15 minutes)

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Create GitHub repo | 2 min |
| 2 | Push code | 3 min |
| 3 | Run workflow | 15 min |
| **Total** | | **20 minutes** |

---

## Step-by-Step

### 1. Create Repository (2 minutes)

Go to https://github.com/new
- **Name:** `tour-analyzer`
- **Public/Private:** Your choice
- Click **"Create repository"**

### 2. Push Your Code (3 minutes)

Open terminal in `website-automation` folder:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Add tour website analyzer"

# Add remote (replace YOURNAME with your GitHub username)
git remote add origin https://github.com/YOURNAME/tour-analyzer.git

# Push
git push -u origin main
```

If `main` doesn't work, try `master`:
```bash
git push -u origin master
```

### 3. Copy Dataset

Make sure your dataset is in the repo:

```bash
# Copy dataset to website-automation folder
cp ../dataset_crawler-google-places_2026-01-22_05-33-25-536.json .

# Push it
git add dataset_crawler-google-places_2026-01-22_05-33-25-536.json
git commit -m "Add dataset"
git push
```

### 4. Run Workflow (15 minutes)

1. Go to: `https://github.com/YOURNAME/tour-analyzer/actions`
2. Click **"Analyze Tour Websites"**
3. Click **"Run workflow"** dropdown
4. Click **"Run workflow"** button
5. Wait for green checkmark (~15 minutes)

### 5. Download Results

When done:
1. Click on the completed run
2. Scroll to **Artifacts**
3. Download:
   - `final-analysis` (JSON results)
   - `analysis-summary-csv` (spreadsheet)

---

## What's in the Results?

```json
[
  {
    "company_name": "Vatican Tour",
    "extracted_email": "info@madeinrometours.com",
    "extracted_phone": "+39 349 55 08 407",
    "total_score": 88,
    "grade": "A",
    "url": "http://www.madeinrometours.com/"
  }
]
```

---

## Visual Guide

```
GitHub.com
    |
    v
[Create repo] → Name: tour-analyzer → [Create]
    |
    v
Terminal
    |
    v
git init
git add .
git commit -m "Initial"
git remote add origin https://github.com/YOURNAME/tour-analyzer.git
git push
    |
    v
GitHub.com/tour-analyzer/actions
    |
    v
[Click Actions tab]
[Click "Analyze Tour Websites"]
[Click "Run workflow"]
    |
    v
Wait 15 minutes...
    |
    v
[Download artifacts]
    |
    v
Get results with scores & emails!
```

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Workflow not showing" | Check file at `.github/workflows/analyze.yml` exists |
| "Permission denied" | Check GitHub login, use token if needed |
| "Dataset not found" | Make sure JSON file is committed and pushed |
| "No artifacts" | Check workflow logs for errors |

---

## Automated Setup

Or use the setup script:

```bash
cd website-automation
python setup_github.py
```

Follow prompts to:
1. Create GitHub repo
2. Enter repository URL
3. Push code automatically
4. Get instructions for running workflow

---

## Cost

**$0** - Within GitHub Actions free tier (2,000 minutes/month)

---

## Speed Comparison

| Method | Time for 430 companies |
|--------|------------------------|
| Your laptop (1 core) | 6 hours |
| Your laptop (4 cores) | 1.5 hours |
| **GitHub Actions** | **15 minutes** |

**20x faster!**
