"""
LLM-Powered Copy Generator
Uses Claude API to generate creative, unique social media copy
Generates 3 A/B variants per carousel per platform
"""

import os
from typing import Dict, List
from anthropic import Anthropic
from utils import create_directory, get_output_dir, log_progress, log_error


class LLMCopyGenerator:
    """Generate social copy using Claude API"""

    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        self.client = Anthropic()

    def generate_linkedin_variants(self, carousel_data: Dict) -> List[str]:
        """Generate 3 LinkedIn copy variants"""
        insight = carousel_data.get('key_insight', '')
        metrics = carousel_data.get('metrics', [])
        takeaway = carousel_data.get('takeaway', '')

        metric_str = " | ".join([f"{m.get('label')}: {m.get('value')}" for m in metrics[:2]])

        prompt = f"""Generate 3 different LinkedIn post copies for this data-driven insight.

INSIGHT: {insight}
METRICS: {metric_str}
TAKEAWAY: {takeaway}

REQUIREMENTS for each variant:
- Start with a punchy hook (no "I discovered", no storytelling)
- 100-150 words total
- Professional but engaging tone
- Include metrics naturally
- End with clear CTA

HOOKS to vary:
1. Variant A: Hook = surprising statement
2. Variant B: Hook = contrarian question
3. Variant C: Hook = data paradox

Format output as:
---VARIANT A---
[copy]

---VARIANT B---
[copy]

---VARIANT C---
[copy]
"""

        response = self.client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        variants = []

        for section in text.split("---VARIANT"):
            if section.strip():
                variant_text = section.replace("A---", "").replace("B---", "").replace("C---", "").strip()
                if variant_text:
                    variants.append(variant_text)

        return variants[:3] if len(variants) >= 3 else variants

    def generate_instagram_variants(self, carousel_data: Dict) -> List[str]:
        """Generate 3 Instagram copy variants"""
        insight = carousel_data.get('key_insight', '')
        metrics = carousel_data.get('metrics', [])

        metric_str = f"{metrics[0].get('label')}: {metrics[0].get('value')}" if metrics else ""

        prompt = f"""Generate 3 different Instagram carousel captions for this insight.

INSIGHT: {insight}
METRIC: {metric_str}

REQUIREMENTS for each variant:
- 80-120 words max
- Casual, conversational tone
- 2-4 emojis per post
- Start with intrigue (plot twist, question, or provocative statement)
- End with hashtags or link in bio mention
- Optimized for mobile scrolling

VARY THE HOOK:
1. Variant A: "Plot twist:" opening
2. Variant B: Question opening
3. Variant C: Surprising fact opening

Format output as:
---VARIANT A---
[copy]

---VARIANT B---
[copy]

---VARIANT C---
[copy]
"""

        response = self.client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        variants = []

        for section in text.split("---VARIANT"):
            if section.strip():
                variant_text = section.replace("A---", "").replace("B---", "").replace("C---", "").strip()
                if variant_text:
                    variants.append(variant_text)

        return variants[:3] if len(variants) >= 3 else variants

    def generate_twitter_variants(self, carousel_data: Dict) -> List[List[str]]:
        """Generate 3 Twitter thread variants (each is a list of tweets)"""
        insight = carousel_data.get('key_insight', '')
        insights = carousel_data.get('insights', [])
        takeaway = carousel_data.get('takeaway', '')

        insights_str = "\n".join([f"- {i.get('headline')}: {i.get('description')}" for i in insights[:3]])

        prompt = f"""Generate 3 different Twitter thread structures for this insight.

MAIN INSIGHT: {insight}
SUPPORTING POINTS:
{insights_str}
TAKEAWAY: {takeaway}

REQUIREMENTS:
- 4-5 tweets per thread
- Punchy, no fluff
- Hook tweet = no explanation, just the insight
- Each variation should have different narrative angle
- Ending tweet = bottom line + link CTA

VARY THE ANGLE:
1. Variant A: Data paradox angle (counterintuitive finding)
2. Variant B: Problem-solution angle (what's broken + how to fix)
3. Variant C: Misconception angle (what people believe wrong)

Format as:
---VARIANT A---
Tweet 1: [hook]
Tweet 2: [insight 1]
Tweet 3: [insight 2]
Tweet 4: [insight 3]
Tweet 5: [takeaway + CTA]

---VARIANT B---
[same structure]

---VARIANT C---
[same structure]
"""

        response = self.client.messages.create(
            model="claude-opus-4-7",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text
        variants = []

        for section in text.split("---VARIANT"):
            if section.strip():
                variant_text = section.replace("A---", "").replace("B---", "").replace("C---", "").strip()
                if variant_text:
                    tweets = [t.strip() for t in variant_text.split("\nTweet") if t.strip()]
                    variants.append(tweets)

        return variants[:3] if len(variants) >= 3 else variants

    def save_variants(self, variants: List[str], output_path: str, platform: str = "linkedin"):
        """Save copy variants to file"""
        create_directory(os.path.dirname(output_path))

        with open(output_path, 'w', encoding='utf-8') as f:
            for i, variant in enumerate(variants, 1):
                f.write(f"{'='*60}\n")
                f.write(f"VARIANT {chr(64+i)} (Option {i})\n")
                f.write(f"{'='*60}\n\n")
                f.write(f"{variant}\n\n")

        log_progress(f"Saved {len(variants)} variants: {output_path}")


def generate_llm_copy_for_project(project_config: Dict, platforms: List[str] = None):
    """Generate LLM copy for all carousels"""

    log_progress("Generating LLM-powered copy variants...")

    try:
        generator = LLMCopyGenerator()
    except ValueError as e:
        log_error("LLM initialization", e)
        return False

    project_name = project_config['project_name']

    if platforms is None:
        platforms = ['linkedin', 'instagram', 'twitter']

    total_generated = 0

    for carousel in project_config.get('carousels', []):
        carousel_name = carousel.get('title', '').lower().replace(' ', '_')

        # LinkedIn variants
        if 'linkedin' in platforms:
            log_progress(f"Generating LinkedIn variants for {carousel_name}...")
            variants = generator.generate_linkedin_variants(carousel)
            if variants:
                output_path = f"{get_output_dir(project_name, 'linkedin')}/{carousel_name}_variants.txt"
                generator.save_variants(variants, output_path, 'linkedin')
                total_generated += len(variants)

        # Instagram variants
        if 'instagram' in platforms:
            log_progress(f"Generating Instagram variants for {carousel_name}...")
            variants = generator.generate_instagram_variants(carousel)
            if variants:
                output_path = f"{get_output_dir(project_name, 'instagram')}/{carousel_name}_variants.txt"
                generator.save_variants(variants, output_path, 'instagram')
                total_generated += len(variants)

        # Twitter variants
        if 'twitter' in platforms:
            log_progress(f"Generating Twitter variants for {carousel_name}...")
            variants = generator.generate_twitter_variants(carousel)
            if variants:
                output_path = f"{get_output_dir(project_name, 'twitter')}/{carousel_name}_variants.txt"
                twitter_variants = []
                for var in variants:
                    twitter_variants.append("\n".join(var))
                generator.save_variants(twitter_variants, output_path, 'twitter')
                total_generated += len(variants)

    log_progress(f"✓ Generated {total_generated} copy variants total")
    return True


if __name__ == "__main__":
    import sys
    from utils import load_json

    if len(sys.argv) < 2:
        print("Usage: python llm_copy_generator.py <project_config.json> [platforms...]")
        sys.exit(1)

    project_config_path = sys.argv[1]
    platforms = sys.argv[2:] if len(sys.argv) > 2 else None

    try:
        project_config = load_json(project_config_path)
        generate_llm_copy_for_project(project_config, platforms)
    except Exception as e:
        log_error("LLM copy generation", e)
        sys.exit(1)
