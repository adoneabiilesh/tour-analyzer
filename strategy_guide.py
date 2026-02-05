"""
Strategy Guide: Which companies to prioritize
Analyzes the dataset and recommends processing order
"""

import json
from collections import Counter
from pathlib import Path


def analyze_dataset(json_path: str):
    """Analyze the full dataset and provide strategy recommendations"""
    
    with open(json_path, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    print("="*70)
    print("DATASET ANALYSIS & STRATEGY RECOMMENDATIONS")
    print("="*70)
    
    print(f"\n[STATS] DATASET OVERVIEW:")
    print(f"   Total companies: {len(companies)}")
    
    # Check which have websites
    with_websites = [c for c in companies if c.get('website')]
    print(f"   With websites: {len(with_websites)}")
    print(f"   Without websites: {len(companies) - len(with_websites)}")
    
    # Score distribution (if already analyzed)
    analysis_file = Path("analysis_results.json")
    if analysis_file.exists():
        with open(analysis_file, 'r') as f:
            analyzed = json.load(f)
        
        print(f"\n[CHART] SCORE DISTRIBUTION ({len(analyzed)} analyzed):")
        
        grades = Counter([c.get('grade', 'N/A') for c in analyzed])
        for grade in ['A+', 'A', 'B', 'C', 'D', 'F']:
            count = grades.get(grade, 0)
            bar = "#" * count
            print(f"   {grade:<3}: {count:>3} {bar}")
        
        # Score ranges
        scores = [c.get('total_score', 0) for c in analyzed]
        print(f"\n   Average score: {sum(scores)/len(scores):.1f}/100")
        print(f"   Highest: {max(scores)}/100")
        print(f"   Lowest: {min(scores)}/100")
        
        # Recommendation
        low_score = [c for c in analyzed if c.get('total_score', 0) < 60]
        high_score = [c for c in analyzed if c.get('total_score', 0) >= 80]
        
        print(f"\n[SEGMENTS]:")
        print(f"   [RED] Needs redesign (score < 60): {len(low_score)} companies")
        print(f"   [YEL] Average (60-79): {len([c for c in analyzed if 60 <= c.get('total_score', 0) < 80])} companies")
        print(f"   [GRN] Good (80+): {len(high_score)} companies")
    
    return companies


def generate_processing_lists(json_path: str):
    """Generate sorted lists for different strategies"""
    
    analysis_file = Path("analysis_results.json")
    if not analysis_file.exists():
        print("\n[!] No analysis_results.json found. Run analyzer first!")
        return
    
    with open(analysis_file, 'r') as f:
        analyzed = json.load(f)
    
    print("\n" + "="*70)
    print("PROCESSING STRATEGIES")
    print("="*70)
    
    # Strategy 1: Worst First (Lowest scores)
    print("\n[1] STRATEGY 1: Worst First (Recommended for Sales)")
    print("-"*70)
    worst_first = sorted(analyzed, key=lambda x: x.get('total_score', 0))
    print("   Top 10 companies needing help most:")
    for i, c in enumerate(worst_first[:10], 1):
        score = c.get('total_score', 0)
        grade = c.get('grade', 'N/A')
        print(f"   {i:>2}. {c['company_name'][:35]:<35} | {score:>3}/100 ({grade})")
    
    # Save worst first list
    with open('strategy_worst_first.json', 'w') as f:
        json.dump(worst_first, f, indent=2)
    print(f"   [SAVED] Saved to: strategy_worst_first.json")
    
    # Strategy 2: Best First
    print("\n[2] STRATEGY 2: Best First (Good References)")
    print("-"*70)
    best_first = sorted(analyzed, key=lambda x: x.get('total_score', 0), reverse=True)
    print("   Top 10 best websites (for reference):")
    for i, c in enumerate(best_first[:10], 1):
        score = c.get('total_score', 0)
        grade = c.get('grade', 'N/A')
        email = c.get('extracted_email', '')
        print(f"   {i:>2}. {c['company_name'][:35]:<35} | {score:>3}/100 ({grade}) | {email[:25]}")
    
    with open('strategy_best_first.json', 'w') as f:
        json.dump(best_first, f, indent=2)
    print(f"   [SAVED] Saved to: strategy_best_first.json")
    
    # Strategy 3: With Email (Contactable)
    print("\n[3] STRATEGY 3: Has Email (Easy to contact)")
    print("-"*70)
    with_email = [c for c in analyzed if c.get('extracted_email')]
    with_email_sorted = sorted(with_email, key=lambda x: x.get('total_score', 0))
    print(f"   {len(with_email)} companies have email addresses")
    print("   Top 10 contactable companies with low scores:")
    for i, c in enumerate(with_email_sorted[:10], 1):
        score = c.get('total_score', 0)
        email = c.get('extracted_email', '')
        print(f"   {i:>2}. {c['company_name'][:30]:<30} | {score:>3}/100 | {email[:30]}")
    
    with open('strategy_with_email.json', 'w') as f:
        json.dump(with_email_sorted, f, indent=2)
    print(f"   [SAVED] Saved to: strategy_with_email.json")
    
    # Strategy 4: High Value (Low score + Has booking)
    print("\n[4] STRATEGY 4: High Value Prospects")
    print("-"*70)
    print("   Criteria: Has online booking BUT low score")
    high_value = [c for c in analyzed 
                  if c.get('has_online_booking') and c.get('total_score', 0) < 70]
    high_value_sorted = sorted(high_value, key=lambda x: x.get('total_score', 0))
    print(f"   Found {len(high_value)} high-value prospects")
    for i, c in enumerate(high_value_sorted[:10], 1):
        score = c.get('total_score', 0)
        email = c.get('extracted_email', 'No email')
        print(f"   {i:>2}. {c['company_name'][:30]:<30} | {score:>3}/100 | {email}")
    
    with open('strategy_high_value.json', 'w') as f:
        json.dump(high_value_sorted, f, indent=2)
    print(f"   [SAVED] Saved to: strategy_high_value.json")
    
    # Recommendation
    print("\n" + "="*70)
    print("RECOMMENDED APPROACH")
    print("="*70)
    print("""
    [BEST] BEST STRATEGY FOR SALES:
       
       Phase 1: Quick Wins (1-2 hours)
       - Process "with_email" list (companies you can contact)
       - Start with lowest scores first
       - These are most likely to buy
       
       Phase 2: Portfolio Building (2-3 hours)
       - Process 10-15 worst websites
       - Create impressive before/after GIFs
       - Use as sales collateral
       
       Phase 3: Scale (Remaining)
       - Process rest in batches of 20
       - Focus on high-value prospects
    
    [TARGET] PRIORITY ORDER:
       1. Low score (< 60) + Has email --> Hot leads
       2. Low score (< 60) + No email --> Portfolio
       3. Medium score (60-79) --> Nurture
       4. High score (80+) --> Skip or reference
    """)
    
    return {
        'worst_first': worst_first,
        'best_first': best_first,
        'with_email': with_email_sorted,
        'high_value': high_value_sorted
    }


if __name__ == "__main__":
    dataset = "../dataset_crawler-google-places_2026-01-22_05-33-25-536.json"
    
    # Analyze
    analyze_dataset(dataset)
    
    # Generate strategies
    generate_processing_lists(dataset)
