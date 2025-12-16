"""
Generate PWA icons from base SVG file
Requires: pip install Pillow cairosvg
"""
from pathlib import Path
import cairosvg
from PIL import Image
import io

# Base paths
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'
ICONS_DIR = STATIC_DIR / 'icons'
BASE_ICON = ICONS_DIR / 'icon-base.svg'

# Ensure icons directory exists
ICONS_DIR.mkdir(parents=True, exist_ok=True)

# Icon sizes needed for PWA
ICON_SIZES = [
    # Standard PWA icons
    (16, 16, 'icon-16x16.png'),
    (32, 32, 'icon-32x32.png'),
    (72, 72, 'icon-72x72.png'),
    (96, 96, 'icon-96x96.png'),
    (128, 128, 'icon-128x128.png'),
    (144, 144, 'icon-144x144.png'),
    (152, 152, 'icon-152x152.png'),
    (192, 192, 'icon-192x192.png'),
    (384, 384, 'icon-384x384.png'),
    (512, 512, 'icon-512x512.png'),

    # Apple touch icons
    (180, 180, 'apple-touch-icon.png'),

    # Windows tiles
    (70, 70, 'icon-70x70.png'),
    (150, 150, 'icon-150x150.png'),
    (310, 310, 'icon-310x310.png'),
    (310, 150, 'icon-310x150.png'),

    # Shortcut icons
    (96, 96, 'shortcut-dashboard.png'),
    (96, 96, 'shortcut-projects.png'),
    (96, 96, 'shortcut-finance.png'),

    # Badge and notification icons
    (72, 72, 'badge-72x72.png'),
    (96, 96, 'og-image.png'),
]


def generate_png_from_svg(svg_path, output_path, width, height):
    """Convert SVG to PNG with specified dimensions"""
    try:
        # Convert SVG to PNG bytes
        png_data = cairosvg.svg2png(
            url=str(svg_path),
            output_width=width,
            output_height=height
        )

        # Open with PIL for any additional processing
        img = Image.open(io.BytesIO(png_data))

        # Ensure RGBA mode for transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Save the image
        img.save(output_path, 'PNG', optimize=True)
        print(f'✓ Generated {output_path.name} ({width}x{height})')
        return True

    except Exception as e:
        print(f'✗ Failed to generate {output_path.name}: {e}')
        return False


def create_favicon_ico():
    """Create favicon.ico with multiple sizes"""
    try:
        sizes = [(16, 16), (32, 32), (48, 48)]
        images = []

        for width, height in sizes:
            png_data = cairosvg.svg2png(
                url=str(BASE_ICON),
                output_width=width,
                output_height=height
            )
            img = Image.open(io.BytesIO(png_data))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            images.append(img)

        # Save as ICO
        ico_path = ICONS_DIR / 'favicon.ico'
        images[0].save(
            ico_path,
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        print(f'✓ Generated favicon.ico')
        return True

    except Exception as e:
        print(f'✗ Failed to generate favicon.ico: {e}')
        return False


def create_safari_pinned_tab():
    """Create Safari pinned tab SVG (monochrome)"""
    try:
        # For now, just copy the base SVG
        # In production, you'd want a monochrome version
        import shutil
        safari_icon = ICONS_DIR / 'safari-pinned-tab.svg'
        shutil.copy(BASE_ICON, safari_icon)
        print(f'✓ Generated safari-pinned-tab.svg')
        return True

    except Exception as e:
        print(f'✗ Failed to generate safari-pinned-tab.svg: {e}')
        return False


def main():
    print('🎨 Starting PWA icon generation...\n')

    # Check if base icon exists
    if not BASE_ICON.exists():
        print(f'❌ Base icon not found: {BASE_ICON}')
        print('Please create a base SVG icon first.')
        return

    print(f'Using base icon: {BASE_ICON}\n')

    success_count = 0
    total_count = len(ICON_SIZES)

    # Generate all PNG icons
    for width, height, filename in ICON_SIZES:
        output_path = ICONS_DIR / filename
        if generate_png_from_svg(BASE_ICON, output_path, width, height):
            success_count += 1

    # Generate favicon.ico
    if create_favicon_ico():
        success_count += 1
        total_count += 1

    # Generate Safari pinned tab
    if create_safari_pinned_tab():
        success_count += 1
        total_count += 1

    print(f'\n✅ Icon generation complete: {success_count}/{total_count} successful')

    if success_count < total_count:
        print(f'⚠️  {total_count - success_count} icons failed to generate')
    else:
        print('🎉 All icons generated successfully!')


if __name__ == '__main__':
    main()
