"""
Copy Generator
Generates platform-specific social media copy from project insights
"""

from typing import Dict, List
from utils import load_yaml, load_json, create_directory, get_output_dir, log_progress, log_error


class SocialCopyGenerator:
    """Generate social media copy for different platforms"""

    def __init__(self, copy_templates: Dict, branding_config: Dict):
        self.templates = copy_templates.get('copy_templates', {})
        self.branding = branding_config.get('branding', {})
        self.cta_templates = branding_config.get('cta_templates', {})
        self.hashtags = copy_templates.get('hashtag_strategies', {})

    def generate_linkedin_post(self, carousel_data: Dict) -> str:
        """Generate LinkedIn carousel post copy with punchy hooks"""
        template = self.templates.get('linkedin', {})

        insight = carousel_data.get('key_insight', '')
        metrics = carousel_data.get('metrics', [])
        takeaway = carousel_data.get('takeaway', '')

        # Start with the insight as the hook (punchy, no fluff)
        post = f"{insight}\n\n"

        # Add metrics
        if metrics:
            metric_str = " | ".join([f"{m.get('label', '')}: {m.get('value', '')}"
                                    for m in metrics[:2]])
            post += f"📊 {metric_str}\n\n"

        # Add the deeper insight
        post += f"{takeaway}\n\n"

        # CTA
        link = carousel_data.get('link', '')
        if link:
            post += f"Read the full analysis → {link}"
        else:
            post += "Read the full analysis on my website"

        return post

    def generate_instagram_post(self, carousel_data: Dict, hashtags_list: List[str] = None) -> str:
        """Generate Instagram carousel post copy with punchy hooks"""
        insight = carousel_data.get('key_insight', '')
        metrics = carousel_data.get('metrics', [{}])
        metric_label = metrics[0].get('label', '') if metrics else ''
        metric_value = metrics[0].get('value', '') if metrics else ''

        # Hook first (punchy, no headline)
        post = f"Plot twist: {insight}\n\n"

        # Quick stat
        if metric_label and metric_value:
            post += f"📊 {metric_label}: {metric_value}\n\n"

        # CTA
        post += f"Full breakdown on my website 🔗 Link in bio"

        if hashtags_list:
            post += f"\n\n{' '.join([f'#{tag}' for tag in hashtags_list])}"

        return post

    def generate_twitter_thread(self, carousel_data: Dict) -> List[str]:
        """Generate Twitter thread with punchy hooks and no fluff"""
        insight = carousel_data.get('key_insight', '')
        insights = carousel_data.get('insights', [])
        takeaway = carousel_data.get('takeaway', '')

        tweets = []

        # Tweet 1: Hook only (no "Thread:" or explanation)
        tweets.append(f"{insight} 🧵")

        # Tweets 2-N: Build narrative with insights
        for i, insight_item in enumerate(insights[:4], start=2):
            tweet = f"{i-1}. {insight_item['headline']}\n\n{insight_item.get('description', '')}"
            if 'metric_value' in insight_item:
                tweet += f"\n\n📊 {insight_item.get('metric_value', '')}"
            tweets.append(tweet)

        # Final tweet: Takeaway + CTA (no "what patterns" fluff)
        final = f"Bottom line: {takeaway}\n\nFull analysis: {carousel_data.get('link', '')}"
        tweets.append(final)

        return tweets

    def generate_tiktok_script(self, carousel_data: Dict) -> Dict:
        """Generate TikTok video script (text overlay for animation)"""
        script = {
            'hook': f"🎯 {carousel_data.get('title', '')}",
            'finding': carousel_data.get('key_insight', ''),
            'metric': f"{carousel_data.get('metrics', [{}])[0].get('value', '')}",
            'takeaway': carousel_data.get('takeaway', ''),
            'cta': "Full analysis on my profile 📊"
        }
        return script

    def generate_blog_teaser(self, carousel_data: Dict) -> Dict:
        """Generate blog teaser image text"""
        teaser = {
            'headline': carousel_data.get('title', ''),
            'subheader': f"{carousel_data.get('metrics', [{}])[0].get('value', '')}",
            'tagline': 'Full analysis inside →'
        }
        return teaser

    def save_copy_to_file(self, content: str, output_path: str):
        """Save copy content to text file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        log_progress(f"Saved copy: {output_path}")

    def save_thread_to_file(self, tweets: List[str], output_path: str):
        """Save Twitter thread to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, tweet in enumerate(tweets, 1):
                f.write(f"Tweet {i}:\n{tweet}\n\n{'='*60}\n\n")
        log_progress(f"Saved thread: {output_path}")


def generate_copy_for_project(project_config: Dict, copy_templates: Dict,
                            branding_config: Dict):
    """Generate social media copy for all carousels"""

    log_progress(f"Generating social copy for {project_config['project_name']}")

    generator = SocialCopyGenerator(copy_templates, branding_config)
    project_name = project_config['project_name']
    hashtags_list = copy_templates.get('hashtag_strategies', {}).get('data_analysis', {}).get('primary', [])

    # Generate copy for each carousel
    for carousel_idx, carousel in enumerate(project_config.get('carousels', []), 1):
        carousel_name = carousel.get('title', f'Carousel {carousel_idx}').lower().replace(' ', '_')

        # LinkedIn
        linkedin_copy = generator.generate_linkedin_post(carousel)
        linkedin_path = f"{get_output_dir(project_name, 'linkedin')}/{carousel_name}_post.txt"
        generator.save_copy_to_file(linkedin_copy, linkedin_path)

        # Instagram
        instagram_copy = generator.generate_instagram_post(carousel, hashtags_list)
        instagram_path = f"{get_output_dir(project_name, 'instagram')}/{carousel_name}_post.txt"
        generator.save_copy_to_file(instagram_copy, instagram_path)

        # Twitter thread
        twitter_tweets = generator.generate_twitter_thread(carousel)
        twitter_path = f"{get_output_dir(project_name, 'twitter')}/{carousel_name}_thread.txt"
        generator.save_thread_to_file(twitter_tweets, twitter_path)

        # TikTok script
        tiktok_script = generator.generate_tiktok_script(carousel)
        tiktok_path = f"{get_output_dir(project_name, 'tiktok')}/{carousel_name}_script.json"
        import json
        create_directory(get_output_dir(project_name, 'tiktok'))
        with open(tiktok_path, 'w') as f:
            json.dump(tiktok_script, f, indent=2)
        log_progress(f"Saved TikTok script: {tiktok_path}")

        # Blog teaser
        blog_teaser = generator.generate_blog_teaser(carousel)
        blog_path = f"{get_output_dir(project_name, 'web')}/{carousel_name}_teaser.json"
        create_directory(get_output_dir(project_name, 'web'))
        with open(blog_path, 'w') as f:
            json.dump(blog_teaser, f, indent=2)
        log_progress(f"Saved blog teaser: {blog_path}")

    log_progress(f"Copy generation complete")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python copy_generator.py <project_config.json>")
        sys.exit(1)

    project_config_path = sys.argv[1]

    try:
        project_config = load_json(project_config_path)
        copy_templates = load_yaml("config/copy_templates.yaml")
        branding_config = load_yaml("config/branding.yaml")

        generate_copy_for_project(project_config, copy_templates, branding_config)

    except Exception as e:
        log_error("Copy generation", e)
        sys.exit(1)
