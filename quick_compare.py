"""
Quick Website Comparison Tool
Modifies template in-place, screenshots old vs new, creates GIF, then restores.
"""

import asyncio
import json
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

try:
    from playwright.async_api import async_playwright
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Run: pip install playwright pillow python-slugify")
    print("Then: playwright install chromium")
    raise


@dataclass
class Company:
    name: str
    website: str
    phone: str = ""
    email: str = ""
    address: str = ""
    description: str = ""


class QuickComparer:
    """Quickly compare old website vs customized template"""
    
    def __init__(self, template_path: str, output_dir: str):
        self.template_path = Path(template_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Files we will modify
        self.files_to_modify = {
            'layout': self.template_path / "src" / "app" / "layout.tsx",
            'hero': self.template_path / "src" / "components" / "Hero.tsx",
            'footer': self.template_path / "src" / "components" / "Footer.tsx",
            'page': self.template_path / "src" / "app" / "page.tsx",
        }
        
        # Store original content
        self.originals = {}
        
    def backup_originals(self):
        """Backup original files"""
        for name, filepath in self.files_to_modify.items():
            if filepath.exists():
                self.originals[name] = filepath.read_text(encoding='utf-8')
                
    def restore_originals(self):
        """Restore original files"""
        for name, content in self.originals.items():
            filepath = self.files_to_modify[name]
            filepath.write_text(content, encoding='utf-8')
        print("Restored original files")
    
    def customize_for_company(self, company: Company):
        """Customize template files for a company"""
        
        # 1. Customize layout.tsx (title and meta)
        layout_path = self.files_to_modify['layout']
        content = self.originals['layout']
        
        title = f"{company.name} | Official Tours & Tickets"
        description = company.description[:160] if company.description else f"Book official tours with {company.name}. Skip-the-line access to Rome's top attractions."
        description = description.replace('"', '\\"').replace('\n', ' ')
        
        # Replace metadata
        content = content.replace(
            'title: "TicketsInRome | Official Vatican & Colosseum Tours"',
            f'title: "{title}"'
        )
        content = content.replace(
            'description: "Exclusive skip-the-line tours for the Vatican Museums, Sistine Chapel, and St. Peter\'s Basilica. Book your official ticketsinrome experience today."',
            f'description: "{description}"'
        )
        layout_path.write_text(content, encoding='utf-8')
        
        # 2. Customize Hero.tsx
        hero_path = self.files_to_modify['hero']
        content = self.originals['hero']
        
        # Change subtitle
        content = content.replace(
            '"Rome, Curated."',
            f'"{company.name.split()[0]}, Curated."'
        )
        
        # Change main subtitle text
        old_sub = "Private access to the Colosseum, Vatican, and hidden gems. Experience Rome without the crowds."
        new_sub = f"Experience Rome with {company.name}. Skip-the-line access to the Vatican, Colosseum, and hidden gems."
        content = content.replace(old_sub, new_sub)
        hero_path.write_text(content, encoding='utf-8')
        
        # 3. Customize Footer.tsx
        footer_path = self.files_to_modify['footer']
        content = self.originals['footer']
        
        # Company name
        content = content.replace(
            'Tickets in <span className="text-emerald-500">Rome</span>',
            f'{company.name.split()[0]} <span className="text-emerald-500">{" ".join(company.name.split()[1:]) or "Tours"}</span>'
        )
        
        # Description
        old_desc = "Your premier gateway to the Eternal City. Experience Rome with our expert guides, skip-the-line access, and unforgettable customized journeys."
        new_desc = f"Your premier gateway to Rome. Experience the Eternal City with {company.name} - expert guides and unforgettable journeys."
        content = content.replace(old_desc, new_desc)
        
        # Contact info
        if company.phone:
            content = content.replace('+39 351 419 9425', company.phone)
        if company.email:
            content = content.replace('info@ticketsinrome.com', company.email)
        if company.address:
            addr = company.address.replace(', ', '<br />')
            content = content.replace('Via Tunisi 43,<br />Rome, Italy', addr)
        
        # Copyright
        content = content.replace('Tickets in Rome', company.name)
        footer_path.write_text(content, encoding='utf-8')
        
        # 4. Customize page.tsx (section subtitles)
        page_path = self.files_to_modify['page']
        content = self.originals['page']
        
        # Add company name to section descriptions
        content = content.replace(
            'Skip the line to the Sistine Chapel',
            f'With {company.name} - Skip the line to the Sistine Chapel'
        )
        footer_path.write_text(content, encoding='utf-8')
        
        print(f"Customized for {company.name}")
    
    async def capture_screenshot(self, url: str, output_path: Path, label: str = None):
        """Capture screenshot of a website"""
        
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1280, 'height': 2000})
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(2000)  # Let animations settle
                
                # Scroll to load lazy content
                await page.evaluate("window.scrollTo(0, 500)")
                await page.wait_for_timeout(500)
                
                # Screenshot (above fold only for comparison)
                await page.screenshot(path=str(output_path), full_page=False)
                
                # Add label
                if label:
                    await self._add_label(output_path, label)
                
            except Exception as e:
                print(f"    Screenshot error: {e}")
                # Create placeholder
                self._create_placeholder(output_path, label or "Error")
            
            await browser.close()
        
        return output_path
    
    async def _add_label(self, image_path: Path, label: str):
        """Add label banner to screenshot"""
        img = Image.open(image_path)
        banner_height = 40
        
        new_img = Image.new('RGB', (img.width, img.height + banner_height), '#1a1a1a')
        new_img.paste(img, (0, banner_height))
        
        draw = ImageDraw.Draw(new_img)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), label, font=font)
        x = (img.width - (bbox[2] - bbox[0])) // 2
        y = (banner_height - (bbox[3] - bbox[1])) // 2
        
        draw.text((x, y), label, fill='white', font=font)
        new_img.save(image_path, quality=90)
    
    def _create_placeholder(self, path: Path, text: str):
        """Create placeholder error image"""
        img = Image.new('RGB', (1280, 2000), '#f3f4f6')
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        draw.text((500, 900), text, fill='#6b7280', font=font)
        img.save(path)
    
    def create_comparison_gif(self, old_img: Path, new_img: Path, output_path: Path, company_name: str):
        """Create animated GIF comparing old vs new"""
        
        img1 = Image.open(old_img)
        img2 = Image.open(new_img)
        
        # Ensure same size
        target_height = min(img1.height, img2.height, 1600)
        img1 = img1.resize((1280, target_height), Image.Resampling.LANCZOS)
        img2 = img2.resize((1280, target_height), Image.Resampling.LANCZOS)
        
        # Create frames with labels
        frames = []
        
        # Frame 1: Old
        f1 = img1.copy()
        draw = ImageDraw.Draw(f1)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        draw.rectangle([20, 20, 300, 80], fill='#dc2626')
        draw.text((35, 30), "BEFORE", fill='white', font=font)
        frames.append(f1)
        
        # Frame 2: Transition
        blend = Image.blend(img1.convert('RGB'), img2.convert('RGB'), alpha=0.5)
        frames.append(blend)
        
        # Frame 3: New
        f2 = img2.copy()
        draw = ImageDraw.Draw(f2)
        draw.rectangle([20, 20, 250, 80], fill='#059669')
        draw.text((35, 30), "AFTER", fill='white', font=font)
        frames.append(f2)
        
        # Save GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=1500,  # 1.5 seconds per frame
            loop=0
        )
        
        return output_path
    
    def create_side_by_side(self, old_img: Path, new_img: Path, output_path: Path, company_name: str):
        """Create side-by-side comparison image"""
        
        img1 = Image.open(old_img)
        img2 = Image.open(new_img)
        
        # Resize to consistent height
        target_height = min(img1.height, img2.height, 1600)
        img1 = img1.resize((1280, target_height), Image.Resampling.LANCZOS)
        img2 = img2.resize((1280, target_height), Image.Resampling.LANCZOS)
        
        # Create combined image with gap
        gap = 20
        total_width = img1.width + img2.width + gap
        combined = Image.new('RGB', (total_width, target_height + 100), '#f5f5f5')
        
        # Header
        draw = ImageDraw.Draw(combined)
        try:
            title_font = ImageFont.truetype("arial.ttf", 36)
            label_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            label_font = ImageFont.load_default()
        
        # Title
        title = f"{company_name} - Website Transformation"
        bbox = draw.textbbox((0, 0), title, font=title_font)
        x = (total_width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 20), title, fill='#1a1a1a', font=title_font)
        
        # Labels
        draw.text((img1.width // 2 - 60, 70), "BEFORE (Current)", fill='#dc2626', font=label_font)
        draw.text((img1.width + gap + img2.width // 2 - 50, 70), "AFTER (New Design)", fill='#059669', font=label_font)
        
        # Paste images
        combined.paste(img1, (0, 100))
        combined.paste(img2, (img1.width + gap, 100))
        
        combined.save(output_path, quality=95)
        return output_path
    
    async def compare_company(self, company: Company, local_url: str = "http://localhost:3000"):
        """Full comparison for one company"""
        
        safe_name = "".join(c for c in company.name if c.isalnum() or c in ' -_').strip().replace(' ', '-').lower()
        comp_dir = self.output_dir / safe_name
        comp_dir.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Comparing: {company.name}")
        print(f"{'='*60}")
        
        # 1. Backup originals
        self.backup_originals()
        
        # 2. Customize template
        self.customize_for_company(company)
        
        # 3. Screenshot old website
        print(f"Capturing OLD: {company.website}")
        old_img = comp_dir / "old.png"
        await self.capture_screenshot(company.website, old_img, "BEFORE")
        
        # 4. Screenshot new (local) - assumes dev server is running
        print(f"Capturing NEW: {local_url}")
        new_img = comp_dir / "new.png"
        await self.capture_screenshot(local_url, new_img, "AFTER")
        
        # 5. Create comparisons
        print("Creating comparison images...")
        
        gif_path = comp_dir / "comparison.gif"
        self.create_comparison_gif(old_img, new_img, gif_path, company.name)
        
        side_path = comp_dir / "side-by-side.png"
        self.create_side_by_side(old_img, new_img, side_path, company.name)
        
        # 6. Restore originals
        self.restore_originals()
        
        print(f"Results saved to: {comp_dir}")
        
        return {
            'company': company.name,
            'old': str(old_img.relative_to(self.output_dir.parent)),
            'new': str(new_img.relative_to(self.output_dir.parent)),
            'gif': str(gif_path.relative_to(self.output_dir.parent)),
            'side_by_side': str(side_path.relative_to(self.output_dir.parent)),
            'folder': str(comp_dir.relative_to(self.output_dir.parent))
        }


async def main():
    """Run comparison on analysis results"""
    
    # Load analysis results
    with open('analysis_results.json', 'r') as f:
        results = json.load(f)
    
    # Take first 3 for testing
    results = results[:3]
    
    comparer = QuickComparer(
        template_path="../rome-tour-tickets",
        output_dir="./comparisons"
    )
    
    print("""
    ===========================================
    WEBSITE COMPARISON TOOL
    ===========================================
    
    IMPORTANT: Make sure your dev server is running!
    
    cd ../rome-tour-tickets
    npm run dev
    
    Then press ENTER to continue...
    """)
    input()
    
    all_results = []
    
    for result in results:
        company = Company(
            name=result['company_name'],
            website=result['url'],
            phone=result.get('extracted_phone', ''),
            email=result.get('extracted_email', ''),
            address=result.get('extracted_address', ''),
            description=result.get('extracted_description', '')
        )
        
        try:
            res = await comparer.compare_company(company)
            # Add additional info from analysis
            res['email'] = result.get('extracted_email', '')
            res['phone'] = result.get('extracted_phone', '')
            res['address'] = result.get('extracted_address', '')
            res['original_score'] = result.get('total_score', 0)
            res['grade'] = result.get('grade', 'N/A')
            res['original_url'] = result.get('url', '')
            all_results.append(res)
        except Exception as e:
            print(f"Error processing {company.name}: {e}")
            # Make sure to restore originals even on error
            comparer.restore_originals()
    
    # Save comprehensive manifest with all info
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_companies': len(all_results),
        'companies': all_results
    }
    
    with open('comparisons/comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # Also save a CSV-friendly version
    csv_data = []
    for r in all_results:
        csv_data.append({
            'company_name': r['company'],
            'email': r.get('email', ''),
            'phone': r.get('phone', ''),
            'website': r.get('original_url', ''),
            'score': r.get('original_score', 0),
            'grade': r.get('grade', ''),
            'gif_path': r.get('gif', ''),
            'comparison_image': r.get('side_by_side', ''),
            'old_screenshot': r.get('old', ''),
            'new_screenshot': r.get('new', '')
        })
    
    with open('comparisons/comparison_summary.json', 'w', encoding='utf-8') as f:
        json.dump(csv_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nCompleted {len(all_results)} comparisons!")
    print(f"Results in: ./comparisons/")
    print(f"Full data: comparison_results.json")
    print(f"Summary: comparison_summary.json")


if __name__ == "__main__":
    asyncio.run(main())
