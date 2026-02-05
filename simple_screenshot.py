"""
Simple Screenshot Comparison - No modifications, just captures
Use this if you just want to screenshot existing websites
"""

import asyncio
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("pip install playwright && playwright install chromium")
    raise


async def screenshot_website(url: str, output_path: Path, width: int = 1280, height: int = 2000):
    """Take a screenshot of a website"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': width, 'height': height})
        
        try:
            print(f"  Loading {url}...")
            await page.goto(url, wait_until='networkidle', timeout=45000)
            await page.wait_for_timeout(3000)  # Let animations/content load
            
            # Screenshot
            await page.screenshot(path=str(output_path), full_page=False)
            print(f"  Saved: {output_path}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        await browser.close()
    
    return output_path


def create_gif(image_paths: list, output_path: Path, duration: int = 2000):
    """Create animated GIF from images"""
    
    images = []
    for path in image_paths:
        img = Image.open(path)
        # Ensure consistent size
        img = img.resize((1280, 2000), Image.Resampling.LANCZOS)
        images.append(img.convert('RGB'))
    
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0
    )
    print(f"GIF saved: {output_path}")


def create_side_by_side(img1_path: Path, img2_path: Path, output_path: Path, title: str = None):
    """Create side-by-side comparison"""
    
    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Resize to same height
    target_height = 2000
    img1 = img1.resize((1280, target_height), Image.Resampling.LANCZOS)
    img2 = img2.resize((1280, target_height), Image.Resampling.LANCZOS)
    
    # Create combined
    gap = 20
    combined = Image.new('RGB', (1280 * 2 + gap, target_height + 150), '#f5f5f5')
    
    draw = ImageDraw.Draw(combined)
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        label_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Title
    if title:
        bbox = draw.textbbox((0, 0), title, font=title_font)
        x = ((1280 * 2 + gap) - (bbox[2] - bbox[0])) // 2
        draw.text((x, 20), title, fill='#1a1a1a', font=title_font)
    
    # Labels
    draw.text((500, 90), "CURRENT WEBSITE", fill='#dc2626', font=label_font)
    draw.text((1280 + gap + 450, 90), "NEW PREMIUM DESIGN", fill='#059669', font=label_font)
    
    # Paste images
    combined.paste(img1, (0, 150))
    combined.paste(img2, (1280 + gap, 150))
    
    combined.save(output_path, quality=95)
    print(f"Comparison saved: {output_path}")


async def compare_two_urls(old_url: str, new_url: str, company_name: str, output_dir: str = "./comparisons"):
    """Compare two websites side by side"""
    
    out = Path(output_dir)
    out.mkdir(exist_ok=True)
    
    safe_name = "".join(c for c in company_name if c.isalnum() or c in ' -_').strip().replace(' ', '-').lower()
    comp_dir = out / safe_name
    comp_dir.mkdir(exist_ok=True)
    
    print(f"\nComparing: {company_name}")
    print("-" * 50)
    
    # Screenshot both
    old_img = comp_dir / "current.png"
    new_img = comp_dir / "new_design.png"
    
    await screenshot_website(old_url, old_img)
    await screenshot_website(new_url, new_img)
    
    # Create comparisons
    create_side_by_side(old_img, new_img, comp_dir / "comparison.png", company_name)
    create_gif([old_img, new_img], comp_dir / "animated.gif")
    
    print(f"Results in: {comp_dir}")
    return comp_dir


async def batch_compare(companies: list, new_url_base: str = "http://localhost:3000"):
    """Compare multiple companies"""
    
    all_results = []
    
    for company in companies:
        comp_dir = await compare_two_urls(
            old_url=company['website'],
            new_url=new_url_base,
            company_name=company['name']
        )
        all_results.append({
            'company_name': company['name'],
            'website': company['website'],
            'folder': str(comp_dir),
            'gif': str(comp_dir / "animated.gif"),
            'comparison': str(comp_dir / "comparison.png"),
            'old_screenshot': str(comp_dir / "current.png"),
            'new_screenshot': str(comp_dir / "new_design.png")
        })
    
    # Save manifest
    with open('comparisons/screenshot_manifest.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nManifest saved to: comparisons/screenshot_manifest.json")
    return all_results


if __name__ == "__main__":
    import json
    
    # Example: Compare from analysis results
    with open('analysis_results.json') as f:
        data = json.load(f)[:3]  # First 3
    
    companies = [{
        'name': d['company_name'],
        'website': d['url']
    } for d in data]
    
    print("""
    ===========================================
    Website Screenshot Comparison
    ===========================================
    
    Make sure your dev server is running on localhost:3000!
    
    Press Ctrl+C to cancel, or
    Press any key to continue...
    """)
    input()
    
    asyncio.run(batch_compare(companies))
