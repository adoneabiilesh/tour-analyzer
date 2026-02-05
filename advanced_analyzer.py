"""
Advanced Website Analyzer
Checks for broken features, design issues, and functionality problems
"""

import asyncio
import json
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse

try:
    from playwright.async_api import async_playwright, Page, Browser
    from bs4 import BeautifulSoup
except ImportError:
    print("pip install playwright beautifulsoup4")
    raise


@dataclass
class BrokenFeatures:
    """Broken functionality checks"""
    # Navigation
    broken_links: List[str] = None
    missing_pages: List[str] = None
    
    # Forms
    broken_forms: List[str] = None  # Forms that don't submit
    missing_labels: List[str] = None  # Inputs without labels
    
    # Images
    broken_images: List[str] = None  # 404 images
    oversized_images: List[str] = None  # Images > 500KB
    missing_alt: int = 0
    
    # Scripts
    console_errors: List[str] = None  # JavaScript errors
    failed_requests: List[str] = None  # 404 CSS/JS files
    
    def __post_init__(self):
        for field in ['broken_links', 'missing_pages', 'broken_forms', 
                      'missing_labels', 'broken_images', 'oversized_images',
                      'console_errors', 'failed_requests']:
            if getattr(self, field) is None:
                setattr(self, field, [])


@dataclass
class DesignIssues:
    """Design and aesthetic issues"""
    # Color
    low_contrast_elements: List[Dict] = None  # Text with poor contrast
    too_many_colors: bool = False
    color_count: int = 0
    
    # Typography
    too_many_fonts: bool = False
    font_count: int = 0
    tiny_text: List[str] = None  # Text < 12px
    
    # Layout
    horizontal_scroll: bool = False  # Mobile issue
    overlapping_elements: List[str] = None
    cluttered_layout: bool = False  # Too many elements above fold
    
    # Images
    blurry_images: List[str] = None  # Low resolution
    stretched_images: List[str] = None  # Wrong aspect ratio
    
    # Mobile
    non_responsive_elements: List[str] = None  # Fixed widths
    touch_targets_too_small: List[str] = None  # Buttons < 44px
    
    def __post_init__(self):
        for field in ['low_contrast_elements', 'tiny_text', 'overlapping_elements',
                      'blurry_images', 'stretched_images', 'non_responsive_elements',
                      'touch_targets_too_small']:
            if getattr(self, field) is None:
                setattr(self, field, [])


@dataclass
class AdvancedScore:
    """Extended scoring with broken features and design checks"""
    url: str
    company_name: str
    
    # Lighthouse-like scores (0-100)
    functionality_score: int = 0  # Broken features
    design_score: int = 0  # Aesthetic issues
    accessibility_score: int = 0  # A11y issues
    ux_score: int = 0  # User experience
    
    # Details
    broken: BrokenFeatures = None
    design: DesignIssues = None
    
    # Specific issues count
    total_errors: int = 0
    total_warnings: int = 0
    
    def __post_init__(self):
        if self.broken is None:
            self.broken = BrokenFeatures()
        if self.design is None:
            self.design = DesignIssues()
    
    @property
    def overall_score(self) -> int:
        """Weighted overall score"""
        return int(
            self.functionality_score * 0.35 +
            self.design_score * 0.25 +
            self.accessibility_score * 0.25 +
            self.ux_score * 0.15
        )
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['overall_score'] = self.overall_score
        return data


