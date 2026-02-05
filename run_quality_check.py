"""
Run Quality Checks using multiple open-source tools
Combines multiple analyzers for comprehensive testing
"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, asdict

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("pip install playwright")
    sys.exit(1)


@dataclass
class QualityReport:
    """Combined quality report"""
    url: str
    company_name: str
    
    # Broken features
    broken_links: List[str] = None
    console_errors: List[str] = None
    missing_alt_text: int = 0
    failed_requests: List[str] = None
    
    # Design issues
    horizontal_scroll: bool = False
    tiny_text_count: int = 0
    color_count: int = 0
    font_count: int = 0
    low_contrast_warnings: int = 0
    
    # Accessibility
    accessibility_score: int = 0
    
    # Overall
    critical_issues: int = 0
    warnings: int = 0
    
    def __post_init__(self):
        if self.broken_links is None:
            self.broken_links = []
        if self.console_errors is None:
            self.console_errors = []
        if self.failed_requests is None:
            self.failed_requests = []


class QualityChecker:
    """Multi-tool quality checker"""
    
    def __init__(self):
        self.issues = []
    
    async def check_website(self, url: str, company_name: str) -> QualityReport:
        """Run comprehensive quality checks"""
        report = QualityReport(url=url, company_name=company_name)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            # Collect errors
            console_errors = []
            failed_requests = []
            
            page = await browser.new_page(viewport={'width': 1280, 'height': 800})
            
            page.on("console", lambda msg: console_errors.append(msg.text) 
                    if msg.type == "error" else None)
            page.on("requestfailed", lambda req: failed_requests.append(req.url))
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)
                
                # 1. Check broken links (internal tool)
                report.broken_links = await self._find_broken_links(page, url)
                
                # 2. Check design issues
                design_data = await self._analyze_design(page)
                report.horizontal_scroll = design_data.get('horizontal_scroll', False)
                report.tiny_text_count = design_data.get('tiny_text_count', 0)
                report.color_count = design_data.get('color_count', 0)
                report.font_count = design_data.get('font_count', 0)
                
                # 3. Check accessibility basics
                a11y_data = await self._check_accessibility(page)
                report.missing_alt_text = a11y_data.get('missing_alt', 0)
                report.accessibility_score = a11y_data.get('score', 0)
                report.low_contrast_warnings = a11y_data.get('contrast_issues', 0)
                
                # 4. Console errors
                report.console_errors = console_errors[:10]  # First 10
                report.failed_requests = failed_requests
                
                # Calculate totals
                report.critical_issues = (
                    len(report.broken_links) + 
                    len(report.failed_requests) +
                    (1 if report.horizontal_scroll else 0)
                )
                report.warnings = (
                    len(report.console_errors) +
                    report.missing_alt_text +
                    report.tiny_text_count
                )
                
            except Exception as e:
                print(f"Error checking {url}: {e}")
            
            await browser.close()
        
        return report
    
    async def _find_broken_links(self, page, base_url: str) -> List[str]:
        """Find broken links on the page"""
        broken = []
        
        links = await page.eval_on_selector_all('a[href]', '''
            links => links
                .map(a => a.href)
                .filter(href => href.startsWith('http'))
                .slice(0, 15)  # Check first 15
        ''')
        
        for link in links:
            try:
                response = await page.context.request.fetch(link, method='HEAD', timeout=10000)
                if response.status >= 400:
                    broken.append(f"{link} (Status: {response.status})")
            except Exception:
                broken.append(f"{link} (Failed to load)")
        
        return broken
    
    async def _analyze_design(self, page) -> Dict:
        """Analyze design issues"""
        return await page.evaluate("""() => {
            const results = {
                colors: new Set(),
                fonts: new Set(),
                tiny_text_count: 0,
                horizontal_scroll: false
            };
            
            // Check all elements
            document.querySelectorAll('*').forEach(el => {
                const style = window.getComputedStyle(el);
                
                results.colors.add(style.color);
                results.colors.add(style.backgroundColor);
                results.fonts.add(style.fontFamily);
                
                const fontSize = parseInt(style.fontSize);
                if (fontSize < 12) results.tiny_text_count++;
            });
            
            // Check horizontal scroll
            results.horizontal_scroll = document.documentElement.scrollWidth > window.innerWidth;
            
            return {
                color_count: results.colors.size,
                font_count: results.fonts.size,
                tiny_text_count: results.tiny_text_count,
                horizontal_scroll: results.horizontal_scroll
            };
        }""")
    
    async def _check_accessibility(self, page) -> Dict:
        """Basic accessibility checks"""
        return await page.evaluate("""() => {
            const issues = {
                missing_alt: 0,
                contrast_issues: 0,
                score: 100
            };
            
            // Missing alt text
            document.querySelectorAll('img').forEach(img => {
                if (!img.alt) issues.missing_alt++;
            });
            
            // Basic contrast check (simplified)
            document.querySelectorAll('p, span, a, h1, h2, h3, h4').forEach(el => {
                const style = window.getComputedStyle(el);
                const color = style.color;
                const bg = style.backgroundColor;
                
                // If light text on light background (simplified check)
                if (color.includes('200') || color.includes('255')) {
                    if (bg.includes('255') || bg.includes('transparent')) {
                        issues.contrast_issues++;
                    }
                }
            });
            
            // Calculate score
            issues.score = Math.max(0, 100 - (issues.missing_alt * 3) - (issues.contrast_issues * 2));
            
            return issues;
        }""")


def print_report(report: QualityReport):
    """Print formatted report"""
    print(f"\n{'='*60}")
    print(f"Quality Report: {report.company_name}")
    print(f"{'='*60}")
    
    print(f"\n📊 SCORES:")
    print(f"  Accessibility: {report.accessibility_score}/100")
    
    print(f"\n🚨 CRITICAL ISSUES ({report.critical_issues}):")
    if report.broken_links:
        print(f"  Broken Links ({len(report.broken_links)}):")
        for link in report.broken_links[:3]:
            print(f"    - {link[:60]}...")
    if report.horizontal_scroll:
        print(f"  Horizontal scroll on mobile (layout issue)")
    if report.failed_requests:
        print(f"  Failed requests: {len(report.failed_requests)}")
    
    print(f"\n⚠️  WARNINGS ({report.warnings}):")
    print(f"  Missing alt text: {report.missing_alt_text} images")
    print(f"  Tiny text (<12px): {report.tiny_text_count} elements")
    print(f"  Console errors: {len(report.console_errors)}")
    
    print(f"\n🎨 DESIGN:")
    print(f"  Colors used: {report.color_count} (too many? {report.color_count > 6})")
    print(f"  Fonts used: {report.font_count} (too many? {report.font_count > 3})")
    print(f"  Contrast issues: {report.low_contrast_warnings}")


async def main():
    """Run quality checks on analysis results"""
    
    # Load companies
    with open('analysis_results.json', 'r') as f:
        companies = json.load(f)[:3]  # First 3
    
    checker = QualityChecker()
    reports = []
    
    print("Running Quality Checks...")
    print("=" * 60)
    
    for company in companies:
        url = company.get('url', company.get('website', ''))
        if not url:
            continue
        
        report = await checker.check_website(url, company['company_name'])
        print_report(report)
        reports.append(asdict(report))
    
    # Save results
    with open('quality_reports.json', 'w') as f:
        json.dump(reports, f, indent=2)
    
    print(f"\n\nSaved to: quality_reports.json")


if __name__ == "__main__":
    asyncio.run(main())
