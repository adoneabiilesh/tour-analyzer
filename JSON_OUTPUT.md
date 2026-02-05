# JSON Output Structure

## 1. Analysis Results (`analysis_results.json`)

Created by: `analyzer.py`

```json
[
  {
    "url": "https://rometourtickets.com/",
    "company_name": "Rome Tour Tickets",
    "extracted_email": "support@rometourtickets.com",
    "extracted_phone": "+39 06 275 7630",
    "extracted_address": "Via della Condotta, 12, Florence, Italy",
    "extracted_description": "Great Experience...",
    "total_score": 100,
    "grade": "A+",
    "has_online_booking": true,
    "has_payment_system": true,
    ...
  }
]
```

**Key Fields:**
- `extracted_email` - Email found on website
- `extracted_phone` - Phone number found
- `extracted_address` - Address found
- `extracted_description` - Tagline/description extracted
- `total_score` - 0-100 score
- `grade` - A+, A, B, C, D, or F

---

## 2. Comparison Results (`comparisons/comparison_results.json`)

Created by: `quick_compare.py`

```json
{
  "generated_at": "2024-02-05T10:30:00",
  "total_companies": 3,
  "companies": [
    {
      "company": "Vatican Tour",
      "email": "info@madeinrometours.com",
      "phone": "+39 349 55 08 407",
      "address": "Via Plauto 17 A, 00193 Rome",
      "original_score": 88,
      "grade": "A",
      "original_url": "http://www.madeinrometours.com/",
      "old": "comparisons/vatican-tour/old.png",
      "new": "comparisons/vatican-tour/new.png",
      "gif": "comparisons/vatican-tour/comparison.gif",
      "side_by_side": "comparisons/vatican-tour/side-by-side.png",
      "folder": "comparisons/vatican-tour"
    }
  ]
}
```

**Key Fields:**
- `email` - Company email (from analysis)
- `phone` - Company phone
- `address` - Company address
- `original_score` - Website score
- `grade` - Letter grade
- `gif` - Path to animated GIF
- `side_by_side` - Path to comparison image
- `old` - Path to old website screenshot
- `new` - Path to new design screenshot

---

## 3. Summary CSV-JSON (`comparisons/comparison_summary.json`)

Simplified format for importing to spreadsheet:

```json
[
  {
    "company_name": "Vatican Tour",
    "email": "info@madeinrometours.com",
    "phone": "+39 349 55 08 407",
    "website": "http://www.madeinrometours.com/",
    "score": 88,
    "grade": "A",
    "gif_path": "comparisons/vatican-tour/comparison.gif",
    "comparison_image": "comparisons/vatican-tour/side-by-side.png"
  }
]
```

---

## 4. Screenshot Manifest (`comparisons/screenshot_manifest.json`)

Created by: `simple_screenshot.py`

```json
[
  {
    "company_name": "Vatican Tour",
    "website": "http://www.madeinrometours.com/",
    "folder": "comparisons/vatican-tour",
    "gif": "comparisons/vatican-tour/animated.gif",
    "comparison": "comparisons/vatican-tour/comparison.png",
    "old_screenshot": "comparisons/vatican-tour/current.png",
    "new_screenshot": "comparisons/vatican-tour/new_design.png"
  }
]
```

---

## File Organization

```
website-automation/
├── analysis_results.json              ← Scores + emails + contact info
├── comparisons/
│   ├── comparison_results.json        ← Full data with GIF paths
│   ├── comparison_summary.json        ← Simple format for spreadsheets
│   ├── screenshot_manifest.json       ← If using simple_screenshot.py
│   ├── vatican-tour/
│   │   ├── old.png
│   │   ├── new.png
│   │   ├── comparison.gif            ← THE GIF
│   │   └── side-by-side.png
│   └── ...
```

---

## Quick Access

**Get all emails:**
```python
import json
with open('analysis_results.json') as f:
    data = json.load(f)
    
emails = [c['extracted_email'] for c in data if c.get('extracted_email')]
print(emails)
```

**Get all GIF paths:**
```python
import json
with open('comparisons/comparison_results.json') as f:
    data = json.load(f)
    
for c in data['companies']:
    print(f"{c['company']}: {c['gif']}")
```

**Filter by score:**
```python
# Get only companies with score < 70 (need redesign)
needs_redesign = [c for c in data['companies'] if c['original_score'] < 70]
```
