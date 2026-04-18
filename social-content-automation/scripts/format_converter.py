"""
Format Converter
Converts carousel images to platform-specific formats
"""

import os
from pathlib import Path
from PIL import Image
from typing import Dict
from utils import load_yaml, load_json, create_directory, get_output_dir, log_progress, log_error


class FormatConverter:
    """Convert carousel images to platform-specific formats"""

    def __init__(self, platform_specs: Dict):
        self.platforms = platform_specs.get('platforms', {})

    def get_platform_dimensions(self, platform: str) -> tuple:
        """Get width and height for a platform"""
        spec = self.platforms.get(platform, {})
        return spec.get('width_px', 1080), spec.get('height_px', 1080)

    def get_platform_format(self, platform: str) -> str:
        """Get image format for a platform (png or jpg)"""
        spec = self.platforms.get(platform, {})
        return spec.get('image_format', 'png')

    def resize_and_crop_to_square(self, image: Image.Image, target_size: int) -> Image.Image:
        """Resize and crop image to square"""
        # Calculate the scaling factor
        scale = max(target_size / image.width, target_size / image.height)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        # Resize
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Crop to square from center
        left = (new_width - target_size) // 2
        top = (new_height - target_size) // 2
        right = left + target_size
        bottom = top + target_size

        return resized.crop((left, top, right, bottom))

    def convert_carousel_images(self, source_dir: str, carousel_name: str,
                              from_platform: str, to_platform: str):
        """Convert carousel images from one platform format to another"""

        source_platform_dir = source_dir  # Assumes images already in source
        target_width, target_height = self.get_platform_dimensions(to_platform)
        target_format = self.get_platform_format(to_platform)

        log_progress(f"Converting {carousel_name} from {from_platform} to {to_platform}")

        # Get all slide images
        slide_files = sorted([f for f in os.listdir(source_platform_dir)
                            if carousel_name in f and f.endswith(('.png', '.jpg', '.jpeg'))])

        for slide_file in slide_files:
            source_path = os.path.join(source_platform_dir, slide_file)
            target_filename = slide_file.rsplit('.', 1)[0] + f".{target_format}"
            target_path = os.path.join(source_platform_dir.replace(from_platform, to_platform),
                                      target_filename)

            try:
                img = Image.open(source_path)

                # For square formats, crop to square
                if target_width == target_height:
                    img_converted = self.resize_and_crop_to_square(img, target_width)
                else:
                    # For other aspect ratios, resize maintaining aspect
                    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                    img_converted = img

                # Create output directory
                create_directory(os.path.dirname(target_path))

                # Save in target format
                if target_format.lower() == 'jpg':
                    img_converted = img_converted.convert('RGB')

                img_converted.save(target_path, format=target_format.upper())
                log_progress(f"Converted: {target_filename}")

            except Exception as e:
                log_error(f"Converting {slide_file}", e)


def convert_all_carousel_formats(project_config: Dict, platform_specs: Dict):
    """Convert carousels from base format to all platform formats"""

    log_progress(f"Converting formats for {project_config['project_name']}")

    converter = FormatConverter(platform_specs)
    project_name = project_config['project_name']

    # Assume images start in 'linkedin' format (1080x1350 is standard)
    source_platform = 'linkedin'
    target_platforms = ['instagram', 'tiktok', 'blog']

    # Get all carousels
    for carousel in project_config.get('carousels', []):
        carousel_name = carousel.get('title', '').lower().replace(' ', '_')

        for target_platform in target_platforms:
            source_dir = get_output_dir(project_name, source_platform)
            if os.path.exists(source_dir):
                converter.convert_carousel_images(source_dir, carousel_name,
                                                source_platform, target_platform)

    log_progress("Format conversion complete")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python format_converter.py <project_config.json>")
        sys.exit(1)

    project_config_path = sys.argv[1]

    try:
        project_config = load_json(project_config_path)
        platform_specs = load_yaml("config/platforms.yaml")

        convert_all_carousel_formats(project_config, platform_specs)

    except Exception as e:
        log_error("Format conversion", e)
        sys.exit(1)
