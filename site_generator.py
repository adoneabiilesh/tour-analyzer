"""
Site Generator - Creates white-labeled tour websites
Customizes only header/home content, keeps products intact
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
from slugify import slugify


@dataclass
class CompanyInfo:
    """Company data for customization"""
    name: str
    description: str
    tagline: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    website: str = ""
    original_score: int = 0


class SiteGenerator:
    """Generates customized websites from template"""
    
    def __init__(self, template_path: str, output_base_path: str):
        self.template_path = Path(template_path)
        self.output_base_path = Path(output_base_path)
        
    def generate_site(self, company: CompanyInfo) -> str:
        """Generate a new site for a company"""
        
        # Create output directory
        safe_name = slugify(company.name)
        output_dir = self.output_base_path / safe_name
        
        # Remove if exists
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        # Copy template (ignore build artifacts and git)
        def ignore_patterns(dir, files):
            return shutil.ignore_patterns('node_modules', '.next', '.vercel', '.git')(dir, files)
        
        shutil.copytree(self.template_path, output_dir, ignore=ignore_patterns)
        
        # Customize files
        self._customize_layout(output_dir, company)
        self._customize_hero(output_dir, company)
        self._customize_footer(output_dir, company)
        self._customize_page_content(output_dir, company)
        
        return str(output_dir)
    
    def _customize_layout(self, output_dir: Path, company: CompanyInfo):
        """Customize layout.tsx with company metadata"""
        layout_path = output_dir / "src" / "app" / "layout.tsx"
        
        if not layout_path.exists():
            print(f"Warning: layout.tsx not found at {layout_path}")
            return
        
        content = layout_path.read_text(encoding='utf-8')
        
        # Generate new metadata
        title = f"{company.name} | Official Tours & Tickets"
        description = (company.description or f"Book official tours with {company.name}. Skip-the-line access to Vatican, Colosseum and Rome's top attractions.")
        # Sanitize for JS string
        description = description.replace('\\', '\\').replace('"', '\\"').replace('\n', ' ').replace('\r', ' ').strip()[:200]
        
        # Replace metadata
        content = self._replace_between(content, 
            'export const metadata: Metadata = {',
            '};',
            f'''  title: "{title}",
  description: "{description}",
  icons: {{
    icon: '/logo.png',
    shortcut: '/logo.png',
    apple: '/logo.png',
  }},
  other: {{
    'viewport': 'width=device-width, initial-scale=1, maximum-scale=1',
  }}''')
        
        layout_path.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated layout.tsx")
    
    def _customize_hero(self, output_dir: Path, company: CompanyInfo):
        """Customize Hero component with company branding"""
        hero_path = output_dir / "src" / "components" / "Hero.tsx"
        
        if not hero_path.exists():
            print(f"Warning: Hero.tsx not found")
            return
        
        content = hero_path.read_text(encoding='utf-8')
        
        # Generate tagline based on company name and description
        tagline = company.tagline or self._generate_tagline(company.name, company.description)
        subtitle = company.description[:150] if len(company.description) > 50 else \
            f"Private access to the Colosseum, Vatican, and hidden gems with {company.name}. Experience Rome without the crowds."
        
        # Replace the default title/hero content
        # Change "Rome, Curated." subtitle
        content = content.replace(
            'Rome, Curated.',
            f'{company.name.split()[0]}, Curated.'
        )
        
        # Replace the default subtitle
        old_subtitle = "Private access to the Colosseum, Vatican, and hidden gems. Experience Rome without the crowds."
        subtitle = subtitle.replace('\n', ' ').replace('\r', ' ').replace('"', '\\"')[:200]
        content = content.replace(old_subtitle, subtitle)
        
        hero_path.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated Hero.tsx")
    
    def _customize_footer(self, output_dir: Path, company: CompanyInfo):
        """Customize Footer with company contact info"""
        footer_path = output_dir / "src" / "components" / "Footer.tsx"
        
        if not footer_path.exists():
            print(f"Warning: Footer.tsx not found")
            return
        
        content = footer_path.read_text(encoding='utf-8')
        
        # Update company name in footer
        content = content.replace(
            'Tickets in <span className="text-emerald-500">Rome</span>',
            f'{company.name.split()[0]} <span className="text-emerald-500">{" ".join(company.name.split()[1:]) or "Tours"}</span>'
        )
        
        # Update description
        old_desc = "Your premier gateway to the Eternal City. Experience Rome with our expert guides, skip-the-line access, and unforgettable customized journeys."
        new_desc = company.description or f"Your premier gateway to Rome. Experience the Eternal City with {company.name} - expert guides, skip-the-line access, and unforgettable journeys."
        new_desc = new_desc.replace('\n', ' ').replace('\r', ' ').replace('"', '\\"')[:180]
        content = content.replace(old_desc, new_desc)
        
        # Update contact info if available
        if company.phone:
            content = content.replace('+39 351 419 9425', company.phone)
        if company.email:
            content = content.replace('info@ticketsinrome.com', company.email)
        if company.address:
            content = content.replace('Via Tunisi 43,<br />Rome, Italy', company.address.replace(', ', '<br />'))
        
        # Update copyright
        content = content.replace(
            'Tickets in Rome. All rights reserved.',
            f'{company.name}. All rights reserved.'
        )
        
        # Update company details
        content = content.replace(
            '<span className="font-medium text-stone-500">Tickets in Rome</span>',
            f'<span className="font-medium text-stone-500">{company.name}</span>'
        )
        
        footer_path.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated Footer.tsx")
    
    def _customize_page_content(self, output_dir: Path, company: CompanyInfo):
        """Customize main page content - section titles"""
        page_path = output_dir / "src" / "app" / "page.tsx"
        
        if not page_path.exists():
            print(f"Warning: page.tsx not found")
            return
        
        content = page_path.read_text(encoding='utf-8')
        
        # Customize section titles to be more generic/company-branded
        replacements = {
            'Skip the line to the Sistine Chapel, Gardens, and the Dome.':
                f'Discover the Vatican with {company.name}. Skip-the-line to the Sistine Chapel, Gardens, and the Dome.',
            
            'Walk in the footsteps of Gladiators. Arena, Underground, and Forum.':
                f'Walk in the footsteps of Gladiators with {company.name}. Arena, Underground, and Forum access.',
            
            'Explore the Pantheon, Trevi Fountain, Spanish Steps and iconic squares.':
                f'Explore Rome\'s iconic squares with {company.name}. Pantheon, Trevi Fountain, Spanish Steps and more.',
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        page_path.write_text(content, encoding='utf-8')
        print(f"  [OK] Updated page.tsx")
    
    def _generate_tagline(self, name: str, description: str) -> str:
        """Generate a catchy tagline"""
        taglines = [
            f"Experience Rome with {name}",
            f"{name} - Your Gateway to Rome",
            f"Discover Rome with {name}",
            f"Rome's Best Tours with {name}",
        ]
        return taglines[0]
    
    def _replace_between(self, content: str, start_marker: str, end_marker: str, new_content: str) -> str:
        """Replace content between markers"""
        start_idx = content.find(start_marker)
        if start_idx == -1:
            return content
        
        end_idx = content.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1:
            return content
        
        return content[:start_idx + len(start_marker)] + "\n" + new_content + "\n" + content[end_idx:]


def generate_sites(analysis_results_path: str, template_path: str, output_path: str, limit: int = None):
    """Generate sites from analysis results"""
    
    # Load analysis results
    with open(analysis_results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    if limit:
        results = results[:limit]
    
    generator = SiteGenerator(template_path, output_path)
    generated = []
    
    print(f"\nGenerating {len(results)} websites...\n")
    
    for i, result in enumerate(results, 1):
        company = CompanyInfo(
            name=result['company_name'],
            description=result.get('extracted_description', ''),
            phone=result.get('extracted_phone', ''),
            email=result.get('extracted_email', ''),
            address=result.get('extracted_address', ''),
            website=result['url'],
            original_score=result.get('total_score', 0)
        )
        
        print(f"[{i}/{len(results)}] Generating site for {company.name}...")
        
        try:
            site_path = generator.generate_site(company)
            generated.append({
                'name': company.name,
                'path': site_path,
                'original_score': company.original_score
            })
            print(f"    [OK] Created: {site_path}\n")
        except Exception as e:
            print(f"    [ERR] Error: {e}\n")
    
    # Save manifest
    manifest_path = Path(output_path) / "generated_sites.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(generated, f, indent=2)
    
    print(f"\nGenerated {len(generated)} sites in {output_path}")
    print(f"Manifest saved to {manifest_path}")
    
    return generated


if __name__ == "__main__":
    generate_sites(
        analysis_results_path="analysis_results.json",
        template_path="../rome-tour-tickets",
        output_path="./generated-sites",
        limit=3  # Start with 3 for testing
    )
