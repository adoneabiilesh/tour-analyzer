# Cloud Deployment Quickstart

## Fastest Option: GitHub Actions (15 minutes for 430 companies)

### Step 1: Create GitHub Repository

```bash
# 1. Go to https://github.com/new
# 2. Name it: tour-analyzer
# 3. Make it Public or Private
# 4. Click "Create repository"
```

### Step 2: Push Your Code

```bash
# In your website-automation folder
git init
git add .
git commit -m "Add tour website analyzer"
git remote add origin https://github.com/YOURNAME/tour-analyzer.git
git push -u origin main
```

### Step 3: Run in Cloud

```bash
# Go to: https://github.com/YOURNAME/tour-analyzer/actions
# Click: "Analyze Tour Websites"
# Click: "Run workflow"
# Wait: 15 minutes
# Download: final-analysis artifact
```

---

## Alternative Options

### Option A: Google Colab (Free, No Setup)

1. Go to https://colab.research.google.com
2. Create new notebook
3. Paste this code:

```python
# Install
!pip install playwright beautifulsoup4 pillow python-slugify
!playwright install chromium

# Upload your dataset
from google.colab import files
uploaded = files.upload()  # Upload dataset_crawler-google-places_2026-01-22_05-33-25-536.json

# Run parallel analysis
!python run_parallel.py

# Download results
files.download('parallel_analysis_results.json')
```

**Time:** 20 minutes  
**Cost:** $0

---

### Option B: AWS Free Tier (More Control)

```bash
# 1. Create EC2 t3.small instance (2 vCPU, 2GB RAM)
# 2. SSH into it
ssh -i key.pem ubuntu@your-instance-ip

# 3. Setup
sudo apt update
sudo apt install python3-pip -y
pip3 install playwright beautifulsoup4 pillow python-slugify
playwright install chromium

# 4. Download your code
git clone https://github.com/YOURNAME/tour-analyzer.git
cd tour-analyzer/website-automation

# 5. Run parallel (uses all CPUs)
python run_parallel.py

# 6. Download results
# Use SCP or upload to S3
```

**Time:** 25 minutes  
**Cost:** $0 (within free tier)

---

### Option C: Local Parallel (If you have 8+ cores)

```bash
python run_parallel.py
```

Automatically detects CPU cores and runs parallel jobs.

**Time:** 1-2 hours (depends on your CPU)  
**Cost:** $0

---

## Speed Comparison

| Method | Time for 430 | Parallel Jobs | Cost |
|--------|--------------|---------------|------|
| Local (1 core) | 6 hours | 1 | $0 |
| Local (4 cores) | 1.5 hours | 4 | $0 |
| GitHub Actions | **15 min** | 20 | **$0** |
| Google Colab | 20 min | 2-4 | $0 |
| AWS Free Tier | 25 min | 2 | $0 |
| Paid VPS ($10) | 30 min | 4 | $10/mo |

---

## Recommendation

**Use GitHub Actions if:**
- You want fastest results (15 min)
- No setup/management needed
- Okay with 2,000 min/month limit

**Use Google Colab if:**
- You want zero setup
- Don't want to create GitHub account
- Can wait 20 minutes

**Use AWS if:**
- You want full control
- Need custom configuration
- Have AWS account already

---

## Results

All methods produce:
- `analysis_results.json` - Full scores and data
- `analysis_summary.csv` - Spreadsheet format
- Extraction of emails, phones, addresses

---

## One-Command Deployment

```bash
# Setup and deploy to GitHub Actions
python deploy_to_github.py --setup
```

Then go to GitHub → Actions → Run workflow.

Done in 15 minutes! 🚀
