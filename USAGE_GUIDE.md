# Usage Guide - Website Comparison Tool

## What You Get

1. **Scores** for each competitor website (0-100 points)
2. **Screenshots** of their current website
3. **Screenshots** of YOUR template with THEIR branding
4. **GIFs** showing before/after animation
5. **Side-by-side** comparison images

## Step-by-Step

### Step 1: Install (One-time)

```bash
cd website-automation

# Install Python packages
pip install playwright pillow python-slugify

# Install browser
playwright install chromium
```

### Step 2: Analyze Competitors

```bash
python analyzer.py
```

This creates `analysis_results.json` with scores for each website.

### Step 3: Start Your Dev Server

Open a **NEW terminal**:

```bash
cd ../rome-tour-tickets
npm run dev
```

Wait for "Ready on http://localhost:3000"

### Step 4: Run Comparison

Back in website-automation folder:

```bash
python quick_compare.py
```

It will:
1. Take screenshot of competitor's website
2. Temporarily customize your template with their info
3. Screenshot your localhost:3000
4. Create GIF + side-by-side comparison
5. Restore your template

### Step 5: View Results

```
comparisons/
├── company-name/
│   ├── old.png          ← Their current site
│   ├── new.png          ← Your template with their brand
│   ├── comparison.gif   ← Animated before/after
│   └── side-by-side.png ← Static comparison
```

## Alternative: Just Screenshots

If you don't want to modify the template at all:

```bash
python simple_screenshot.py
```

This just screenshots their site + your current localhost (no modifications).

## Tips

- **Screenshots are ~2000px tall** - captures hero + some content
- **GIFs loop forever** - great for presentations
- **Side-by-side is 2580px wide** - good for proposals
- **Scores help prioritize** - focus on low-scoring sites (need redesign most)

## Troubleshooting

### "localhost:3000 refused"
- Make sure `npm run dev` is running in rome-tour-tickets
- Check it's actually on port 3000

### Screenshots are blank
- Website might block headless browsers
- Try increasing timeout in the script

### Template not restoring
- Check if files are read-only
- Originals are backed up in memory - just git checkout if needed

## Data Flow

```
Dataset JSON
     ↓
analyzer.py → Scores + Extracted Info
     ↓
quick_compare.py
     ├── Screenshots old website
     ├── Customizes template (temp)
     ├── Screenshots localhost
     ├── Creates GIF
     └── Restores template
     ↓
comparisons/ folder with assets
```
