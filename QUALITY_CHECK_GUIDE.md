# Complete Quality Check Guide

## The Problem

Lighthouse says **A+** but website has:
- ❌ Broken booking buttons
- ❌ Forms that don't submit
- ❌ Horrible mobile layout
- ❌ Missing images
- ❌ JavaScript errors
- ❌ Low contrast text

## The Solution

Use multiple specialized tools:

---

## 🔥 TOP 5 RECOMMENDED TOOLS

### 1. **Pa11y** - Accessibility + Design Issues
```bash
npm install -g pa11y
pa11y https://example.com
```
**Finds:**
- Color contrast issues
- Missing alt text
- Form labels missing
- Heading order wrong
- Touch targets too small

### 2. **Muffet** - Broken Links
```bash
go install github.com/raviqqe/muffet@latest
muffet https://example.com
```
**Finds:**
- 404 links
- Timeout issues
- Redirect chains
- Broken images

### 3. **Playwright** - Functionality Testing
```python
# Check if forms actually work
page.on("console", lambda msg: print(msg.text) if msg.type == "error" else None)
page.click("button[type='submit']")
# Verify success message appears
```
**Finds:**
- JavaScript errors
- Failed API calls
- Broken forms
- Console warnings

### 4. **BackstopJS** - Visual Regression
```bash
npm install -g backstopjs
backstop reference
backstop test
```
**Finds:**
- Layout shifts
- Broken CSS
- Missing elements
- Visual glitches

### 5. **My Advanced Analyzer** - Custom Checks
```bash
python advanced_analyzer.py
```
**Finds:**
- Too many fonts/colors
- Horizontal scroll (mobile)
- Text too small
- Non-responsive elements
- Broken features

---

## 🎯 COMPLETE CHECKLIST FOR TOUR WEBSITES

### Functional Issues
- [ ] All booking buttons work
- [ ] Forms actually submit
- [ ] Payment links not broken
- [ ] No 404 errors on tour pages
- [ ] Images load correctly
- [ ] Calendar widget works
- [ ] Mobile menu opens/closes
- [ ] Search function works

### Design Issues
- [ ] No horizontal scroll on mobile
- [ ] Text readable (12px minimum)
- [ ] Good color contrast
- [ ] Touch targets 44px+
- [ ] Consistent fonts (max 3)
- [ ] Consistent colors (max 5-6)
- [ ] Images not stretched
- [ ] Layout not broken on tablet

### Content Issues
- [ ] All images have alt text
- [ ] Prices clearly visible
- [ ] Contact info correct
- [ ] No placeholder text (Lorem ipsum)
- [ ] Working links to social media
- [ ] Reviews load properly

---

## 📋 RUNNING ALL CHECKS

### Quick Mode (5 minutes)
```bash
cd website-automation

# 1. My custom analyzer
python advanced_analyzer.py --limit 5

# 2. Quality checker
python run_quality_check.py
```

### Complete Mode (15 minutes)
```bash
# 1. Broken links
muffet https://example.com --buffer-size 8192 > broken_links.txt

# 2. Accessibility
pa11y --standard WCAG2AA --reporter json https://example.com > a11y.json

# 3. Performance
npx lighthouse https://example.com --output=json --chrome-flags="--headless"

# 4. Visual regression (if you have reference)
backstop test
```

---

## 📊 INTERPRETING RESULTS

### Critical Issues (Fix Immediately)
| Issue | Tool | Impact |
|-------|------|--------|
| Broken booking form | Playwright | Lost sales |
| 404 payment links | Muffet | Lost sales |
| Console errors | Playwright | Broken functionality |
| Horizontal scroll | Advanced Analyzer | Mobile unusable |

### Warnings (Fix Soon)
| Issue | Tool | Impact |
|-------|------|--------|
| Missing alt text | Pa11y | Accessibility |
| Low contrast | Pa11y | Hard to read |
| Too many fonts | Advanced Analyzer | Looks unprofessional |
| Tiny text | Advanced Analyzer | Hard to read |

### Nice-to-Have
| Issue | Tool | Impact |
|-------|------|--------|
| Image optimization | Lighthouse | Speed |
| Caching headers | Lighthouse | Speed |
| Minification | Lighthouse | Speed |

---

## 🚀 EXAMPLE: TOUR WEBSITE FIXES

### Before: Score 45/100 (D)
- ❌ Booking button links to 404
- ❌ Mobile: horizontal scroll
- ❌ 15 images missing alt text
- ❌ Console: 8 JavaScript errors
- ❌ Pink text on yellow background

### After Fixes: Score 88/100 (A)
- ✅ Booking form fixed
- ✅ Responsive layout
- ✅ All images have alt
- ✅ No console errors
- ✅ Good contrast

---

## 🛠️ ONE-COMMAND SETUP

```bash
# Install all tools at once
npm install -g pa11y backstopjs @sitespeedio/sitespeed.io
pip install playwright beautifulsoup4
playwright install chromium
go install github.com/raviqqe/muffet@latest
```

---

## 📁 OUTPUT FILES

```
website-automation/
├── advanced_analysis.json      ← My custom analyzer results
├── quality_reports.json        ← Quality checker results
├── broken_links.txt            ← Muffet output
├── a11y.json                   ← Pa11y accessibility results
└── backstop_results/           ← Visual regression screenshots
```

---

## 💡 PRO TIPS

1. **Test on mobile viewport**
   ```python
   page.set_viewport_size({'width': 375, 'height': 667})  # iPhone SE
   ```

2. **Check forms thoroughly**
   ```python
   # Fill and submit each form
   await page.fill('input[name="email"]', 'test@test.com')
   await page.click('button[type="submit"]')
   await page.wait_for_selector('.success-message')
   ```

3. **Test booking flow**
   - Select date
   - Choose tour
   - Enter details
   - Check if payment loads

4. **Common tour site issues**
   - Calendar not loading
   - Price calculator broken
   - "Book Now" button does nothing
   - Mobile menu doesn't open
   - Gallery images don't open

---

## 🎯 BOTTOM LINE

| Lighthouse Score | Real Quality |
|-----------------|--------------|
| 95/100 | Could still be broken |
| My Advanced Score | Actually functional |

**Use both:**
- Lighthouse = Performance metrics
- My tools = Real functionality

Run both to catch everything!
