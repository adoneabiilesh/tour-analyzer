# Open Source Tools for Broken Features & Design Quality

## The Problem with Lighthouse
- **Lighthouse checks:** Performance, SEO, Best Practices, Accessibility
- **Lighthouse misses:** Broken links, console errors, design quality, UX issues

---

## 🔧 1. BROKEN FEATURE DETECTORS

### A. Link & Resource Checkers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **Link Checker** | https://github.com/linkchecker/linkchecker | Broken links, 404s |
| **Broken Link Checker** | https://github.com/stevenvachon/broken-link-checker | Dead links, redirects |
| **htmltest** | https://github.com/wjdp/htmltest | Bad links, images, scripts |
| ** muffet** | https://github.com/raviqqe/muffet | Fast broken link checker |

**Install & Use:**
```bash
# Link Checker (Python)
pip install linkchecker
linkchecker https://example.com

# muffet (Go - fastest)
go install github.com/raviqqe/muffet@latest
muffet https://example.com
```

### B. Form & Functionality Testers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **Playwright** | https://github.com/microsoft/playwright | Broken forms, buttons |
| **Selenium** | https://github.com/SeleniumHQ/selenium | Functional testing |
| **Cypress** | https://github.com/cypress-io/cypress | E2E testing |
| **Puppeteer** | https://github.com/puppeteer/puppeteer | Automated testing |

**Example - Test all forms:**
```javascript
// Check if forms actually submit
const forms = await page.$$('form');
for (const form of forms) {
  try {
    await form.fill({ email: 'test@test.com' });
    await form.submit();
    // Check if thank you page loads
  } catch (e) {
    console.log('Broken form detected');
  }
}
```

### C. Console Error Catchers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **Jest + Puppeteer** | Built-in | JavaScript errors |
| **Playwright** | Built-in | Console errors, network failures |

**Playwright code:**
```python
errors = []
page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
page.on("pageerror", lambda err: errors.append(str(err)))
```

---

## 🎨 2. DESIGN & AESTHETIC CHECKERS

### A. Visual Regression Tools

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **BackstopJS** | https://github.com/garris/BackstopJS | Visual changes, layout breaks |
| **Percy** | https://github.com/percy/percy-agent | Visual diffs |
| **Loki** | https://github.com/oblador/loki | Storybook visual tests |
| **Playwright Visual** | Built-in | Screenshot comparisons |

**BackstopJS Setup:**
```bash
npm install -g backstopjs
backstop init
backstop reference  # Take reference screenshots
backstop test       # Compare current to reference
```

### B. Color & Contrast Checkers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **axe-core** | https://github.com/dequelabs/axe-core | Color contrast issues |
| **pa11y** | https://github.com/pa11y/pa11y | Accessibility + contrast |
| **ColorContrastChecker** | https://github.com/maasencioh/ColorContrastChecker | WCAG contrast ratios |

**axe Usage:**
```bash
npm install @axe-core/cli
axe https://example.com
```

### C. Layout & Responsive Checkers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **Galen Framework** | https://github.com/galenframework/galen | Responsive layout testing |
| **Responsively App** | https://github.com/responsively-org/responsively-app | Multi-device preview |
| **Screen sizes** | N/A | Viewport testing |

**Galen Example:**
```javascript
// Check if elements are properly aligned
@objects
  header     css  header
  content    css  .content

= Main section =
  header:
    width 100% of screen/width
  content:
    below header 10 to 50px
```

### D. Image Quality Checkers

| Tool | GitHub | What It Finds |
|------|--------|---------------|
| **Image-size** | https://github.com/image-size/image-size | Oversized images |
| **Sharp** | https://github.com/lovell/sharp | Image optimization check |
| **Squoosh CLI** | https://github.com/GoogleChromeLabs/squoosh | Compression check |

---

## 🧪 3. COMPLETE TESTING SUITES

### A. Accessibility (finds design issues too)

