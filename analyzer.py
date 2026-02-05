"""
Website Analyzer for Tour Agencies
Scores websites on key functionalities using Playwright
"""

import asyncio
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from urllib.parse import urlparse
import re

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install")
    raise


@dataclass
class TourWebsiteScore:
    """Scoring rubric for tour websites"""
    url: str
    company_name: str
    
    # Core Functionality (40 points)
    has_online_booking: bool = False  # 10 pts
    has_payment_system: bool = False  # 10 pts
    has_contact_form: bool = False    # 5 pts
    has_live_chat: bool = False       # 5 pts
    has_reviews: bool = False         # 5 pts
    has_faq: bool = False             # 5 pts
    
    # Content Quality (30 points)
    has_tour_listings: bool = False   # 10 pts
    has_pricing: bool = False         # 10 pts
    has_descriptions: bool = False    # 5 pts
    has_photos: bool = False          # 5 pts
    
    # Technical (20 points)
    mobile_friendly: bool = False     # 10 pts
    ssl_secure: bool = False          # 5 pts
    fast_loading: bool = False        # 5 pts
    
    # Trust Signals (10 points)
    has_phone: bool = False           # 3 pts
    has_email: bool = False           # 3 pts
    has_address: bool = False         # 2 pts
    has_social_links: bool = False    # 2 pts
    
    # Extracted data
    extracted_phone: str = ""
    extracted_email: str = ""
    extracted_address: str = ""
    extracted_description: str = ""
    
    @property
    def total_score(self) -> int:
        score = 0
        # Core Functionality
        score += 10 if self.has_online_booking else 0
        score += 10 if self.has_payment_system else 0
        score += 5 if self.has_contact_form else 0
        score += 5 if self.has_live_chat else 0
        score += 5 if self.has_reviews else 0
        score += 5 if self.has_faq else 0
        # Content
        score += 10 if self.has_tour_listings else 0
        score += 10 if self.has_pricing else 0
        score += 5 if self.has_descriptions else 0
        score += 5 if self.has_photos else 0
        # Technical
        score += 10 if self.mobile_friendly else 0
        score += 5 if self.ssl_secure else 0
        score += 5 if self.fast_loading else 0
        # Trust
        score += 3 if self.has_phone else 0
        score += 3 if self.has_email else 0
        score += 2 if self.has_address else 0
        score += 2 if self.has_social_links else 0
        return score
    
    @property
    def grade(self) -> str:
        if self.total_score >= 90:
            return "A+"
        elif self.total_score >= 80:
            return "A"
        elif self.total_score >= 70:
            return "B"
        elif self.total_score >= 60:
            return "C"
        elif self.total_score >= 50:
            return "D"
        else:
            return "F"
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['total_score'] = self.total_score
        data['grade'] = self.grade
        return data


