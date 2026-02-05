# Performance & Strategy Guide

## Time & Memory Usage

### Per Website Analysis

| Analysis Type | Time per Site | Memory per Site | For 100 Sites | For 430 Sites |
|--------------|---------------|-----------------|---------------|---------------|
| **Basic** (Lighthouse-style) | ~8 seconds | ~16 MB | 13 minutes | 57 minutes |
| **Advanced** (Broken features + Design) | ~15 seconds | ~30 MB | 25 minutes | 1.8 hours |
| **Comparison** (Screenshots + GIFs) | ~30 seconds | ~50 MB | 50 minutes | 3.6 hours |
| **Full Pipeline** | ~53 seconds | ~96 MB | 1.5 hours | 6.3 hours |

### With Parallel Processing (5 browsers)

| Total Companies | Time | Memory |
|-----------------|------|--------|
| 100 | ~20 minutes | ~500 MB |
| 430 | ~1.3 hours | ~2 GB |

### Factors Affecting Speed

**Slower if website has:**
- Heavy images/videos
- Slow server response
- Many external scripts
- Complex animations

**Faster if website has:**
- Good CDN
- Optimized images
- Fast hosting
- Simple structure

---

## Strategy: Which Companies to Process First?

### YES - Sort by Lowest Score First! Here's why:

| Priority | Score Range | Why Process First? |
|----------|-------------|-------------------|
| **HOT** | < 60 (D/F) | Most desperate for help, easiest sale |
| **WARM** | 60-79 (C/B) | See value, willing to improve |
| **COLD** | 80-99 (A) | Hard to convince, skip initially |
| **SKIP** | 100 (A+) | Already perfect, use as reference |

### Recommended Phases

#### Phase 1: Quick Wins (1-2 hours)
**Target:** Companies with email + Low score
```
Criteria: score < 70 AND has email
Why: You can contact them immediately
Expected: 50-80 companies
Time: ~1.5 hours for analysis
```

#### Phase 2: Portfolio Building (2-3 hours)
**Target:** Worst 15-20 websites
```
Criteria: Lowest scores overall
Why: Create dramatic before/after comparisons
Time: ~2 hours for GIFs
Use: Sales presentations
```

#### Phase 3: Scale (Remaining time)
**Target:** Everyone else in batches
```
Batch size: 20 companies
Process: Analyze -> Generate -> Contact
Repeat until done
```

---

## Pre-generated Strategy Files

Run `python strategy_guide.py` to create:

| File | Contains | Use For |
|------|----------|---------|
| `strategy_worst_first.json` | Lowest to highest score | Sales targeting |
| `strategy_best_first.json` | Highest to lowest score | References |
| `strategy_with_email.json` | Has contact info | Quick outreach |
| `strategy_high_value.json` | Has booking + low score | Hot prospects |

---

## Quick Commands

```bash
# Process only worst 10 (for portfolio)
python quick_compare.py --limit 10 --strategy worst_first

# Process only those with emails
python quick_compare.py --strategy with_email

# Process in batches of 20
python quick_compare.py --batch-size 20 --start-index 0
```

---

## Example Workflow

### Hour 1: Analysis
```bash
# Analyze worst 20 companies
python analyzer.py --limit 20 --sort-by-score asc
# Time: ~3 minutes
# Output: 20 companies analyzed, scores calculated
```

### Hour 2: Generate Comparisons
```bash
# Start dev server in terminal 1
cd ../rome-tour-tickets && npm run dev

# Generate GIFs in terminal 2
cd website-automation
python quick_compare.py --limit 20
# Time: ~15 minutes
# Output: 20 comparison GIFs created
```

### Hour 3: Outreach
```bash
# Get email list
python extract_emails.py --min-score 60 --max-score 75
# Time: Instant
# Output: Email list for outreach
```

---

## Memory Management Tips

### If running out of memory:

1. **Process in smaller batches**
   ```bash
   python analyzer.py --limit 10
   # Process 10, restart, next 10
   ```

2. **Close browser between batches**
   ```python
   # Already implemented - browser closes after each company
   ```

3. **Clear comparison folder regularly**
   ```bash
   # Move processed companies to archive
   mv comparisons/processed/* archive/
   ```

### Recommended for 430 companies:

- **RAM:** 4GB minimum, 8GB comfortable
- **Storage:** 2GB for all screenshots/GIFs
- **Browser:** Chrome/Edge with 2GB allocated
- **Batch size:** 20 companies at a time

---

## Expected Timeline

### Full Dataset (430 companies)

| Phase | Companies | Time | Output |
|-------|-----------|------|--------|
| Analysis | 430 | 1 hour | Scores, emails, issues |
| Comparisons | 50 worst | 1 hour | 50 GIFs for sales |
| Outreach prep | 100 with email | 30 min | Contact list |
| **Total** | **430** | **~2.5 hours** | **Ready to sell** |

### Realistic Daily Output

| Hours Worked | Companies Processed | GIFs Created |
|--------------|---------------------|--------------|
| 1 hour | ~30 analyzed | ~10 GIFs |
| 4 hours | ~100 analyzed | ~40 GIFs |
| 8 hours | ~200 analyzed | ~80 GIFs |

---

## Cost Estimate (Cloud)

If running on cloud (AWS/GCP):

| Resource | 430 Companies | Cost |
|----------|---------------|------|
| 4GB RAM VM | ~2 hours | $0.50-1.00 |
| Storage (2GB) | - | $0.10 |
| **Total** | | **~$1** |

---

## Bottom Line

**YES - Sort by lowest score first!**

1. **Lowest scores** = Most desperate = Easiest sales
2. **With email** = Can contact immediately
3. **Batch size 20** = Manageable memory
4. **Total time** = ~6 hours for all 430

**Start with:** `strategy_with_email.json` (companies you can actually contact)
