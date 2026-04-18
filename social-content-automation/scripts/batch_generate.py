"""
Batch Generate
Orchestrates the full social content pipeline for a project
Runs: carousel generation → format conversion → copy generation → video generation
"""

import sys
import argparse
import os
from pathlib import Path

from utils import (
    load_yaml, load_json, create_directory, ensure_output_dirs,
    validate_config, log_progress, log_error
)
from carousel_generator import generate_carousel_for_project
from format_converter import convert_all_carousel_formats
from copy_generator import generate_copy_for_project
from llm_copy_generator import generate_llm_copy_for_project


def run_full_pipeline(project_config_path: str, platforms: list = None, use_llm: bool = False):
    """Run full social content generation pipeline"""

    log_progress("=" * 60)
    log_progress("SOCIAL CONTENT AUTOMATION PIPELINE", "🚀")
    log_progress("=" * 60)

    try:
        # Load configs
        log_progress("Loading configurations...")
        project_config = load_json(project_config_path)
        branding_config = load_yaml("config/branding.yaml")
        platform_specs = load_yaml("config/platforms.yaml")
        copy_templates = load_yaml("config/copy_templates.yaml")

        # Validate project config
        if not validate_config(project_config):
            log_error("Invalid project configuration", Exception("See errors above"))
            return False

        project_name = project_config['project_name']
        log_progress(f"Project: {project_name}")

        # Determine which platforms to generate for
        if platforms is None:
            platforms = [p for p in ['linkedin', 'instagram', 'tiktok', 'twitter', 'web']
                        if platform_specs['platforms'].get(p, {}).get('enabled', False)]

        # Create output directories
        log_progress(f"Creating output directories for {len(platforms)} platforms...")
        ensure_output_dirs(project_name, platforms)

        # Phase 1: Carousel Generation
        log_progress("\n" + "=" * 60)
        log_progress("PHASE 1: CAROUSEL GENERATION", "📊")
        log_progress("=" * 60)
        for platform in platforms:
            if platform != 'twitter':  # Twitter doesn't use carousel images
                generate_carousel_for_project(project_config, branding_config,
                                            platform_specs, platform)

        # Phase 2: Format Conversion
        log_progress("\n" + "=" * 60)
        log_progress("PHASE 2: FORMAT CONVERSION", "🎨")
        log_progress("=" * 60)
        convert_all_carousel_formats(project_config, platform_specs)

        # Phase 3: Copy Generation
        log_progress("\n" + "=" * 60)
        log_progress("PHASE 3: COPY GENERATION", "✍️")
        log_progress("=" * 60)

        if use_llm:
            log_progress("Using Claude API for creative copy generation...")
            generate_llm_copy_for_project(project_config, platforms)
        else:
            log_progress("Using template-based copy generation...")
            generate_copy_for_project(project_config, copy_templates, branding_config)

        # Phase 4: Video Generation (optional - requires moviepy)
        log_progress("\n" + "=" * 60)
        log_progress("PHASE 4: VIDEO GENERATION", "🎥")
        log_progress("=" * 60)
        log_progress("Video generation (TikTok/Reels) requires moviepy.")
        log_progress("This feature is documented but not auto-generated.")
        log_progress("Videos can be created using your video editor or automated script.")

        # Summary
        log_progress("\n" + "=" * 60)
        log_progress("PIPELINE COMPLETE", "✓")
        log_progress("=" * 60)
        log_progress(f"Output folder: outputs/{project_name}/")
        log_progress(f"Platforms generated: {', '.join(platforms)}")
        log_progress("\nNext steps:")
        log_progress("1. Review generated copy in each platform folder")
        log_progress("2. Edit copy as needed (only text, visuals are automated)")
        log_progress("3. Upload carousel images to LinkedIn/Instagram")
        log_progress("4. Copy/paste Twitter thread to Twitter")
        log_progress("5. Upload videos to TikTok/Reels when ready")

        return True

    except Exception as e:
        log_error("Pipeline execution", e)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate social media content for a project"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to project config JSON file"
    )
    parser.add_argument(
        "--platforms",
        nargs="+",
        default=None,
        help="Specific platforms to generate for (e.g., linkedin instagram twitter)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use Claude API for LLM-generated copy variants (requires ANTHROPIC_API_KEY)"
    )

    args = parser.parse_args()

    # Run pipeline
    success = run_full_pipeline(args.config, args.platforms, args.use_llm)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
