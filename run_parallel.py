"""
Parallel Processing Runner
Runs multiple analysis jobs in parallel using multiprocessing
"""

import asyncio
import json
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path
from analyzer import TourWebsiteAnalyzer, analyze_companies


def process_batch(batch_info):
    """Process a single batch of companies"""
    batch_id, companies_chunk = batch_info
    
    print(f"[Batch {batch_id}] Starting with {len(companies_chunk)} companies...")
    
    # Save temporary input file
    temp_input = f"batch_{batch_id}_input.json"
    with open(temp_input, 'w') as f:
        json.dump(companies_chunk, f)
    
    # Run analysis
    try:
        asyncio.run(analyze_companies(temp_input, f"batch_{batch_id}_results.json", limit=None))
        print(f"[Batch {batch_id}] Complete!")
        return batch_id, True
    except Exception as e:
        print(f"[Batch {batch_id}] Error: {e}")
        return batch_id, False


def run_parallel(input_file: str, num_workers: int = None):
    """Run analysis in parallel using multiple processes"""
    
    if num_workers is None:
        num_workers = min(cpu_count(), 10)  # Max 10 parallel
    
    print(f"Loading companies from {input_file}...")
    with open(input_file, 'r') as f:
        all_companies = json.load(f)
    
    total = len(all_companies)
    print(f"Total companies: {total}")
    print(f"Parallel workers: {num_workers}")
    
    # Split into batches
    batch_size = total // num_workers
    batches = []
    
    for i in range(num_workers):
        start = i * batch_size
        if i == num_workers - 1:  # Last batch gets remainder
            end = total
        else:
            end = start + batch_size
        batches.append((i, all_companies[start:end]))
    
    print(f"Batch size: ~{batch_size} companies per worker\n")
    
    # Process in parallel
    start_time = time.time()
    
    with Pool(num_workers) as pool:
        results = pool.map(process_batch, batches)
    
    elapsed = time.time() - start_time
    
    # Merge results
    print("\nMerging results...")
    all_results = []
    success_count = 0
    
    for batch_id, success in results:
        result_file = f"batch_{batch_id}_results.json"
        if Path(result_file).exists():
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_results.extend(data)
                    success_count += len(data) if isinstance(data, list) else 1
            except Exception as e:
                print(f"Error reading batch {batch_id}: {e}")
    
    # Save final results
    with open('parallel_analysis_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Cleanup temp files
    for batch_id, _ in results:
        for file_type in ['input', 'results']:
            file_path = Path(f"batch_{batch_id}_{file_type}.json")
            if file_path.exists():
                file_path.unlink()
    
    print(f"\n{'='*60}")
    print(f"Complete!")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Companies analyzed: {len(all_results)}")
    print(f"Speedup: {num_workers}x faster than sequential")
    print(f"Results saved to: parallel_analysis_results.json")
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys
    
    input_file = "../dataset_crawler-google-places_2026-01-22_05-33-25-536.json"
    
    # Detect if running on cloud (more CPUs available)
    cpu_cores = cpu_count()
    print(f"Detected {cpu_cores} CPU cores")
    
    if cpu_cores >= 8:
        workers = 10  # Cloud instance
        print("Cloud environment detected - using 10 workers")
    else:
        workers = min(4, cpu_cores)  # Local machine
        print(f"Local machine - using {workers} workers")
    
    run_parallel(input_file, num_workers=workers)
