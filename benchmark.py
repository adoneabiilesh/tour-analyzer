"""
Benchmark script to measure time and memory usage
"""

import time
import psutil
import asyncio
import json
from analyzer import TourWebsiteAnalyzer, analyze_companies
from advanced_analyzer import AdvancedAnalyzer, run_advanced_analysis


def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024


async def benchmark_analysis(companies_json: str, limit: int = 5):
    """Benchmark the analysis tools"""
    
    print("="*70)
    print("BENCHMARK: Website Analysis Performance")
    print("="*70)
    
    # Load companies
    with open(companies_json, 'r') as f:
        all_companies = json.load(f)
    companies = all_companies[:limit]
    
    print(f"\nTesting with {len(companies)} companies...")
    print(f"Memory at start: {get_memory_usage():.1f} MB")
    
    # Benchmark Basic Analyzer
    print("\n" + "-"*70)
    print("BASIC ANALYZER (Lighthouse-style)")
    print("-"*70)
    
    start_mem = get_memory_usage()
    start_time = time.time()
    
    await analyze_companies(companies_json, "benchmark_basic.json", limit)
    
    basic_time = time.time() - start_time
    basic_mem = get_memory_usage() - start_mem
    
    print(f"\nTime: {basic_time:.1f} seconds ({basic_time/len(companies):.1f}s per site)")
    print(f"Memory: {basic_mem:.1f} MB ({basic_mem/len(companies):.1f} MB per site)")
    
    # Benchmark Advanced Analyzer
    print("\n" + "-"*70)
    print("ADVANCED ANALYZER (Broken features + Design)")
    print("-"*70)
    
    start_mem = get_memory_usage()
    start_time = time.time()
    
    await run_advanced_analysis(companies_json, "benchmark_advanced.json", limit)
    
    adv_time = time.time() - start_time
    adv_mem = get_memory_usage() - start_mem
    
    print(f"\nTime: {adv_time:.1f} seconds ({adv_time/len(companies):.1f}s per site)")
    print(f"Memory: {adv_mem:.1f} MB ({adv_mem/len(companies):.1f} MB per site)")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n{'Metric':<30} {'Basic':<15} {'Advanced':<15}")
    print("-"*60)
    print(f"{'Time per site':<30} {basic_time/len(companies):.1f}s{'':<10} {adv_time/len(companies):.1f}s")
    print(f"{'Memory per site':<30} {basic_mem/len(companies):.1f} MB{'':<7} {adv_mem/len(companies):.1f} MB")
    print(f"{'Total for 100 sites':<30} {basic_time/len(companies)*100/60:.1f} min{'':<7} {adv_time/len(companies)*100/60:.1f} min")
    print(f"{'Total for 430 sites':<30} {basic_time/len(companies)*430/60:.1f} min{'':<7} {adv_time/len(companies)*430/60:.1f} min")


def estimate_full_run():
    """Estimate time for full dataset"""
    print("\n" + "="*70)
    print("ESTIMATES FOR FULL DATASET (430 companies)")
    print("="*70)
    
    # Conservative estimates based on typical performance
    basic_per_site = 8  # seconds
    advanced_per_site = 15  # seconds
    comparison_per_site = 30  # seconds (screenshots + GIF)
    
    print(f"\n1. BASIC ANALYSIS ONLY:")
    print(f"   Time: {basic_per_site * 430 / 60:.0f} minutes ({basic_per_site * 430 / 3600:.1f} hours)")
    print(f"   Memory: ~{basic_per_site * 2:.0f} MB peak")
    
    print(f"\n2. ADVANCED ANALYSIS ONLY:")
    print(f"   Time: {advanced_per_site * 430 / 60:.0f} minutes ({advanced_per_site * 430 / 3600:.1f} hours)")
    print(f"   Memory: ~{advanced_per_site * 2:.0f} MB peak")
    
    print(f"\n3. FULL PIPELINE (Analysis + Comparison):")
    total_time = (basic_per_site + advanced_per_site + comparison_per_site) * 430
    print(f"   Time: {total_time / 60:.0f} minutes ({total_time / 3600:.1f} hours)")
    print(f"   Memory: ~500 MB peak")
    
    print(f"\n4. PARALLEL PROCESSING (5 concurrent):")
    print(f"   Time: {total_time / 3600 / 5:.1f} hours (with 5 browsers)")
    print(f"   Memory: ~2 GB peak")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "estimate":
        estimate_full_run()
    else:
        # Run actual benchmark
        asyncio.run(benchmark_analysis(
            "../dataset_crawler-google-places_2026-01-22_05-33-25-536.json",
            limit=3
        ))
        estimate_full_run()
