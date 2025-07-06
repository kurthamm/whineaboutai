#!/usr/bin/env python3
"""
Create a better share image with more visual appeal
"""

from PIL import Image, ImageDraw, ImageFont
import math

def create_better_share_image():
    # Social media optimal dimensions
    width, height = 1200, 630
    
    # Create base image
    img = Image.new('RGB', (width, height), '#002855')
    draw = ImageDraw.Draw(img)
    
    # Create animated-style gradient background
    for y in range(height):
        for x in range(width):
            # Create a radial gradient effect
            center_x, center_y = width/2, height/2
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            max_distance = math.sqrt(center_x**2 + center_y**2)
            ratio = distance / max_distance
            
            # Blend from center blue to edge purple
            r = int(0 + (102 * ratio))
            g = int(40 + (86 * ratio))  
            b = int(85 + (149 * ratio))
            
            img.putpixel((x, y), (r, g, b))
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        tagline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 35)
        stats_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        cta_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except:
        title_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()
        stats_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()
    
    # Add tech-style decorative elements
    # Circuit-like lines
    line_color = (255, 255, 255, 60)
    
    # Horizontal lines
    for i in range(5):
        y_pos = 50 + i * 130
        draw.line([(50, y_pos), (300, y_pos)], fill=line_color, width=2)
        draw.line([(900, y_pos), (1150, y_pos)], fill=line_color, width=2)
    
    # Vertical connectors  
    for i in range(3):
        x_pos = 100 + i * 100
        draw.line([(x_pos, 100), (x_pos, 200)], fill=line_color, width=2)
        x_pos = 950 + i * 100
        draw.line([(x_pos, 300), (x_pos, 400)], fill=line_color, width=2)
    
    # Add geometric shapes for visual interest
    shapes = [
        # (x, y, size, shape_type)
        (150, 150, 40, 'circle'),
        (1000, 180, 35, 'square'),
        (100, 400, 30, 'triangle'),
        (1050, 450, 45, 'circle'),
        (200, 500, 25, 'square'),
        (950, 100, 38, 'triangle'),
    ]
    
    for x, y, size, shape_type in shapes:
        if shape_type == 'circle':
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        outline=(255, 255, 255, 100), width=3)
        elif shape_type == 'square':
            draw.rectangle([x-size//2, y-size//2, x+size//2, y+size//2], 
                          outline=(255, 255, 255, 100), width=3)
        elif shape_type == 'triangle':
            points = [
                (x, y - size//2),  # top
                (x - size//2, y + size//2),  # bottom left
                (x + size//2, y + size//2)   # bottom right
            ]
            draw.polygon(points, outline=(255, 255, 255, 100), width=3)
    
    # Main content
    center_x = width // 2
    center_y = height // 2
    
    # Title with shadow
    title_text = "WhineAboutAI"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = center_x - title_width // 2
    title_y = center_y - 100
    
    # Triple shadow for depth
    for offset in [5, 3, 1]:
        alpha = 40 * offset
        draw.text((title_x + offset, title_y + offset), title_text, 
                 font=title_font, fill=(0, 0, 0, alpha))
    draw.text((title_x, title_y), title_text, font=title_font, fill='white')
    
    # Tagline
    tagline_text = "Let it out. The bots are listening."
    tagline_bbox = draw.textbbox((0, 0), tagline_text, font=tagline_font)
    tagline_width = tagline_bbox[2] - tagline_bbox[0]
    tagline_x = center_x - tagline_width // 2
    tagline_y = title_y + 85
    draw.text((tagline_x, tagline_y), tagline_text, font=tagline_font, fill=(255, 255, 255, 220))
    
    # Stats with emoji-style replacements
    stats_text = "Join thousands venting about AI fails!"
    stats_bbox = draw.textbbox((0, 0), stats_text, font=stats_font)
    stats_width = stats_bbox[2] - stats_bbox[0]
    stats_x = center_x - stats_width // 2
    stats_y = tagline_y + 50
    draw.text((stats_x, stats_y), stats_text, font=stats_font, fill=(255, 255, 255, 200))
    
    # Call to action with stylized background
    cta_text = "whineaboutai.com"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_height = cta_bbox[3] - cta_bbox[1]
    
    # Fancy CTA background
    cta_bg_x = center_x - (cta_width + 50) // 2
    cta_bg_y = stats_y + 70
    cta_bg_width = cta_width + 50
    cta_bg_height = cta_height + 25
    
    # Gradient background for CTA
    cta_bg = Image.new('RGBA', (cta_bg_width, cta_bg_height), (255, 255, 255, 0))
    cta_bg_draw = ImageDraw.Draw(cta_bg)
    
    # Create gradient for CTA background
    for i in range(cta_bg_height):
        alpha = int(80 * (1 - i / cta_bg_height))
        cta_bg_draw.rectangle([0, i, cta_bg_width, i+1], 
                             fill=(255, 255, 255, alpha))
    
    # Paste CTA background
    img.paste(cta_bg, (cta_bg_x, cta_bg_y), cta_bg)
    
    # CTA border
    draw.rounded_rectangle(
        [cta_bg_x, cta_bg_y, cta_bg_x + cta_bg_width, cta_bg_y + cta_bg_height],
        radius=15,
        outline='white',
        width=2
    )
    
    # CTA text
    cta_x = center_x - cta_width // 2
    cta_y = cta_bg_y + 12
    draw.text((cta_x, cta_y), cta_text, font=cta_font, fill='white')
    
    # Save
    output_path = "whine-about-ai-share.jpg"
    img.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"✅ Enhanced share image created: {output_path}")
    print(f"📐 Dimensions: {width}x{height}px")
    print(f"💾 File size: {round(os.path.getsize(output_path) / 1024, 1)}KB")
    return output_path

if __name__ == "__main__":
    import os
    create_better_share_image()