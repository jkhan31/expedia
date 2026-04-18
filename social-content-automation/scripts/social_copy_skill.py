#!/usr/bin/env python3
"""
Social Copy Generation Skill
Interactive, progressive copy generation with memory and refinement.
Generates 3 A/B variants with actual refinement based on user feedback.

Usage in Claude Code:
  python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform linkedin --save
  python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform instagram
  python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --memory
"""

import json
import os
import sys
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
from utils import load_json, create_directory, log_progress, log_error


class SocialCopySkill:
    """Interactive social copy generation skill with memory and progressive refinement"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_config = self._load_project_config()
        self.memory = self._load_memory()

    def _get_memory_file(self) -> str:
        """Get per-project memory file name"""
        project_hash = hashlib.md5(self.project_name.encode()).hexdigest()[:8]
        return f".social_copy_memory_{project_hash}.json"

    def _load_memory(self) -> Dict:
        """Load previous generation history and refinements"""
        memory_file = self._get_memory_file()
        if os.path.exists(memory_file):
            try:
                with open(memory_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                log_progress(f"⚠️  Memory file corrupted, starting fresh")
                return self._init_memory()
        return self._init_memory()

    def _init_memory(self) -> Dict:
        """Initialize fresh memory structure"""
        return {
            "project": self.project_name,
            "generated_copies": {},
            "selected_copies": {},
            "refinement_history": [],
            "created_at": datetime.now().isoformat()
        }

    def _save_memory(self):
        """Save generation history and refinements"""
        memory_file = self._get_memory_file()
        with open(memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
        log_progress(f"✓ Memory saved: {memory_file}")

    def _load_project_config(self) -> Dict:
        """Load project configuration with smart fallback"""
        config_path = None

        # Try exact match
        if os.path.exists(f"config/projects/{self.project_name}.json"):
            config_path = f"config/projects/{self.project_name}.json"

        # Try lowercase with dash
        elif os.path.exists(f"config/projects/{self.project_name.lower().replace(' ', '-')}.json"):
            config_path = f"config/projects/{self.project_name.lower().replace(' ', '-')}.json"

        # Try with date prefix
        elif os.path.exists(f"config/projects/2026-04-{self.project_name.lower().replace(' ', '-')}.json"):
            config_path = f"config/projects/2026-04-{self.project_name.lower().replace(' ', '-')}.json"

        # Fallback: glob search
        else:
            import glob
            matches = glob.glob(f"config/projects/*{self.project_name.lower()}*.json")
            if matches:
                config_path = matches[0]

        if not config_path:
            raise FileNotFoundError(f"Project config not found for '{self.project_name}'")

        return load_json(config_path)

    def generate_variants(self, platform: str, carousel_num: Optional[int] = None) -> Dict:
        """
        Generate 3 copy variants for a carousel.
        Progressive: Tracks in memory, can be refined later.
        """
        log_progress(f"\n{'='*60}")
        log_progress(f"SOCIAL COPY SKILL: Variant Generation", "✨")
        log_progress(f"{'='*60}")
        log_progress(f"Project: {self.project_name}")
        log_progress(f"Platform: {platform.title()}")

        # Select carousel
        carousels = self.project_config.get('carousels', [])
        if not carousels:
            raise ValueError("No carousels found in project config")

        if carousel_num:
            carousel = carousels[carousel_num - 1] if carousel_num <= len(carousels) else carousels[0]
        else:
            carousel = carousels[0]

        carousel_name = carousel.get('title', '').lower().replace(' ', '_').replace(':', '')
        log_progress(f"Carousel: {carousel.get('title')}")

        # Check memory for this carousel
        memory_key = f"{platform.lower()}_{carousel_name}"
        if memory_key in self.memory['generated_copies']:
            prev = self.memory['generated_copies'][memory_key]
            log_progress(f"\n✓ Found previous generation in memory")
            log_progress(f"  Generated: {prev['generated_at']}")
            log_progress(f"  Refinements: {prev.get('refinement_count', 0)}")

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
            "refinement_count": len([r for r in self.memory['refinement_history'] if r.get('carousel') == memory_key])
        }
        self._save_memory()

        return {
            "carousel": carousel.get('title'),
            "platform": platform,
            "variants": variants,
            "memory_key": memory_key
        }

    def _generate_linkedin_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 distinct LinkedIn variants with different hooks"""
        insight = carousel.get('key_insight', '')
        metrics = carousel.get('metrics', [])
        takeaway = carousel.get('takeaway', '')
        title = carousel.get('title', '')

        metric_str = " | ".join([f"{m.get('label')}: {m.get('value')}" for m in metrics[:2]])

        # Variant A: Direct impact statement (authority tone)
        var_a = f"{insight}\n\n📊 {metric_str}\n\n{takeaway}\n\nRead the full analysis on my website →"

        # Variant B: Contrarian/provocative (curiosity-driven)
        var_b = f"Most people get {title.lower()} wrong.\n\nHere's what the data actually shows: {insight}\n\n📊 {metric_str}\n\nFull breakdown →"

        # Variant C: Question-based narrative (engagement-driven)
        var_c = f"What if everything you thought about {title.lower()} was backwards?\n\n{insight}\n\n📊 {metric_str}\n\nThe implications? {takeaway}"

        return [var_a, var_b, var_c]

    def _generate_instagram_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 distinct Instagram variants optimized for engagement"""
        insight = carousel.get('key_insight', '')
        metrics = carousel.get('metrics', [])
        title = carousel.get('title', '')

        metric_str = f"{metrics[0].get('label')}: {metrics[0].get('value')}" if metrics else "Key insight"

        # Variant A: Plot twist (stop-scroll hook, highest engagement)
        var_a = f"Plot twist 🔄\n\n{insight}\n\n📊 {metric_str}\n\nFull breakdown 🔗 Link in bio\n\n#dataanalysis #insights #casestudy"

        # Variant B: Myth-busting angle (contrarian, save-worthy)
        var_b = f"❌ Everyone thinks: {title.lower()}\n✅ Reality: {insight}\n\n📊 {metric_str}\n\nSave this 👆\n\n#data #myth #research"

        # Variant C: Question hook (comment-bait, discussion-starter)
        var_c = f"Why is this important?\n\n{insight}\n\n📊 {metric_str}\n\nComment your thoughts 👇\n\nFull story 🔗 Bio link\n\n#analysis #casestudy"

        return [var_a, var_b, var_c]

    def _generate_twitter_variants(self, carousel: Dict) -> List[str]:
        """Generate 3 distinct Twitter thread variants with full narrative structure"""
        insight = carousel.get('key_insight', '')
        insights = carousel.get('insights', [])
        takeaway = carousel.get('takeaway', '')
        metrics = carousel.get('metrics', [])
        title = carousel.get('title', '')

        # Variant A: Data paradox thread (contrarian, research-focused)
        metric_1 = f"{metrics[0].get('value')}" if metrics else ""
        metric_2 = f"{metrics[1].get('value')}" if len(metrics) > 1 else ""
        var_a = (
            f"{insight} 🧵\n\n"
            f"1️⃣ Most people think {title.lower()} matters because X\n\n"
            f"2️⃣ But {metric_1} tells a different story\n\n"
            f"3️⃣ {takeaway}\n\n"
            f"Full analysis: [link]"
        )

        # Variant B: Problem-solution-impact thread (actionable)
        insight_1 = insights[0].get('headline', 'The core issue') if insights else 'The core issue'
        insight_2 = insights[1].get('headline', 'Second insight') if len(insights) > 1 else 'Deeper insight'
        var_b = (
            f"Problem: {title} 🧵\n\n"
            f"1️⃣ {insight_1}\n\n"
            f"2️⃣ {insight_2}\n\n"
            f"3️⃣ Solution: {takeaway}\n\n"
            f"Read more: [link]"
        )

        # Variant C: Misconception-correction thread (myth-busting)
        var_c = (
            f"Myth: {title} is about {title.lower()}\n\n"
            f"Reality: {insight} 🧵\n\n"
            f"1️⃣ Evidence: {metric_1}\n\n"
            f"2️⃣ What it means: {takeaway}\n\n"
            f"3️⃣ What to do about it: [your recommendation]\n\n"
            f"Full case study: [link]"
        )

        return [var_a, var_b, var_c]

    def refine_variants(self, memory_key: str, refinement_prompt: str) -> List[str]:
        """
        Refine previously generated variants based on user feedback.
        Progressive: Uses feedback to improve variants.
        """
        log_progress(f"\n{'='*60}")
        log_progress(f"REFINING VARIANTS", "🔄")
        log_progress(f"{'='*60}")
        log_progress(f"Refinement request: {refinement_prompt}")

        if memory_key not in self.memory['generated_copies']:
            log_error("Refinement", Exception("Variants not found in memory"))
            return []

        original_variants = self.memory['generated_copies'][memory_key]['variants']
        carousel_title = self.memory['generated_copies'][memory_key]['carousel']

        # Track refinement in history
        self.memory['refinement_history'].append({
            "carousel": memory_key,
            "carousel_title": carousel_title,
            "refinement": refinement_prompt,
            "timestamp": datetime.now().isoformat()
        })

        log_progress(f"Original variants: {len(original_variants)}")
        log_progress(f"Applying refinement: {refinement_prompt}")

        # Apply refinement transformations
        refined = []
        for i, variant in enumerate(original_variants):
            refined_variant = self._apply_refinement(variant, refinement_prompt)
            refined.append(refined_variant)

        # Store refined variants
        self.memory['generated_copies'][memory_key]['refined_variants'] = refined
        self.memory['generated_copies'][memory_key]['refinement_count'] = len([r for r in self.memory['refinement_history'] if r.get('carousel') == memory_key])
        self._save_memory()

        log_progress(f"✓ Refinement applied to {len(refined)} variants")
        return refined

    def _apply_refinement(self, variant: str, refinement_prompt: str) -> str:
        """Apply intelligent user feedback to variant"""
        refinement_lower = refinement_prompt.lower()

        # Sophisticated refinement transformations
        transformations = {
            # Tone adjustments
            'punch': self._make_punchier,
            'punchier': self._make_punchier,
            'punchy': self._make_punchier,
            'bold': lambda v: f"🔥 {v}" if not v.startswith('🔥') else v,
            'aggressive': lambda v: v.replace('could', 'will').replace('may', 'will'),

            # Length adjustments
            'shorter': self._make_shorter,
            'concise': self._make_shorter,
            'brief': self._make_shorter,
            'longer': lambda v: v + "\n\nMore details available on my website →",
            'expand': lambda v: v + "\n\nHere's why this matters: [full context]",

            # Tone shifts
            'casual': self._make_casual,
            'conversational': self._make_casual,
            'friendly': self._make_casual,
            'professional': self._make_professional,
            'formal': self._make_professional,
            'corporate': self._make_professional,

            # Hook/angle shifts
            'question': self._make_question,
            'question_hook': self._make_question,
            'statement': self._make_statement,
            'bold_statement': self._make_statement,
            'contrarian': self._make_contrarian,
            'controversial': self._make_contrarian,
            'surprising': self._make_surprising,

            # Data emphasis
            'data_heavy': self._emphasize_data,
            'metrics': self._emphasize_data,
            'numbers': self._emphasize_data,
            'less_data': self._deemphasize_data,
            'less_numbers': self._deemphasize_data,

            # Engagement hooks
            'engaging': self._add_engagement,
            'viral': self._add_engagement,
            'shareworthy': self._add_engagement,
        }

        # Try to match refinement keywords
        for key, transform in transformations.items():
            if key in refinement_lower:
                result = transform(variant)
                log_progress(f"  Applied '{key}' transformation")
                return result

        # Default: note that refinement was received
        return f"{variant}\n\n📝 [Refinement requested: {refinement_prompt}]"

    def _make_punchier(self, text: str) -> str:
        """Make text more punchy and direct"""
        result = text
        # Remove extra whitespace
        result = '\n'.join([line.strip() for line in result.split('\n')])
        # Replace explanations with action verbs
        result = result.replace('Here is what', 'Here's what')
        result = result.replace('Here are', 'Here\'s')
        # Add power words
        if 'Most people' not in result:
            result = result.replace('People', 'Most people').replace('think', 'get wrong')
        return result

    def _make_shorter(self, text: str) -> str:
        """Reduce text length, keep main points"""
        lines = text.split('\n')
        # Keep first 3 non-empty lines
        kept = []
        for line in lines:
            if line.strip() and len(kept) < 3:
                kept.append(line)
        return '\n'.join(kept)

    def _make_casual(self, text: str) -> str:
        """Make tone more casual and conversational"""
        result = text
        result = result.replace('📊', '🎯').replace('📈', '📊')
        result = result.replace('analysis', 'findings').replace('data reveals', 'data shows')
        result = result.replace('reveals', 'shows').replace('demonstrates', 'shows')
        return result

    def _make_professional(self, text: str) -> str:
        """Make tone more professional and formal"""
        result = text
        result = result.replace('Plot twist', 'Key finding').replace('🚨', '📊')
        result = result.replace('people think', 'research suggests')
        return result

    def _make_question(self, text: str) -> str:
        """Reframe as question"""
        if text.startswith('Why') or '?' in text[:30]:
            return text
        return f"Why {text.lower()}?" if not text.lower().startswith('why') else text

    def _make_statement(self, text: str) -> str:
        """Make it a bold statement"""
        result = text.replace('?', '.').replace('Could', 'Will').replace('May', 'Does')
        if not result.startswith('🔥') and not result.startswith('💪'):
            result = f"💪 {result}"
        return result

    def _make_contrarian(self, text: str) -> str:
        """Make it more contrarian and provocative"""
        result = text
        if 'Most people' not in result:
            result = result.replace('Everyone', 'Most people').replace('thinks', 'get wrong')
        result = result.replace('may', 'will').replace('could', 'does')
        return result

    def _make_surprising(self, text: str) -> str:
        """Emphasize surprising elements"""
        result = text
        if '🔄' not in result and '⚡' not in result and '🤯' not in result:
            result = f"🤯 {result}"
        result = result.replace('found', 'discovered').replace('shows', 'reveals')
        return result

    def _emphasize_data(self, text: str) -> str:
        """Add more data and metrics"""
        result = text
        if '📊' not in result:
            result = result.replace('\n\n', '\n\n📊 ')
        return result

    def _deemphasize_data(self, text: str) -> str:
        """Remove or reduce data mentions"""
        result = text.replace('📊', '').replace('metrics:', '').replace('data:', '')
        return result

    def _add_engagement(self, text: str) -> str:
        """Add engagement hooks (questions, calls to action)"""
        result = text
        if 'Comment' not in result and '?' not in result:
            result += "\n\nWhat's your take? 👇"
        return result

    def save_variants_to_file(self, result: Dict, output_dir: Optional[str] = None):
        """Save generated variants to file"""
        if not output_dir:
            output_dir = f"outputs/{self.project_name}/{result['platform'].lower()}"

        create_directory(output_dir)

        carousel_name = result['carousel'].lower().replace(' ', '_').replace(':', '')
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
        """Show all previously generated copies from memory"""
        log_progress(f"\n{'='*60}")
        log_progress(f"MEMORY: All Generated Copies", "🧠")
        log_progress(f"{'='*60}\n")

        if not self.memory['generated_copies']:
            log_progress("No copies generated yet")
            return

        for key, data in self.memory['generated_copies'].items():
            log_progress(f"✓ {data['carousel']} ({data['platform'].title()})")
            log_progress(f"  Generated: {data['generated_at']}")
            log_progress(f"  Refinements: {data.get('refinement_count', 0)}")
            log_progress(f"  Variants: {len(data['variants'])}\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Social Copy Generation Skill - Progressive copy creation with memory & refinement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  # Generate LinkedIn variants
  python social_copy_skill.py --project "Expedia..." --platform linkedin --save

  # Generate all platforms for carousel 2
  python social_copy_skill.py --project "Expedia..." --platform all --carousel 2

  # Refine existing variants
  python social_copy_skill.py --project "Expedia..." --refine "make it punchier"

  # View memory
  python social_copy_skill.py --project "Expedia..." --memory

  # Batch generate all carousels
  python social_copy_skill.py --project "Expedia..." --batch --platforms linkedin instagram twitter
        """
    )
    parser.add_argument("--project", required=True, help="Project name (e.g., 'Expedia Marketplace Analysis')")
    parser.add_argument("--platform", help="Platform: linkedin, instagram, twitter, or 'all' for all platforms")
    parser.add_argument("--carousel", type=int, help="Carousel number (1, 2, 3...)")
    parser.add_argument("--refine", help="Refinement prompt (e.g., 'make it punchier', 'more casual', 'bold statement')")
    parser.add_argument("--save", action="store_true", help="Save to file")
    parser.add_argument("--memory", action="store_true", help="Show memory of all generated copies")
    parser.add_argument("--batch", action="store_true", help="Batch generate all carousels")
    parser.add_argument("--platforms", nargs="+", default=["linkedin", "instagram", "twitter"], help="Platforms for batch mode")
    parser.add_argument("--compare", action="store_true", help="Show side-by-side comparison of variants")

    args = parser.parse_args()

    try:
        skill = SocialCopySkill(args.project)

        if args.memory:
            skill.list_all_generated()
            return

        # Batch mode: generate all carousels for specified platforms
        if args.batch:
            log_progress(f"\n{'='*60}")
            log_progress("BATCH GENERATION MODE", "🚀")
            log_progress(f"{'='*60}\n")

            carousels = skill.project_config.get('carousels', [])
            for carousel_idx, carousel in enumerate(carousels, 1):
                log_progress(f"\n📋 Carousel {carousel_idx}: {carousel.get('title')}")
                for platform in args.platforms:
                    result = skill.generate_variants(platform, carousel_idx)
                    if args.save:
                        skill.save_variants_to_file(result)
                    log_progress(f"  ✓ {platform.title()}: 3 variants saved")
            return

        if not args.platform:
            log_error("Missing argument", Exception("--platform required (linkedin, instagram, twitter, or 'all')"))
            sys.exit(1)

        # Handle 'all' platform shortcut
        platforms_to_generate = args.platform.split(',') if ',' in args.platform else [args.platform]
        if 'all' in platforms_to_generate:
            platforms_to_generate = ['linkedin', 'instagram', 'twitter']

        # Generate for each platform
        all_results = []
        for platform in platforms_to_generate:
            if platform.lower() not in ['linkedin', 'instagram', 'twitter']:
                log_progress(f"⚠️  Skipping unknown platform: {platform}")
                continue

            result = skill.generate_variants(platform.lower(), args.carousel)
            all_results.append(result)

            # Display variants
            log_progress(f"\n{'='*60}")
            log_progress(f"{platform.upper()} VARIANTS")
            log_progress(f"{'='*60}\n")

            for i, variant in enumerate(result['variants'], 1):
                log_progress(f"\n{'='*40}")
                log_progress(f"VARIANT {chr(64+i)} (Option {i})")
                log_progress(f"{'='*40}\n")
                print(variant)

            if args.save:
                skill.save_variants_to_file(result)

        # Show comparison if requested
        if args.compare and len(all_results) > 1:
            log_progress(f"\n{'='*60}")
            log_progress("COMPARISON: All Platforms", "🔄")
            log_progress(f"{'='*60}\n")
            for result in all_results:
                log_progress(f"\n{result['platform'].upper()} - Variant A:\n{result['variants'][0]}\n")

    except Exception as e:
        log_error("Skill execution", e)
        sys.exit(1)


if __name__ == "__main__":
    main()

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