| Tool | GitHub | Checks |
|------|--------|--------|
| **axe-core** | https://github.com/dequelabs/axe-core | 50+ accessibility rules |
| **Lighthouse (a11y)** | Built-in | Basic accessibility |
| **WAVE** | https://github.com/paciellogroup/war | Visual feedback on issues |
| **Pa11y** | https://github.com/pa11y/pa11y | CLI accessibility testing |

**Pa11y - Best CLI tool:**
```bash
npm install -g pa11y
pa11y https://example.com
pa11y --standard WCAG2AA https://example.com  # Stricter
```

### B. Comprehensive Analyzers

| Tool | GitHub | Finds |
|------|--------|-------|
| **Sitespeed.io** | https://github.com/sitespeedio/sitespeed.io | Performance + errors + best practices |
| **Yellow Lab Tools** | https://github.com/YellowLabTools/YellowLabTools | Performance + quality |
| **Webhint** | https://github.com/webhintio/hint | Multiple categories |

**Sitespeed.io (most comprehensive):**
```bash
docker run --rm -v "$(pwd):/sitespeed.io" sitespeedio/sitespeed.io https://example.com
```

---

## 🚀 4. RECOMMENDED COMBINATION

For your tour website analysis, use this stack:

```bash
# 1. BROKEN FEATURES
# Check broken links
muffet https://example.com --timeout 30

# Check console errors (Playwright/Selenium)
# Check form submissions

# 2. DESIGN ISSUES  
# Check color contrast
pa11y --standard WCAG2AA https://example.com

# Visual regression (if you have reference)
backstop test

# 3. PERFORMANCE (Lighthouse alternative)
sitespeed.io https://example.com

# 4. COMPLETE ANALYSIS
# My advanced_analyzer.py combines all these
```

---

## 📊 5. WHAT EACH TOOL FINDS

### Broken Features Detectors:
- ✅ Broken links (404s)
- ✅ Missing images
- ✅ JavaScript errors
- ✅ Failed API calls
- ✅ Broken forms (won't submit)
- ✅ Missing alt text
- ✅ 404 CSS/JS files

### Design Quality Detectors:
- ✅ Low color contrast
- ✅ Too many fonts
- ✅ Horizontal scroll (mobile)
- ✅ Touch targets too small
- ✅ Text too small
- ✅ Images not optimized
- ✅ Layout shifts
- ✅ Fixed widths (not responsive)

---

## 🔌 6. GITHUB ACTIONS INTEGRATION

Add to `.github/workflows/test.yml`:

```yaml
name: Website Quality Check

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # Broken link check
      - name: Check links
        uses: lycheeverse/lychee-action@v1
        with:
          args: https://your-site.com
      
      # Accessibility check
      - name: Check accessibility
        run: |
          npm install -g pa11y
          pa11y https://your-site.com --reporter json > pa11y-results.json
      
      # Performance
      - name: Performance test
        run: |
          npm install -g @sitespeedio/sitespeed.io
          sitespeed.io https://your-site.com
```

---

## 🎯 QUICK WINS FOR TOUR WEBSITES

**Most common issues on tour sites:**

1. **Broken booking forms** → Test with Playwright/Cypress
2. **Missing alt text on tour photos** → Pa11y/axe
3. **Non-responsive calendars** → Galen/responsive checkers
4. **Slow-loading images** → Image-size + Squoosh
5. **Poor mobile touch targets** → Playwright mobile emulation
6. **Broken payment links** → Link checker
7. **Low contrast text** → Pa11y contrast checker

---

## 📝 SUMMARY

| If you need to check... | Use this tool |
|------------------------|---------------|
| Broken links | muffet, lychee |
| Console errors | Playwright |
| Form submissions | Cypress, Playwright |
| Visual regressions | BackstopJS |
| Color contrast | Pa11y, axe |
| Responsive layout | Galen, Responsively |
| Image optimization | Sharp, Squoosh |
| Everything combined | Sitespeed.io |

**My recommendation:** Run `pa11y` (accessibility + design) + `muffet` (broken links) + `advanced_analyzer.py` (custom checks) for complete coverage.
