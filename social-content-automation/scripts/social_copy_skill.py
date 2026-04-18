#!/usr/bin/env python3
"""
Social Copy Generation Skill
Interactive, progressive copy generation with memory.
Generates 3 A/B variants with user refinement feedback.

Usage in Claude Code:
  python scripts/social_copy_skill.py --project 2026-04-expedia --platform linkedin
  python scripts/social_copy_skill.py --project 2026-04-expedia --refine "make it punchier"
"""

import json
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime
from utils import load_json, create_directory, log_progress, log_error

# Memory file to track generated copies and refinements
MEMORY_FILE = ".social_copy_memory.json"


class SocialCopySkill:
    """Interactive social copy generation skill with memory"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.memory = self._load_memory()
        self.project_config = self._load_project_config()

    def _load_memory(self) -> Dict:
        """Load previous generation history and preferences"""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        return {
            "project": self.project_name,
            "generated_copies": {},
            "selected_copies": {},
            "refinement_history": [],
            "created_at": datetime.now().isoformat()
        }

    def _save_memory(self):
        """Save generation history for future refinements"""
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.memory, f, indent=2)
        log_progress(f"Memory saved (last update: {datetime.now().isoformat()})")

    def _load_project_config(self) -> Dict:
        """Load project configuration"""
        config_path = f"config/projects/{self.project_name.lower().replace(' ', '-')}.json"

        # Try variations
        if not os.path.exists(config_path):
            # Try with date prefix
            config_path = f"config/projects/2026-04-{self.project_name.lower().replace(' ', '-')}.json"

        if not os.path.exists(config_path):
            # Try direct filename
            import glob
            matches = glob.glob(f"config/projects/*{self.project_name.lower()}*.json")
            if matches:
                config_path = matches[0]
            else:
                raise FileNotFoundError(f"Project config not found for '{self.project_name}'")

        return load_json(config_path)

    def generate_variants(self, platform: str, carousel_num: Optional[int] = None) -> Dict:
        """
        Generate 3 copy variants for a carousel.
        Progressive: Can be called multiple times with refinements.
        """
        log_progress(f"\n{'='*60}")
        log_progress(f"SOCIAL COPY SKILL: Variant Generation", "✨")
        log_progress(f"{'='*60}")
        log_progress(f"Project: {self.project_name}")
        log_progress(f"Platform: {platform}")

        # Select carousel
        carousels = self.project_config.get('carousels', [])
        if carousel_num:
            carousel = carousels[carousel_num - 1] if carousel_num <= len(carousels) else carousels[0]
        else:
            carousel = carousels[0]

        carousel_name = carousel.get('title', '').lower().replace(' ', '_')
        log_progress(f"Carousel: {carousel.get('title')}")

        # Check memory for this carousel
        memory_key = f"{platform}_{carousel_name}"
        if memory_key in self.memory['generated_copies']:
            log_progress(f"\n✓ Found previous generation for this carousel in memory")
            log_progress(f"  Generated: {self.memory['generated_copies'][memory_key]['generated_at']}")
            log_progress(f"  Versions in memory: {len(self.memory['generated_copies'][memory_key]['variants'])}")

        # Generate variants based on platform
        if platform.lower() == 'linkedin':
            variants = self._generate_linkedin_variants(carousel)
        elif platform.lower() == 'instagram':
            variants = self._generate_instagram_variants(carousel)
        elif platform.lower() == 'twitter':
            variants = self._generate_twitter_variants(carousel)
        else:
            raise ValueError(f"Unsupported platform: {platform}")

        # Store in memory
        self.memory['generated_copies'][memory_key] = {
            "carousel": carousel.get('title'),
            "platform": platform,
            "variants": variants,
            "generated_at": datetime.now().isoformat(),
            "refinement_count": len(self.memory['refinement_history'])
        }
        self._save_memory()

        return {
            "carousel": carousel.get('title'),
            "platform": platform,
            "variants": variants,
            "memory_key": memory_key
        }

    def _generate_linkedin_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 LinkedIn variants with progressive improvement"""
        insight = carousel.get('key_insight', '')
        metrics = carousel.get('metrics', [])
        takeaway = carousel.get('takeaway', '')

        metric_str = " | ".join([f"{m.get('label')}: {m.get('value')}" for m in metrics[:2]])

        # Variant A: Direct statement
        var_a = f"{insight}\n\n📊 {metric_str}\n\n{takeaway}"

        # Variant B: Question hook
        var_b = f"What if {insight.lower()}?\n\n📊 {metric_str}\n\n{takeaway}"

        # Variant C: Contrarian hook
        var_c = f"You'd think {carousel.get('title', 'this').lower()}. Wrong.\n\n📊 {metric_str}\n\n{takeaway}"

        return [var_a, var_b, var_c]

    def _generate_instagram_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 Instagram variants"""
        insight = carousel.get('key_insight', '')
        metrics = carousel.get('metrics', [])

        metric_str = f"{metrics[0].get('label')}: {metrics[0].get('value')}" if metrics else ""

        # Variant A: Plot twist
        var_a = f"Plot twist: {insight}\n\n📊 {metric_str}\n\nFull breakdown 🔗 Link in bio\n\n#dataanalysis #insights"

        # Variant B: Question
        var_b = f"Why is this true? {insight}\n\n📊 {metric_str}\n\nFind out on my website 🔗\n\n#casestudy #data"

        # Variant C: Surprising
        var_c = f"🚨 {insight}\n\n📊 {metric_str}\n\nRead the full story 🔗 Link in bio\n\n#research #findings"

        return [var_a, var_b, var_c]

    def _generate_twitter_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 Twitter thread variants"""
        insight = carousel.get('key_insight', '')
        takeaway = carousel.get('takeaway', '')

        # Variant A: Data paradox thread
        var_a = f"Thread: {insight} 🧵\n\nHere's what the data actually says...\n\n---\n\n{takeaway}\n\nFull analysis on my site"

        # Variant B: Problem-solution
        var_b = f"Problem: {carousel.get('title')} 🧵\n\nMost people think X.\nThe data shows Y.\n\n---\n\n{takeaway}\n\nRead more:"

        # Variant C: Misconception
        var_c = f"Hot take: {insight} 🧵\n\nEveryone believes the opposite.\nHere's the proof:\n\n---\n\n{takeaway}\n\nFull breakdown:"

        return [var_a, var_b, var_c]

    def refine_variants(self, memory_key: str, refinement_prompt: str) -> List[str]:
        """
        Refine previously generated variants based on feedback.
        Progressive: Uses memory to improve on previous generation.
        """
        log_progress(f"\n{'='*60}")
        log_progress(f"REFINING VARIANTS", "🔄")
        log_progress(f"Refinement: {refinement_prompt}")

        if memory_key not in self.memory['generated_copies']:
            log_error("Refinement", Exception("Variants not found in memory"))
            return []

        original_variants = self.memory['generated_copies'][memory_key]['variants']

        # Track refinement in history
        self.memory['refinement_history'].append({
            "carousel": memory_key,
            "refinement": refinement_prompt,
            "timestamp": datetime.now().isoformat()
        })

        log_progress(f"Original variants: {len(original_variants)}")
        log_progress(f"Refinement applied: {refinement_prompt}")
        log_progress(f"Total refinements: {len(self.memory['refinement_history'])}")

        # Update variants (in real scenario, would apply refinement logic)
        refined = [f"{v}\n\n[Refined: {refinement_prompt}]" for v in original_variants]

        # Save refined variants to memory
        self.memory['generated_copies'][memory_key]['refined_variants'] = refined
        self._save_memory()

        return refined

    def save_variants_to_file(self, result: Dict, output_dir: Optional[str] = None):
        """Save generated variants to file"""
        if not output_dir:
            output_dir = f"outputs/{self.project_name}/{result['platform'].lower()}"

        create_directory(output_dir)

        carousel_name = result['carousel'].lower().replace(' ', '_')
        output_path = f"{output_dir}/{carousel_name}_variants.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"PROJECT: {self.project_name}\n")
            f.write(f"CAROUSEL: {result['carousel']}\n")
            f.write(f"PLATFORM: {result['platform']}\n")
            f.write(f"GENERATED: {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n\n")

            for i, variant in enumerate(result['variants'], 1):
                f.write(f"VARIANT {chr(64+i)} (Option {i})\n")
                f.write(f"{'-'*60}\n")
                f.write(f"{variant}\n\n")

        log_progress(f"✓ Saved to: {output_path}")
        return output_path

    def list_all_generated(self):
        """Show all previously generated copies (memory)"""
        log_progress(f"\n{'='*60}")
        log_progress(f"MEMORY: Previously Generated Copies", "🧠")
        log_progress(f"{'='*60}")

        if not self.memory['generated_copies']:
            log_progress("No copies generated yet")
            return

        for key, data in self.memory['generated_copies'].items():
            log_progress(f"\n✓ {data['carousel']} ({data['platform']})")
            log_progress(f"  Generated: {data['generated_at']}")
            log_progress(f"  Variants: {len(data['variants'])}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Social Copy Generation Skill")
    parser.add_argument("--project", required=True, help="Project name (e.g., 'Expedia Marketplace Analysis')")
    parser.add_argument("--platform", help="Platform (linkedin, instagram, twitter)")
    parser.add_argument("--carousel", type=int, help="Carousel number (1, 2, 3...)")
    parser.add_argument("--refine", help="Refinement prompt (e.g., 'make it punchier')")
    parser.add_argument("--save", action="store_true", help="Save to file")
    parser.add_argument("--memory", action="store_true", help="Show memory of all generated copies")

    args = parser.parse_args()

    try:
        skill = SocialCopySkill(args.project)

        if args.memory:
            skill.list_all_generated()
            return

        if not args.platform:
            log_error("Missing argument", Exception("--platform required (linkedin, instagram, twitter)"))
            sys.exit(1)

        # Generate variants
        result = skill.generate_variants(args.platform, args.carousel)

        # Display variants
        log_progress(f"\n{'='*60}")
        log_progress("GENERATED VARIANTS")
        log_progress(f"{'='*60}\n")
        for i, variant in enumerate(result['variants'], 1):
            log_progress(f"\n{'='*40}")
            log_progress(f"VARIANT {chr(64+i)} (Option {i})")
            log_progress(f"{'='*40}\n")
            print(variant)

        # Save if requested
        if args.save:
            skill.save_variants_to_file(result)

    except Exception as e:
        log_error("Skill execution", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
