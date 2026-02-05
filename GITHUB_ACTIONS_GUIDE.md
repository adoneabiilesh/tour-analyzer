# GitHub Actions Setup - Step by Step

## Quick Steps (5 minutes setup, 15 minutes runtime)

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. **Repository name:** `tour-analyzer`
3. **Description:** (optional) "Analyze tour websites and generate comparisons"
4. **Public** or **Private** (both work)
5. Click **"Create repository"**

Copy the repository URL (looks like: `https://github.com/YOURNAME/tour-analyzer`)

---

### Step 2: Initialize Git in Your Project

Open terminal in your project folder:

```bash
# Navigate to website-automation folder
cd website-automation

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with analyzer"

# Add remote (use YOUR repository URL)
git remote add origin https://github.com/YOURNAME/tour-analyzer.git

# Push to GitHub
git push -u origin main
```

If you get an error about "main", try:
```bash
git push -u origin master
```

---

### Step 3: Add Dataset to Repository

**IMPORTANT:** You need to add your dataset file to the repo

```bash
# Copy dataset to website-automation folder
cp ../dataset_crawler-google-places_2026-01-22_05-33-25-536.json .

# Commit and push
git add dataset_crawler-google-places_2026-01-22_05-33-25-536.json
git commit -m "Add dataset"
git push
```

---

### Step 4: Run the Workflow

1. Go to your GitHub repository: `https://github.com/YOURNAME/tour-analyzer`
2. Click **"Actions"** tab at the top
3. You should see **"Analyze Tour Websites"** workflow
4. Click **"Analyze Tour Websites"**
5. Click **"Run workflow"** button (blue button on right)
6. Click **"Run workflow"** in the dropdown

![Run workflow](https://docs.github.com/assets/images/actions-workflow-button.png)

---

### Step 5: Wait for Completion

- **Status:** Yellow dot = running, Green check = complete
- **Time:** ~15 minutes for all 430 companies
- **Progress:** You can click on individual jobs to see live logs

---

### Step 6: Download Results

When complete:

1. Click on the completed workflow run
2. Scroll down to **"Artifacts"** section
3. Download:
   - `final-analysis` (contains merged JSON results)
   - `analysis-summary-csv` (spreadsheet format)

---

## What Happens Behind the Scenes

```
Your GitHub Repo
├── .github/workflows/
│   └── analyze.yml          ← The workflow file
├── analyzer.py               ← Main analyzer
├── dataset_crawler...json    ← Your 430 companies
└── requirements.txt          ← Dependencies

When you click "Run workflow":
  ↓
GitHub spins up 10 virtual machines (Ubuntu)
  ↓
Each VM processes 43 companies in parallel
  ↓
All 10 VMs finish in ~15 minutes
  ↓
Results are merged and uploaded as artifacts
  ↓
You download the results
```

---

## Troubleshooting

### Problem: "Workflow not showing"

**Solution:**
```bash
# Make sure workflow file is in correct location
git add .github/workflows/analyze.yml
git commit -m "Add workflow"
git push

# Refresh GitHub page
```

### Problem: "No artifact uploaded"

**Solution:** Check the workflow logs:
1. Click on the failed job
2. Click "Build" or job name
3. Look for error messages

### Problem: "Dataset file not found"

**Solution:** Make sure you committed the dataset:
```bash
ls -la dataset_crawler-google-places_2026-01-22_05-33-25-536.json
git add dataset_crawler-google-places_2026-01-22_05-33-25-536.json
git commit -m "Add dataset"
git push
```

### Problem: "Out of disk space"

**Solution:** The free tier has 500MB storage. If your dataset is large:
1. Go to repo **Settings** → **Actions** → **General**
2. Scroll to **"Artifact retention"**
3. Change to **1 day** (saves space)

---

## Viewing Results

After download, extract and view:

```bash
# Unzip the artifact
unzip final-analysis.zip

# View results
cat final_analysis.json | head -100

# Or open in Python
import json
with open('final_analysis.json') as f:
    data = json.load(f)
    print(f"Analyzed {len(data)} companies")
    for company in data[:5]:
        print(f"{company['company_name']}: {company['total_score']}/100")
```

---

## Alternative: Run from Command Line

If you prefer CLI:

```bash
# Install GitHub CLI
# https://cli.github.com/

# Login
gh auth login

# Run workflow
gh workflow run "Analyze Tour Websites"

# Watch progress
gh run watch

# Download results (when done)
gh run download
```

---

## Cost

**FREE** - GitHub Actions free tier includes:
- 2,000 minutes/month
- 500MB storage
- This workflow uses ~150 minutes

---

## Next Steps After Analysis

Once you have results:

1. **Sort by score:** Find lowest scoring companies
2. **Extract emails:** Contact the ones with emails
3. **Generate GIFs:** Use `quick_compare.py` for worst 10-20 sites
4. **Sales:** Reach out with before/after comparisons

---

## Need Help?

- GitHub Actions docs: https://docs.github.com/en/actions
- Check workflow logs for errors
- Free tier limits: https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions
