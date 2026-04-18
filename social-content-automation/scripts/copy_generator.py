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
        """Generate LinkedIn carousel post copy"""
        template = self.templates.get('linkedin', {})

        headline = carousel_data.get('title', '')
        insight = carousel_data.get('key_insight', '')
        metrics = carousel_data.get('metrics', [])
        takeaway = carousel_data.get('takeaway', '')

        # Build metric string
        metric_str = " • ".join([f"{m.get('label', '')}: {m.get('value', '')}"
                               for m in metrics[:2]])

        post = f"🔍 {headline}\n\n"
        post += f"In a recent analysis, I discovered: {insight}\n\n"
        post += f"📊 {metric_str}\n\n"
        post += f"This suggests: {takeaway}\n\n"
        post += f"Read the full case study → {carousel_data.get('link', '')}\n\n"
        post += f"What patterns have you noticed? Comment below."

        return post

    def generate_instagram_post(self, carousel_data: Dict, hashtags_list: List[str] = None) -> str:
        """Generate Instagram carousel post copy"""
        template = self.templates.get('instagram', {})

        headline = carousel_data.get('title', '')
        insight = carousel_data.get('key_insight', '')
        metric_label = carousel_data.get('metrics', [{}])[0].get('label', '')
        metric_value = carousel_data.get('metrics', [{}])[0].get('value', '')

        post = f"💡 {headline}\n\n"
        post += f"{insight}\n\n"
        post += f"📊 {metric_label}: {metric_value}\n\n"
        post += f"Full breakdown on my website 🔗 Link in bio\n\n"

        if hashtags_list:
            post += " ".join([f"#{tag}" for tag in hashtags_list])

        return post

    def generate_twitter_thread(self, carousel_data: Dict) -> List[str]:
        """Generate Twitter thread (list of tweets)"""
        headline = carousel_data.get('title', '')
        insights = carousel_data.get('insights', [])
        metrics = carousel_data.get('metrics', [])

        tweets = []

        # Tweet 1: Hook
        tweets.append(f"Thread: {headline} 🧵\n\nWhat I found will surprise you. Here's the data 👇")

        # Tweets 2-N: Insights
        for i, insight in enumerate(insights[:5], start=2):
            metric_str = f" {metrics[i-2]['value']}" if i-2 < len(metrics) else ""
            tweet = f"{i-1}. {insight['headline']}\n\n{insight.get('description', '')}{metric_str}"
            tweets.append(tweet)

        # Final tweet: CTA
        cta = f"Full analysis + recommendations: {carousel_data.get('link', '')}\n\nWhat patterns have you noticed? Reply below."
        tweets.append(cta)

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
