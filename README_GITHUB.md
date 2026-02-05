# Run on GitHub Actions - Complete Guide

## Option 1: Automated Setup (Easiest)

```bash
cd website-automation

# Run setup script
python setup_github.py
```

**Then:**
1. Create repo on GitHub when prompted
2. Paste the repository URL
3. Go to GitHub → Actions tab
4. Click "Run workflow"
5. Wait 15 minutes
6. Download results

---

## Option 2: Manual Setup

### Step 1: Create GitHub Repo

Go to https://github.com/new and create a repository named `tour-analyzer`

### Step 2: Push Code

```bash
cd website-automation

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURNAME/tour-analyzer.git
git push -u origin main
```

### Step 3: Run Workflow

1. Go to https://github.com/YOURNAME/tour-analyzer/actions
2. Click "Analyze Tour Websites"
3. Click "Run workflow" → "Run workflow"
4. Wait 15 minutes

---

## What You Get

After 15 minutes, download:
- `final-analysis.zip` - All company data with scores
- `analysis-summary-csv` - Spreadsheet format

**Each company includes:**
- Company name
- Email (extracted from website)
- Phone number
- Website score (0-100)
- Grade (A+ to F)
- Broken features detected
- Design issues found

---

## Cost

**$0** - Within GitHub Actions free tier

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Workflow not showing | Push `.github/workflows/analyze.yml` file |
| Dataset not found | Copy `dataset_crawler...json` to repo and push |
| Push fails | Check GitHub credentials, try token authentication |
| Out of space | Reduce artifact retention to 1 day in Settings |

---

## Need Help?

Run the setup script and follow prompts:
```bash
python setup_github.py
```
