"""
Carousel Generator
Generates carousel slides from project config and source materials
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
from typing import Dict, List, Tuple
from utils import (
    load_yaml, load_json, create_directory, get_output_dir,
    log_progress, log_error, get_hex_color
)


class CarouselSlideGenerator:
    """Generate individual carousel slides as images"""

    def __init__(self, branding_config: Dict, platform_specs: Dict):
        self.branding = branding_config.get('branding', {})
        self.platforms = platform_specs.get('platforms', {})
        self.primary_color = get_hex_color('primary', branding_config)
        self.secondary_color = get_hex_color('secondary', branding_config)
        self.text_color = get_hex_color('text', branding_config)
        self.bg_color = get_hex_color('background', branding_config)

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_title_slide(self, width: int, height: int, title: str,
                          subtitle: str = "") -> Image.Image:
        """Create title slide for carousel"""
        img = Image.new('RGB', (width, height), self.hex_to_rgb(self.bg_color))
        draw = ImageDraw.Draw(img)

        # Simple font fallback (use default if custom fonts not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", int(width * 0.06))
            subtitle_font = ImageFont.truetype("arial.ttf", int(width * 0.04))
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        # Draw colored background accent
        accent_height = int(height * 0.15)
        draw.rectangle(
            [(0, 0), (width, accent_height)],
            fill=self.hex_to_rgb(self.primary_color)
        )

        # Draw title
        title_y = int(height * 0.35)
        draw.text(
            (int(width * 0.1), title_y),
            title,
            font=title_font,
            fill=self.hex_to_rgb(self.text_color)
        )

        # Draw subtitle if provided
        if subtitle:
            subtitle_y = int(height * 0.55)
            draw.text(
                (int(width * 0.1), subtitle_y),
                subtitle,
                font=subtitle_font,
                fill=self.hex_to_rgb(self.primary_color)
            )

        return img

    def create_data_slide(self, width: int, height: int, headline: str,
                         metric: str, metric_value: str,
                         description: str = "") -> Image.Image:
        """Create data-focused slide"""
        img = Image.new('RGB', (width, height), self.hex_to_rgb("#FFFFFF"))
        draw = ImageDraw.Draw(img)

        try:
            headline_font = ImageFont.truetype("arial.ttf", int(width * 0.05))
            metric_font = ImageFont.truetype("arial.ttf", int(width * 0.12))
            body_font = ImageFont.truetype("arial.ttf", int(width * 0.035))
        except:
            headline_font = ImageFont.load_default()
            metric_font = ImageFont.load_default()
            body_font = ImageFont.load_default()

        # Draw colored bar at top
        bar_height = 8
        draw.rectangle(
            [(0, 0), (width, bar_height)],
            fill=self.hex_to_rgb(self.secondary_color)
        )

        # Draw headline
        headline_y = int(height * 0.15)
        draw.text(
            (int(width * 0.1), headline_y),
            headline,
            font=headline_font,
            fill=self.hex_to_rgb(self.text_color)
        )

        # Draw metric (large number)
        metric_y = int(height * 0.40)
        draw.text(
            (int(width * 0.1), metric_y),
            metric_value,
            font=metric_font,
            fill=self.hex_to_rgb(self.primary_color)
        )

        # Draw metric label
        label_y = int(height * 0.52)
        draw.text(
            (int(width * 0.1), label_y),
            metric,
            font=body_font,
            fill=self.hex_to_rgb(self.text_color)
        )

        # Draw description if provided
        if description:
            desc_y = int(height * 0.70)
            draw.text(
                (int(width * 0.1), desc_y),
                description,
                font=body_font,
                fill=self.hex_to_rgb(self.text_color)
            )

        return img

    def create_cta_slide(self, width: int, height: int, message: str,
                        cta_text: str) -> Image.Image:
        """Create call-to-action slide"""
        img = Image.new('RGB', (width, height),
                       self.hex_to_rgb(self.primary_color))
        draw = ImageDraw.Draw(img)

        try:
            message_font = ImageFont.truetype("arial.ttf", int(width * 0.05))
            cta_font = ImageFont.truetype("arial.ttf", int(width * 0.07))
        except:
            message_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()

        # Draw message
        msg_y = int(height * 0.35)
        draw.text(
            (int(width * 0.1), msg_y),
            message,
            font=message_font,
            fill=self.hex_to_rgb("#FFFFFF")
        )

        # Draw CTA button background
        button_y = int(height * 0.65)
        button_height = int(height * 0.15)
        draw.rectangle(
            [(int(width * 0.15), button_y),
             (int(width * 0.85), button_y + button_height)],
            fill=self.hex_to_rgb(self.secondary_color)
        )

        # Draw CTA text
        draw.text(
            (int(width * 0.2), button_y + int(button_height * 0.25)),
            cta_text,
            font=cta_font,
            fill=self.hex_to_rgb("#FFFFFF")
        )

        return img

    def save_slide(self, image: Image.Image, output_path: str, format: str = "png"):
        """Save slide image"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if format.lower() == "jpg":
            image = image.convert('RGB')
            format = "JPEG"
        image.save(output_path, format=format.upper())
        log_progress(f"Saved slide: {output_path}")


