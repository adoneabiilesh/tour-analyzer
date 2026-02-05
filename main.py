"""
Main Orchestrator for Tour Website Automation
Analyzes, generates, and compares tour websites
"""

import asyncio
import json
import argparse
from pathlib import Path
from datetime import datetime

from analyzer import TourWebsiteAnalyzer, analyze_companies
from site_generator import SiteGenerator, CompanyInfo, generate_sites
from visual_recorder import VisualRecorder, ComparisonConfig, record_comparisons


class TourWebsiteAutomation:
    """Main automation pipeline"""
    
    def __init__(self, config: dict):
        self.config = config
        self.results_dir = Path(config.get('results_dir', './results'))
        self.results_dir.mkdir(exist_ok=True)
        
    async def run_full_pipeline(self, companies_json: str, limit: int = None):
        """Run the complete automation pipeline"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("=" * 70)
        print("TOUR WEBSITE AUTOMATION PIPELINE")
        print("=" * 70)
        
        # Phase 1: Analysis
        print("\n" + "=" * 70)
        print("PHASE 1: ANALYZING WEBSITES")
        print("=" * 70)
        
        analysis_output = self.results_dir / f"analysis_{timestamp}.json"
        await analyze_companies(companies_json, str(analysis_output), limit)
        
        # Phase 2: Generate Sites
        print("\n" + "=" * 70)
        print("PHASE 2: GENERATING WHITE-LABEL SITES")
        print("=" * 70)
        
        generated_output = self.results_dir / f"generated_{timestamp}"
        generate_sites(str(analysis_output), self.config['template_path'], 
                      str(generated_output), limit)
        
        # Phase 3: Visual Comparison (requires local dev servers running)
        print("\n" + "=" * 70)
        print("PHASE 3: VISUAL COMPARISON")
        print("=" * 70)
        print("Note: This phase requires the generated sites to be running on local dev servers")
        print("Skipping for now - run separately after building and deploying generated sites")
        
        # Summary
        print("\n" + "=" * 70)
        print("PIPELINE COMPLETE")
        print("=" * 70)
        print(f"\nResults saved to: {self.results_dir}")
        print(f"Analysis: {analysis_output}")
        print(f"Generated Sites: {generated_output}")
        
        return {
            'analysis': str(analysis_output),
            'generated': str(generated_output)
        }
    
    async def analyze_only(self, companies_json: str, limit: int = None):
        """Run only the analysis phase"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_output = self.results_dir / f"analysis_{timestamp}.json"
        
        await analyze_companies(companies_json, str(analysis_output), limit)
        return str(analysis_output)
    
    def generate_only(self, analysis_json: str, limit: int = None):
        """Run only the generation phase"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_output = self.results_dir / f"generated_{timestamp}"
        
        generate_sites(analysis_json, self.config['template_path'], 
                      str(generated_output), limit)
        return str(generated_output)
    
    async def compare_only(self, manifest_json: str, output_dir: str = None):
        """Run only the visual comparison phase"""
        
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.results_dir / f"comparisons_{timestamp}"
        
        await record_comparisons(manifest_json, str(output_dir))
        return str(output_dir)


def create_sample_config():
    """Create a sample configuration file"""
    config = {
        "template_path": "../rome-tour-tickets",
        "results_dir": "./results",
        "dev_server": {
            "host": "localhost",
            "port": 3000
        },
        "scoring_weights": {
            "online_booking": 10,
            "payment_system": 10,
            "mobile_friendly": 10,
            "tour_listings": 10,
            "pricing": 10
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Created config.json - edit this file to customize settings")


def main():
    parser = argparse.ArgumentParser(description='Tour Website Automation')
    parser.add_argument('command', choices=['full', 'analyze', 'generate', 'compare', 'init'],
                       help='Command to run')
    parser.add_argument('--input', '-i', default='../dataset_crawler-google-places_2026-01-22_05-33-25-536.json',
                       help='Input JSON file with company data')
    parser.add_argument('--analysis', '-a', help='Analysis JSON file (for generate command)')
    parser.add_argument('--manifest', '-m', help='Generated sites manifest (for compare command)')
    parser.add_argument('--limit', '-l', type=int, help='Limit number of companies to process')
    parser.add_argument('--config', '-c', default='config.json',
                       help='Configuration file')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        create_sample_config()
        return
    
    # Load config
    if Path(args.config).exists():
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = {
            'template_path': '../rome-tour-tickets',
            'results_dir': './results'
        }
    
    automation = TourWebsiteAutomation(config)
    
    if args.command == 'full':
        asyncio.run(automation.run_full_pipeline(args.input, args.limit))
    
    elif args.command == 'analyze':
        asyncio.run(automation.analyze_only(args.input, args.limit))
    
    elif args.command == 'generate':
        if not args.analysis:
            print("Error: --analysis required for generate command")
            return
        automation.generate_only(args.analysis, args.limit)
    
    elif args.command == 'compare':
        if not args.manifest:
            print("Error: --manifest required for compare command")
            return
        asyncio.run(automation.compare_only(args.manifest))


if __name__ == "__main__":
    main()
