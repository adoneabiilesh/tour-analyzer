"""
Visual Comparison Recorder
Captures screenshots of old vs new websites and creates comparison GIFs/videos
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

try:
    from playwright.async_api import async_playwright, Page, Browser
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install")
    raise

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not installed. Run: pip install pillow")
    raise


@dataclass
class ComparisonConfig:
    """Configuration for visual comparison"""
    old_url: str
    new_url: str  # Local dev server URL
    company_name: str
    output_dir: str
    

class VisualRecorder:
    """Records and compares website screenshots"""
    
    def __init__(self):
        self.browser: Browser = None
        
    async def init(self):
        """Initialize browser"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=True)
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
    
    async def capture_comparison(self, config: ComparisonConfig) -> Dict[str, str]:
        """Capture old vs new website screenshots"""
        
        output_path = Path(config.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        safe_name = "".join(c for c in config.company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '-').lower()
        
        results = {}
        
        # Capture old website
        print(f"  Capturing OLD website: {config.old_url}")
        old_screenshot = await self._capture_screenshot(
            config.old_url, 
            output_path / f"{safe_name}_old.png",
            label="BEFORE (Original)"
        )
        results['old_screenshot'] = str(old_screenshot)
        
        # Capture new website (if URL provided)
        if config.new_url:
            print(f"  Capturing NEW website: {config.new_url}")
            new_screenshot = await self._capture_screenshot(
                config.new_url,
                output_path / f"{safe_name}_new.png",
                label="AFTER (Redesigned)"
            )
            results['new_screenshot'] = str(new_screenshot)
            
            # Create side-by-side comparison
            comparison_path = await self._create_side_by_side(
                old_screenshot, new_screenshot, 
                output_path / f"{safe_name}_comparison.png",
                config.company_name
            )
            results['comparison'] = str(comparison_path)
            
            # Create animated GIF
            gif_path = await self._create_animated_gif(
                [old_screenshot, new_screenshot],
                output_path / f"{safe_name}_animated.gif"
            )
            results['animated_gif'] = str(gif_path)
        
        return results
    
    async def _capture_screenshot(self, url: str, output_file: Path, label: str = None) -> Path:
        """Capture a full-page screenshot with optional label"""
        
        page = await self.browser.new_page(viewport={'width': 1280, 'height': 800})
        
        try:
            # Navigate to page
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            # Wait for content to load
            await page.wait_for_timeout(2000)
            
            # Scroll to trigger lazy loading
            await page.evaluate("""async () => {
                await new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 100;
                    const timer = setInterval(() => {
                        const scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        
                        if (totalHeight >= scrollHeight) {
                            clearInterval(timer);
                            window.scrollTo(0, 0);
                            resolve();
                        }
                    }, 50);
                });
            }""")
            
            await page.wait_for_timeout(1000)
            
            # Get full page height
            height = await page.evaluate('() => document.body.scrollHeight')
            
            # Set viewport to capture full page (up to 4000px max)
            capture_height = min(height, 4000)
            await page.set_viewport_size({'width': 1280, 'height': capture_height})
            
            # Take screenshot
            await page.screenshot(path=str(output_file), full_page=False)
            
            # Add label if provided
            if label:
                await self._add_label_to_image(output_file, label)
            
        except Exception as e:
            print(f"    Warning: Error capturing {url}: {e}")
            # Create placeholder image on error
            await self._create_placeholder_image(output_file, label or "Error")
        
        await page.close()
        return output_file
    
    async def _add_label_to_image(self, image_path: Path, label: str):
        """Add a label banner to the top of the image"""
        
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Banner height
        banner_height = 40
        
        # Create new image with banner
        new_img = Image.new('RGB', (img.width, img.height + banner_height), '#1a1a1a')
        new_img.paste(img, (0, banner_height))
        
        draw = ImageDraw.Draw(new_img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) // 2
        y = (banner_height - (bbox[3] - bbox[1])) // 2
        
        draw.text((x, y), label, fill='white', font=font)
        
        new_img.save(image_path, quality=90)
    
    async def _create_side_by_side(self, old_img_path: Path, new_img_path: Path, 
                                   output_path: Path, company_name: str) -> Path:
        """Create side-by-side comparison image"""
        
        old_img = Image.open(old_img_path)
        new_img = Image.open(new_img_path)
        
        # Resize to same height
        max_height = min(max(old_img.height, new_img.height), 3000)
        
        old_ratio = old_img.width / old_img.height
        new_ratio = new_img.width / new_img.height
        
        old_new_height = min(max_height, old_img.height)
        new_new_height = min(max_height, new_img.height)
        
        old_img = old_img.resize((int(old_new_height * old_ratio), old_new_height), Image.Resampling.LANCZOS)
        new_img = new_img.resize((int(new_new_height * new_ratio), new_new_height), Image.Resampling.LANCZOS)
        
        # Create combined image
        total_width = old_img.width + new_img.width + 20  # 20px gap
        max_h = max(old_img.height, new_img.height)
        
        combined = Image.new('RGB', (total_width, max_h + 60), '#f5f5f5')  # Extra for header
        
        # Add header
        draw = ImageDraw.Draw(combined)
        try:
            font = ImageFont.truetype("arial.ttf", 28)
            small_font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Title
        title = f"{company_name} - Website Transformation"
        bbox = draw.textbbox((0, 0), title, font=font)
        title_width = bbox[2] - bbox[0]
        draw.text(((total_width - title_width) // 2, 15), title, fill='#1a1a1a', font=font)
        
        # Labels
        draw.text((old_img.width // 2 - 40, 50), "BEFORE", fill='#666666', font=small_font)
        draw.text((old_img.width + 20 + new_img.width // 2 - 30, 50), "AFTER", fill='#059669', font=small_font)
        
        # Paste images
        combined.paste(old_img, (0, 60))
        combined.paste(new_img, (old_img.width + 20, 60))
        
        # Save
        combined.save(output_path, quality=90)
        return output_path
    
    async def _create_animated_gif(self, image_paths: List[Path], output_path: Path, 
                                   duration: int = 2000) -> Path:
        """Create animated GIF switching between images"""
        
        images = []
        for path in image_paths:
            img = Image.open(path)
            # Resize to consistent size
            img = img.resize((1280, min(img.height, 2000)), Image.Resampling.LANCZOS)
            images.append(img.convert('RGB'))
        
        # Save as GIF
        images[0].save(
            output_path,
            save_all=True,
            append_images=images[1:],
            duration=duration,  # ms per frame
            loop=0  # Infinite loop
        )
        
        return output_path
    
    async def _create_placeholder_image(self, output_path: Path, text: str):
        """Create a placeholder image when screenshot fails"""
        
        img = Image.new('RGB', (1280, 800), '#f3f4f6')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1280 - text_width) // 2
        y = (800 - text_height) // 2
        
        draw.text((x, y), text, fill='#6b7280', font=font)
        img.save(output_path)


async def record_comparisons(manifest_path: str, output_dir: str, dev_server_base: str = "http://localhost:3000"):
    """Record comparisons for all generated sites"""
    
    # Load manifest
    with open(manifest_path, 'r', encoding='utf-8') as f:
        sites = json.load(f)
    
    recorder = VisualRecorder()
    await recorder.init()
    
    results = []
    
    print(f"\nRecording {len(sites)} visual comparisons...\n")
    
    for i, site in enumerate(sites, 1):
        print(f"[{i}/{len(sites)}] Recording {site['name']}...")
        
        config = ComparisonConfig(
            old_url=site.get('website', ''),
            new_url=f"{dev_server_base}/{Path(site['path']).name}",
            company_name=site['name'],
            output_dir=output_dir
        )
        
        try:
            result = await recorder.capture_comparison(config)
            results.append({
                'name': site['name'],
                **result
            })
            print(f"    ✓ Comparison saved\n")
        except Exception as e:
            print(f"    ✗ Error: {e}\n")
    
    await recorder.close()
    
    # Save results
    results_path = Path(output_dir) / "comparison_results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAll comparisons saved to {output_dir}")
    print(f"Results manifest: {results_path}")
    
    return results


if __name__ == "__main__":
    # Example usage
    asyncio.run(record_comparisons(
        manifest_path="./generated-sites/generated_sites.json",
        output_dir="./comparisons",
        dev_server_base="http://localhost:3000"
    ))
