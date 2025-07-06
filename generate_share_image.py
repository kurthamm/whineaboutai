#!/usr/bin/env python3
"""
Generate Social Media Share Image for WhineAboutAI
Creates a 1200x630px image optimized for Facebook/Twitter sharing
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_share_image():
    # Image dimensions for social media (Facebook/Twitter optimal)
    width, height = 1200, 630
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color='#002855')
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for y in range(height):
        # Interpolate between blue and purple
        ratio = y / height
        r = int(0 + (102 * ratio))
        g = int(40 + (126 * ratio))
        b = int(85 + (234 * ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to load fonts, fall back to default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 40)
        stats_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        cta_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        # Fall back to default font
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()
    
    # Add floating emojis
    emoji_font_size = 60
    try:
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", emoji_font_size)
    except:
        emoji_font = ImageFont.load_default()
    
    # Skip emojis for now due to font encoding issues
    # Add decorative elements instead
    
    # Add some decorative circles
    decorative_elements = [
        (80, 80, 25),
        (1000, 100, 30),
        (60, 450, 20),
        (1050, 480, 35),
        (200, 200, 28),
        (900, 300, 22)
    ]
    
    for x, y, radius in decorative_elements:
        # Semi-transparent circles
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    fill=(255, 255, 255, 40), outline=(255, 255, 255, 80), width=2)
    
    # Main content positioning
    center_x = width // 2
    center_y = height // 2
    
    # Main title
    title_text = "WhineAboutAI"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = center_x - title_width // 2
    title_y = center_y - 120
    
    # Add text shadow for title
    shadow_offset = 3
    draw.text((title_x + shadow_offset, title_y + shadow_offset), title_text, 
              font=title_font, fill=(0, 0, 0, 128))
    draw.text((title_x, title_y), title_text, font=title_font, fill='white')
    
    # Tagline
    tagline_text = "Let it out. The bots are listening."
    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = center_x - tagline_width // 2
    tagline_y = title_y + 100
    draw.text((tagline_x, tagline_y), tagline_text, font=tagline_font, fill=(255, 255, 255, 230))
    
    # Stats text
    stats_text = "Join thousands venting about AI gone wrong!"
    stats_bbox = draw.textbbox((0, 0), stats_text, font=stats_font)
    stats_width = stats_bbox[2] - stats_bbox[0]
    stats_x = center_x - stats_width // 2
    stats_y = tagline_y + 60
    draw.text((stats_x, stats_y), stats_text, font=stats_font, fill=(255, 255, 255, 200))
    
    # Call to action with background
    cta_text = "Share Your AI Nightmare"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_height = cta_bbox[3] - cta_bbox[1]
    
    # CTA background rectangle
    cta_bg_x = center_x - (cta_width + 60) // 2
    cta_bg_y = stats_y + 80
    cta_bg_width = cta_width + 60
    cta_bg_height = cta_height + 30
    
    # Draw rounded rectangle background
    draw.rounded_rectangle(
        [cta_bg_x, cta_bg_y, cta_bg_x + cta_bg_width, cta_bg_y + cta_bg_height],
        radius=25,
        fill=(255, 255, 255, 51),  # Semi-transparent white
        outline='white',
        width=3
    )
    
    # CTA text
    cta_x = center_x - cta_width // 2
    cta_y = cta_bg_y + 15
    draw.text((cta_x, cta_y), cta_text, font=cta_font, fill='white')
    
    # Save the image
    output_path = "whine-about-ai-share.jpg"
    img.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"✅ Share image created: {output_path}")
    print(f"📐 Dimensions: {width}x{height}px (optimized for social media)")
    return output_path

if __name__ == "__main__":
    create_share_image()