def generate_carousel_for_project(project_config: Dict, branding_config: Dict,
                                 platform_specs: Dict, platform: str):
    """Generate all carousel slides for a project on a specific platform"""

    log_progress(f"Generating {platform} carousels for {project_config['project_name']}")

    generator = CarouselSlideGenerator(branding_config, platform_specs)
    platform_spec = platform_specs['platforms'].get(platform, {})
    output_base = get_output_dir(project_config['project_name'], platform)

    # Determine slide dimensions
    width = platform_spec.get('width_px', 1080)
    height = platform_spec.get('height_px', 1350)
    image_format = platform_spec.get('image_format', 'png')

    # Generate slides for each carousel
    carousel_count = 0
    for carousel_idx, carousel in enumerate(project_config.get('carousels', []), 1):
        carousel_name = carousel.get('title', f'Carousel {carousel_idx}').lower().replace(' ', '_')

        # Slide 1: Title slide
        title_slide = generator.create_title_slide(
            width, height,
            carousel.get('title', ''),
            carousel.get('subtitle', '')
        )
        title_path = f"{output_base}/{carousel_name}_slide_1.{image_format}"
        generator.save_slide(title_slide, title_path, image_format)

        # Slides 2+: Data slides (using carousel insights/metrics)
        insights = carousel.get('insights', [])
        for slide_num, insight in enumerate(insights[:5], start=2):  # Max 5 data slides
            data_slide = generator.create_data_slide(
                width, height,
                insight.get('headline', ''),
                insight.get('metric_label', ''),
                insight.get('metric_value', ''),
                insight.get('description', '')
            )
            data_path = f"{output_base}/{carousel_name}_slide_{slide_num}.{image_format}"
            generator.save_slide(data_slide, data_path, image_format)

        # Final slide: CTA
        cta_slide = generator.create_cta_slide(
            width, height,
            carousel.get('cta_message', 'Read the full case study'),
            carousel.get('cta_button_text', 'Learn More')
        )
        final_slide_num = len(insights) + 2
        cta_path = f"{output_base}/{carousel_name}_slide_{final_slide_num}.{image_format}"
        generator.save_slide(cta_slide, cta_path, image_format)

        carousel_count += 1

    log_progress(f"Generated {carousel_count} carousels for {platform}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python carousel_generator.py <project_config.json> <platform>")
        sys.exit(1)

    project_config_path = sys.argv[1]
    platform = sys.argv[2]

    try:
        project_config = load_json(project_config_path)
        branding_config = load_yaml("config/branding.yaml")
        platform_specs = load_yaml("config/platforms.yaml")

        generate_carousel_for_project(project_config, branding_config, platform_specs, platform)

    except Exception as e:
        log_error("Carousel generation", e)
        sys.exit(1)
