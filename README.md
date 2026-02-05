# Tour Website Comparison Tool

Screenshots competitor websites and compares them against your premium template - creates GIFs and side-by-side comparisons.

## How It Works

```
1. Screenshots old website (their current site)
2. Temporarily modifies your template with their info
3. Screenshots your template (localhost:3000)
4. Creates GIF and side-by-side comparison
5. Restores your template to original
```

**No full website copies!** Just screenshots/GIFs for comparison.

## Quick Start

```bash
cd website-automation

# 1. Install dependencies
pip install playwright pillow python-slugify
playwright install chromium

# 2. Analyze websites (scores them)
python analyzer.py

# 3. Start your dev server (in another terminal)
cd ../rome-tour-tickets
npm run dev

# 4. Run comparison (back in website-automation)
python quick_compare.py
```

## Output

```
comparisons/
├── vatican-tour/
│   ├── old.png              # Their current website
│   ├── new.png              # Your template with their branding
│   ├── comparison.gif       # Animated before/after
│   └── side-by-side.png     # Static comparison
├── rome-tour-tickets/
│   └── ...
└── comparison_manifest.json # All results
```

## Scoring Criteria

| Feature | Points | Description |
|---------|--------|-------------|
| Online Booking | 10 | Has booking/checkout system |
| Payment | 10 | Accepts payments online |
| Mobile Friendly | 10 | Responsive design |
| Tour Listings | 10 | Shows tour products |
| Pricing | 10 | Prices visible |
| Contact Form | 5 | Can contact via form |
| Live Chat | 5 | Has chat widget |
| Reviews | 5 | Shows testimonials |
| FAQ | 5 | Has FAQ section |
| SSL/HTTPS | 5 | Secure connection |
| Fast Loading | 5 | Loads under 3s |
| Contact Info | 10 | Phone, email, address |

**Max Score: 100 points**
- A+ (90-100): Excellent
- A (80-89): Good
- B (70-79): Average
- C (60-69): Below Average
- D (50-59): Poor
- F (<50): Needs Redesign

## What Gets Customized

Only these files are temporarily modified (then restored):

| File | Changes |
|------|---------|
| `layout.tsx` | Title, meta description |
| `Hero.tsx` | Tagline, subtitle |
| `Footer.tsx` | Company name, phone, email, address |
| `page.tsx` | Section titles |

Products, booking system, admin panel - **all preserved**.

## Individual Scripts

### Just Analyze (get scores)
```bash
python analyzer.py
# Creates: analysis_results.json
```

### Just Screenshot (no template changes)
```bash
python simple_screenshot.py
# Screenshots old sites + your localhost
```

### Full Comparison (modify + screenshot + GIF)
```bash
python quick_compare.py
# Does everything, creates GIFs
```

## Windows Quick Start

Double-click to run:
```
run_comparison.bat
```

## Sample Results

```json
{
  "company_name": "Vatican Tour",
  "url": "http://www.madeinrometours.com/",
  "total_score": 88,
  "grade": "A",
  "has_online_booking": true,
  "has_payment_system": true,
  "extracted_phone": "+39 349 55 08 407",
  "extracted_email": "info@madeinrometours.com"
}
```

## Requirements

- Python 3.9+
- Playwright (`playwright install chromium`)
- Pillow (`pip install pillow`)
- Your template dev server running on localhost:3000

## Notes

- Screenshots capture ~2000px height (above fold + some scroll)
- GIFs loop infinitely with 1.5s per frame
- Side-by-side images are 2580px wide (1280+1280+gap)
- Original template files are always restored after comparison