class TourWebsiteAnalyzer:
    """Analyzes tour websites for functionality and extracts key info"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        
    async def init(self):
        """Initialize browser"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            self.browser = None
    
    async def analyze_website(self, url: str, company_name: str) -> TourWebsiteScore:
        """Analyze a single website"""
        if not self.browser:
            await self.init()
            
        score = TourWebsiteScore(url=url, company_name=company_name)
        
        # Check SSL
        score.ssl_secure = url.startswith('https://')
        
        try:
            page = await self.browser.new_page(viewport={'width': 1280, 'height': 800})
            
            # Set timeout for slow sites
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Check loading speed
            if response:
                timing = await page.evaluate("""() => {
                    const nav = performance.getEntriesByType('navigation')[0];
                    return nav ? nav.loadEventEnd - nav.loadEventStart : 9999;
                }""")
                score.fast_loading = timing < 3000  # Under 3 seconds
            
            # Get page content
            content = await page.content()
            text_content = await page.evaluate("() => document.body.innerText")
            text_lower = text_content.lower()
            
            # Check for booking functionality
            score.has_online_booking = await self._check_booking(page, content)
            score.has_payment_system = self._check_payment(content)
            
            # Check contact features
            score.has_contact_form = 'contact' in text_lower and ('form' in text_lower or '<form' in content)
            score.has_live_chat = self._check_live_chat(content)
            score.has_phone = bool(re.search(r'\+\d[\d\s\-\(\)]{7,20}', text_content))
            score.has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', text_content))
            score.has_address = any(word in text_lower for word in ['via ', 'street', 'avenue', 'address', 'rome', 'italy'])
            score.has_social_links = any(social in content.lower() for social in ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com'])
            
            # Check content
            score.has_tour_listings = any(word in text_lower for word in ['tour', 'tickets', 'book', 'experience'])
            score.has_pricing = '€' in text_content or 'price' in text_lower or 'from' in text_lower
            score.has_descriptions = len(text_content) > 500
            score.has_photos = '<img' in content and content.count('<img') > 3
            
            # Check reviews and FAQ
            score.has_reviews = any(word in text_lower for word in ['review', 'testimonial', 'rating', 'tripadvisor', 'google'])
            score.has_faq = 'faq' in text_lower or 'frequently asked' in text_lower
            
            # Check mobile friendly (viewport meta)
            score.mobile_friendly = 'viewport' in content.lower() and 'width=device-width' in content.lower()
            
            # Extract contact info
            score.extracted_phone = self._extract_phone(text_content)
            score.extracted_email = self._extract_email(text_content)
            score.extracted_address = self._extract_address(text_content)
            score.extracted_description = self._extract_description(text_content)
            
            await page.close()
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
            
        return score
    
    async def _check_booking(self, page: Page, content: str) -> bool:
        """Check if site has online booking capability"""
        booking_keywords = ['book now', 'add to cart', 'checkout', 'availability', 'calendar', 
                           'select date', 'choose date', 'reserve', 'booking form']
        content_lower = content.lower()
        return any(kw in content_lower for kw in booking_keywords)
    
    def _check_payment(self, content: str) -> bool:
        """Check for payment system indicators"""
        payment_keywords = ['stripe', 'paypal', 'credit card', 'payment', 'checkout', 
                           'mastercard', 'visa', 'american express']
        return any(kw in content.lower() for kw in payment_keywords)
    
    def _check_live_chat(self, content: str) -> bool:
        """Check for live chat widgets"""
        chat_indicators = ['tidio', 'intercom', 'zendesk', 'livechat', 'tawk', 'chatwoot',
                          'crisp', 'hubspot', 'drift', 'chat widget']
        return any(ind in content.lower() for ind in chat_indicators)
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text"""
        patterns = [
            r'\+39\s?\d{2,3}[\s\-]?\d{3}[\s\-]?\d{4}',  # Italian
            r'\+\d[\d\s\-\(\)]{7,15}',  # General international
            r'\(\d{3}\)\s?\d{3}[\s\-]?\d{4}',  # US format
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        pattern = r'[\w.-]+@[\w.-]+\.\w+'
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_address(self, text: str) -> str:
        """Extract address from text"""
        # Look for Via/Viale patterns (Italian addresses)
        patterns = [
            r'Via\s+[\w\s]+,?\s*\d+[^.\n]*(?:Rome|Italy)',
            r'Viale\s+[\w\s]+,?\s*\d+[^.\n]*',
            r'Piazza\s+[\w\s]+,?\s*\d+[^.\n]*',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return ""
    
    def _extract_description(self, text: str) -> str:
        """Extract a short description from the website"""
        # Look for tagline or mission statement patterns
        sentences = text.split('.')
        for sent in sentences:
            sent = sent.strip()
            if 50 < len(sent) < 200 and any(word in sent.lower() for word in 
                ['tour', 'experience', 'rome', 'vatican', 'travel', 'visit', 'explore', 'guide']):
                return sent
        # Fallback to first substantial sentence
        for sent in sentences:
            sent = sent.strip()
            if len(sent) > 50:
                return sent[:200]
        return ""


async def analyze_companies(companies_json_path: str, output_path: str, limit: int = None):
    """Analyze all companies from JSON file"""
    
    # Load companies
    with open(companies_json_path, 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    if limit:
        companies = companies[:limit]
    
    analyzer = TourWebsiteAnalyzer()
    results = []
    
    print(f"Analyzing {len(companies)} websites...")
    
    for i, company in enumerate(companies, 1):
        url = company.get('website', '')
        if not url or not url.startswith('http'):
            print(f"[{i}/{len(companies)}] Skipping {company.get('title', 'Unknown')} - no valid URL")
            continue
            
        print(f"[{i}/{len(companies)}] Analyzing {company.get('title', 'Unknown')}...")
        
        try:
            score = await analyzer.analyze_website(url, company.get('title', 'Unknown'))
            results.append(score.to_dict())
            print(f"    Score: {score.total_score}/100 (Grade: {score.grade})")
        except Exception as e:
            print(f"    Error: {e}")
    
    await analyzer.close()
    
    # Save results
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to {output_path}")
    
    # Print summary
    if results:
        avg_score = sum(r['total_score'] for r in results) / len(results)
        print(f"\nAverage Score: {avg_score:.1f}/100")
        print(f"Highest: {max(r['total_score'] for r in results)}/100")
        print(f"Lowest: {min(r['total_score'] for r in results)}/100")


if __name__ == "__main__":
    import sys
    
    # Analyze first 5 companies as a test
    asyncio.run(analyze_companies(
        companies_json_path="../dataset_crawler-google-places_2026-01-22_05-33-25-536.json",
        output_path="analysis_results.json",
        limit=5  # Start with 5 for testing
    ))
