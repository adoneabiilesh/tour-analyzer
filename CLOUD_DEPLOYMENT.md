# Deploy to Cloud (Free Tiers) - Run 10x Faster

## Overview

Instead of running 430 companies in 6 hours locally, use cloud free tiers to run **parallel processing** and finish in **30-45 minutes**.

---

## Option 1: GitHub Actions (RECOMMENDED - Completely Free)

### Limits
- **Free tier:** 2,000 minutes/month (Linux)
- **Parallel jobs:** 20 concurrent
- **Max runtime:** 6 hours per job

### Setup

**1. Create `.github/workflows/analyze.yml`** in your repo:

```yaml
name: Analyze Tour Websites

on:
  workflow_dispatch:  # Manual trigger
  # Or scheduled: cron: '0 0 * * 0'  # Weekly

jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        # Split into 10 parallel jobs (43 companies each)
        batch: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      fail-fast: false
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install playwright beautifulsoup4 pillow python-slugify
          playwright install chromium
      
      - name: Run analysis batch
        run: |
          python website-automation/analyzer.py \
            --start ${{ matrix.batch * 43 }} \
            --limit 43
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: analysis-batch-${{ matrix.batch }}
          path: analysis_results_batch_${{ matrix.batch }}.json
```

**2. Results:**
- 10 jobs run in parallel
- Each job: ~15 minutes
- **Total time: 15 minutes** (vs 6 hours locally)

---

## Option 2: Google Colab (Free GPU/CPU)

### Limits
- **Free tier:** 12 hours continuous runtime
- **GPU:** Tesla T4 (optional, not needed for this)
- **Storage:** 35 GB drive

### Notebook Setup

**1. Create Colab notebook:**

```python
# Cell 1: Install
!pip install playwright beautifulsoup4 pillow python-slugify
!playwright install chromium

# Cell 2: Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Cell 3: Upload your dataset
# Upload: dataset_crawler-google-places_2026-01-22_05-33-25-536.json

# Cell 4: Run analysis with parallel processing
import asyncio
from multiprocessing import Pool

# Split into chunks
def process_chunk(chunk_id):
    start = chunk_id * 43
    limit = 43
    # Run analyzer for this chunk
    !python analyzer.py --start {start} --limit {limit}

# Run 10 processes in parallel
with Pool(10) as p:
    p.map(process_chunk, range(10))

# Cell 5: Download results
from google.colab import files
files.download('analysis_results.json')
```

**Time:** ~20 minutes for all 430

---

## Option 3: AWS Free Tier (12 Months Free)

### Limits
- **EC2:** 750 hours/month of t2.micro (1 vCPU, 1GB RAM)
- **S3:** 5GB storage
- **Lambda:** 1M requests free

### Setup: EC2 Instance

**1. Launch t3.small (2 vCPU, 2GB RAM)**
```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Setup
sudo apt update
sudo apt install python3-pip -y
pip3 install playwright beautifulsoup4 pillow python-slugify
playwright install chromium

# Download your code
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo/website-automation

# Run with GNU Parallel
sudo apt install parallel -y

# Split into 10 parallel jobs
seq 0 9 | parallel -j 10 python3 analyzer.py --batch {} --total-batches 10

# Results uploaded to S3
aws s3 cp analysis_results.json s3://your-bucket/
```

**Cost:** FREE (within free tier)
**Time:** ~25 minutes

---

## Option 4: Vercel Serverless Functions

### Limits
- **Free tier:** 100GB bandwidth, 10s max execution
- **Hobby:** 1,000GB bandwidth, 60s max execution

**Use for:** Individual company analysis via API

```javascript
// api/analyze.js
export default async function handler(req, res) {
  const { url } = req.query;
  
  // Run playwright analysis
  const result = await analyzeWebsite(url);
  
  res.json(result);
}
```

**Call 430 URLs in parallel:**
```bash
curl "https://your-app.vercel.app/api/analyze?url=https://example1.com" &
curl "https://your-app.vercel.app/api/analyze?url=https://example2.com" &
# ... 430 times
```

**Time:** ~5 minutes (but limited by 60s timeout per request)

---

## Option 5: Railway/Render (Easy Deployment)

### Railway
- **Free tier:** $5 credit/month (~500 hours)
- **Deploy:** GitHub repo directly
- **Scale:** Up to 8 concurrent workers

### Render
- **Free tier:** 750 hours/month
- **Background workers:** Available
- **Deploy:** Docker or native

---

## Performance Comparison

| Platform | Free Tier | Parallel Jobs | Time for 430 | Setup Difficulty |
|----------|-----------|---------------|--------------|------------------|
| **Local** | Always | 1 | 6 hours | Easy |
| **GitHub Actions** | 2,000 min/mo | 20 | **15 min** | Easy |
| **Google Colab** | 12 hours/day | 2-4 | 20 min | Medium |
| **AWS EC2** | 750 hrs/mo | 2-4 | 25 min | Hard |
| **Vercel** | 100GB/mo | Unlimited | 5 min* | Easy |
| **Railway** | $5 credit | 8 | 30 min | Easy |

*Vercel has 60s timeout limit

---

## Recommended: GitHub Actions

### Why?
1. **Zero cost** - 2,000 minutes/month is plenty
2. **20 parallel jobs** - Finish in 15 minutes
3. **No setup** - Just push code
4. **Artifacts** - Results automatically saved
5. **Scheduled runs** - Run weekly automatically

### Step-by-Step

**1. Create repository:**
```bash
mkdir tour-analyzer
cd tour-analyzer
git init
```

**2. Push your code:**
```bash
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/tour-analyzer.git
git push -u origin main
```

**3. Create workflow file:**
```bash
mkdir -p .github/workflows
cat > .github/workflows/analyze.yml << 'EOF'
name: Analyze Websites

on:
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        batch: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - run: pip install playwright beautifulsoup4 pillow python-slugify
      - run: playwright install chromium
      
      - run: python analyzer.py --batch ${{ matrix.batch }} --total-batches 10
      
      - uses: actions/upload-artifact@v3
        with:
          name: results-batch-${{ matrix.batch }}
          path: results/batch_${{ matrix.batch }}.json
EOF
```

**4. Run:**
- Go to GitHub → Actions → Analyze Websites
- Click "Run workflow"
- Wait 15 minutes
- Download all artifacts

---

## Merging Results from Parallel Jobs

After GitHub Actions completes:

```python
import json
import glob

# Download all artifacts into artifacts/ folder
results = []
for file in glob.glob("artifacts/batch_*.json"):
    with open(file) as f:
        results.extend(json.load(f))

# Save combined
with open("final_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Combined {len(results)} companies")
```

---

## Cost Comparison (430 Companies)

| Method | Cost | Time | Effort |
|--------|------|------|--------|
| Local laptop | $0 | 6 hours | None |
| GitHub Actions | **$0** | **15 min** | Low |
| AWS EC2 (free tier) | $0 | 25 min | Medium |
| AWS EC2 (paid) | ~$0.50 | 25 min | Medium |
| Google Cloud Run | ~$1 | 20 min | Medium |
| Paid VPS ($5/mo) | $5 | 1 hour | Low |

---

## Quick Start: GitHub Actions

```bash
# 1. Fork/create repo
# 2. Add your code
# 3. Create .github/workflows/analyze.yml
# 4. Push
# 5. Go to Actions tab → Run workflow
# 6. Download results in 15 minutes
```

**Result:** Your laptop stays free, job runs in cloud, done in 15 minutes instead of 6 hours!