class AdvancedAnalyzer:
    """Advanced analyzer for broken features and design issues"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    async def init(self):
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
    
    async def close(self):
        if self.browser:
            await self.browser.close()
    
    async def analyze_website(self, url: str, company_name: str) -> AdvancedScore:
        """Full advanced analysis"""
        await self.init()
        score = AdvancedScore(url=url, company_name=company_name)
        
        page = await self.browser.new_page(viewport={'width': 1280, 'height': 800})
        
        # Collect console errors
        self.errors = []
        page.on("console", lambda msg: self.errors.append(msg.text) if msg.type == "error" else None)
        
        try:
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(2000)
            
            # Get HTML content
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Check broken features
            score.broken = await self._check_broken_features(page, soup, url)
            
            # Check design issues
            score.design = await self._check_design_issues(page, soup)
            
            # Check accessibility
            score.accessibility_score = await self._check_accessibility(page, soup)
            
            # Calculate scores
            score.functionality_score = self._calc_functionality_score(score.broken)
            score.design_score = self._calc_design_score(score.design)
            score.ux_score = self._calc_ux_score(score.broken, score.design)
            
            score.total_errors = len(score.broken.broken_links) + len(score.broken.broken_images) + \
                                len(score.broken.console_errors) + len(score.broken.failed_requests)
            score.total_warnings = len(score.broken.missing_labels) + len(score.design.low_contrast_elements) + \
                                  len(score.design.tiny_text)
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
        
        await page.close()
        return score
    
    async def _check_broken_features(self, page: Page, soup: BeautifulSoup, base_url: str) -> BrokenFeatures:
        """Check for broken functionality"""
        broken = BrokenFeatures()
        
        # Check all links
        links = soup.find_all('a', href=True)
        for link in links[:20]:  # Check first 20 links
            href = link['href']
            if href.startswith('http') or href.startswith('/'):
                full_url = urljoin(base_url, href)
                try:
                    response = await page.context.request.fetch(full_url, method='HEAD')
                    if response.status >= 400:
                        broken.broken_links.append(full_url)
                except:
                    pass  # Skip if can't check
        
        # Check images
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            if not img.get('alt'):
                broken.missing_alt += 1
            if src:
                try:
                    response = await page.context.request.fetch(urljoin(base_url, src), method='HEAD')
                    if response.status >= 400:
                        broken.broken_images.append(src)
                except:
                    pass
        
        # Check forms
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all(['input', 'textarea', 'select'])
            for inp in inputs:
                if not inp.get('id') or not soup.find('label', {'for': inp.get('id')}):
                    if not inp.get('aria-label') and not inp.get('placeholder'):
                        broken.missing_labels.append(inp.get('name', 'unnamed'))
        
        # Console errors
        broken.console_errors = self.errors[:10]  # First 10 errors
        
        return broken
    
    async def _check_design_issues(self, page: Page, soup: BeautifulSoup) -> DesignIssues:
        """Check for design/aesthetic issues"""
        design = DesignIssues()
        
        # Check via JavaScript
        js_results = await page.evaluate("""() => {
            const results = {
                colors: new Set(),
                fonts: new Set(),
                tinyText: [],
                lowContrast: [],
                fixedWidths: [],
                smallTouchTargets: [],
                horizontalScroll: false
            };
            
            // Get all elements
            const allElements = document.querySelectorAll('*');
            
            allElements.forEach(el => {
                const style = window.getComputedStyle(el);
                
                // Collect colors
                results.colors.add(style.color);
                results.colors.add(style.backgroundColor);
                
                // Collect fonts
                results.fonts.add(style.fontFamily);
                
                // Check font size
                const fontSize = parseInt(style.fontSize);
                if (fontSize < 12) {
                    results.tinyText.push(el.tagName + (el.className ? '.' + el.className : ''));
                }
                
                // Check contrast (simplified)
                const color = style.color;
                const bg = style.backgroundColor;
                if (color.includes('rgb') && (bg.includes('255') || bg.includes('transparent'))) {
                    // Potentially low contrast
                }
                
                // Check fixed widths
                if (style.width.includes('px') && !style.width.includes('%')) {
                    const width = parseInt(style.width);
                    if (width > 400) {
                        results.fixedWidths.push(el.tagName);
                    }
                }
                
                // Check touch target size
                const rect = el.getBoundingClientRect();
                if ((el.tagName === 'BUTTON' || el.tagName === 'A') && 
                    (rect.width < 44 || rect.height < 44)) {
                    results.smallTouchTargets.push(el.textContent?.substring(0, 20) || el.tagName);
                }
            });
            
            // Check for horizontal scroll
            results.horizontalScroll = document.documentElement.scrollWidth > window.innerWidth;
            
            return {
                colorCount: results.colors.size,
                fontCount: results.fonts.size,
                tinyTextCount: results.tinyText.length,
                horizontalScroll: results.horizontalScroll,
                smallTouchTargets: results.smallTouchTargets.slice(0, 5)
            };
        }""")
        
        design.color_count = js_results['colorCount']
        design.too_many_colors = design.color_count > 6
        design.font_count = js_results['fontCount']
        design.too_many_fonts = design.font_count > 3
        design.horizontal_scroll = js_results['horizontalScroll']
        design.touch_targets_too_small = js_results['smallTouchTargets']
        
        return design
    
    async def _check_accessibility(self, page: Page, soup: BeautifulSoup) -> int:
        """Check accessibility and return score (0-100)"""
        issues = 0
        
        # Check for common accessibility issues
        checks = {
            'missing_alt': len(soup.find_all('img', alt=False)),
            'missing_labels': len([f for f in soup.find_all('form') if not f.find('label')]),
            'no_lang_attr': 1 if not soup.html.get('lang') else 0,
            'missing_title': 1 if not soup.title else 0,
            'low_contrast_risk': 0,  # Would need actual contrast calculation
        }
        
        issues = sum(checks.values())
        
        # Score: 100 - (issues * 5), minimum 0
        return max(0, 100 - (issues * 5))
    
    def _calc_functionality_score(self, broken: BrokenFeatures) -> int:
        """Calculate functionality score (0-100)"""
        score = 100
        score -= len(broken.broken_links) * 5
        score -= len(broken.broken_images) * 3
        score -= len(broken.console_errors) * 2
        score -= len(broken.failed_requests) * 5
        score -= len(broken.broken_forms) * 10
        return max(0, score)
    
    def _calc_design_score(self, design: DesignIssues) -> int:
        """Calculate design score (0-100)"""
        score = 100
        if design.too_many_colors:
            score -= 15
        if design.too_many_fonts:
            score -= 15
        if design.horizontal_scroll:
            score -= 20
        score -= len(design.tiny_text) * 2
        score -= len(design.low_contrast_elements) * 5
        score -= len(design.touch_targets_too_small) * 3
        return max(0, score)
    
    def _calc_ux_score(self, broken: BrokenFeatures, design: DesignIssues) -> int:
        """Calculate UX score (0-100)"""
        score = 100
        # Missing labels hurts UX
        score -= len(broken.missing_labels) * 5
        # Alt text missing hurts UX
        score -= broken.missing_alt * 2
        # Small touch targets
        score -= len(design.touch_targets_too_small) * 5
        return max(0, score)


async def run_advanced_analysis(input_json: str, output_json: str, limit: int = None):
    """Run advanced analysis on companies"""
    
    with open(input_json, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    if limit:
        companies = companies[:limit]
    
    analyzer = AdvancedAnalyzer()
    results = []
    
    print(f"Advanced analysis of {len(companies)} websites...\n")
    
    for i, company in enumerate(companies, 1):
        url = company.get('website', '')
        if not url or not url.startswith('http'):
            continue
        
        print(f"[{i}/{len(companies)}] Analyzing {company['title']}...")
        
        try:
            score = await analyzer.analyze_website(url, company['title'])
            results.append(score.to_dict())
            
            print(f"    Overall: {score.overall_score}/100")
            print(f"    Functionality: {score.functionality_score}/100")
            print(f"    Design: {score.design_score}/100")
            print(f"    Accessibility: {score.accessibility_score}/100")
            print(f"    Errors: {score.total_errors}, Warnings: {score.total_warnings}")
            
            if score.broken.broken_links:
                print(f"    Broken links: {len(score.broken.broken_links)}")
            if score.design.horizontal_scroll:
                print(f"    Has horizontal scroll (mobile issue)")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    await analyzer.close()
    
    # Save results
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to {output_json}")
    
    # Summary
    if results:
        avg_overall = sum(r['overall_score'] for r in results) / len(results)
        print(f"\nAverage Overall Score: {avg_overall:.1f}/100")
        print(f"Highest: {max(r['overall_score'] for r in results)}/100")
        print(f"Lowest: {min(r['overall_score'] for r in results)}/100")


if __name__ == "__main__":
    asyncio.run(run_advanced_analysis(
        input_json="../dataset_crawler-google-places_2026-01-22_05-33-25-536.json",
        output_json="advanced_analysis.json",
        limit=5
    ))
