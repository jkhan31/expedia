# Tools, Plugins, and Integrations Guide

This document outlines all optional tools, MCP servers, plugins, and CLI integrations you should consider adding when migrating this project to a new standalone repo.

---

## 1. Claude Code Settings & Hooks

### Add to `.claude/settings.json`

**File:** `.claude/settings.json`

```json
{
  "project_instructions": {
    "claude_code": {
      "read_only_tools": ["config/", "templates/", "docs/"],
      "write_allowed": ["scripts/", "config/projects/"],
      "execute_tools": ["python", "bash"]
    }
  },
  "permissions": {
    "execute": {
      "python": {
        "allowed_patterns": [
          "python scripts/batch_generate.py",
          "python scripts/carousel_generator.py",
          "python scripts/copy_generator.py",
          "python scripts/format_converter.py"
        ]
      },
      "bash": {
        "allowed_commands": [
          "mkdir",
          "cp",
          "ls",
          "git add",
          "git commit",
          "git push"
        ]
      }
    }
  },
  "environment": {
    "PYTHONPATH": "./scripts",
    "PROJECT_ROOT": ".",
    "CONFIG_DIR": "./config"
  },
  "hooks": {
    "before_script_execution": "Validate that config files are well-formed YAML/JSON",
    "after_generation_complete": "Notify user that outputs are ready in outputs/ folder"
  }
}
```

### Optional: Add Hooks to Run Validation

Create `.claude/hooks/before-commit.sh`:
```bash
#!/bin/bash
# Validate all project configs before commit
python scripts/validate_configs.py
if [ $? -ne 0 ]; then
  echo "Config validation failed. Fix errors before committing."
  exit 1
fi
```

Then add to settings.json:
```json
{
  "hooks": {
    "pre-commit": ".claude/hooks/before-commit.sh"
  }
}
```

---

## 2. Claude API / Anthropic SDK Integration

### For Future AI-Powered Copy Generation

Currently, copy is generated from templates. To enable **AI-generated, truly unique copy** for each carousel:

**Option A: Use Claude API directly**

Install:
```bash
pip install anthropic
```

Create `scripts/ai_copy_generator.py`:
```python
from anthropic import Anthropic

client = Anthropic()

def generate_platform_copy(carousel_data, platform):
    """Use Claude to generate platform-specific copy"""
    prompt = f"""
    Generate {platform} copy for this carousel:
    
    Title: {carousel_data['title']}
    Insight: {carousel_data['key_insight']}
    Metrics: {carousel_data['metrics']}
    
    Requirements:
    - Platform: {platform}
    - Tone: {'professional' if platform == 'linkedin' else 'conversational'}
    - Length: {'100-150 words' if platform == 'linkedin' else '80-120 words'}
    """
    
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
```

Usage:
```bash
export ANTHROPIC_API_KEY="your-api-key"
python scripts/ai_copy_generator.py
```

**Option B: Use Claude Code (simpler)**
Just ask Claude Code to "Generate better copy for carousel 1" and it will edit the .txt files.

---

## 3. GitHub Integration

### GitHub CLI Setup

Install [GitHub CLI](https://cli.github.com/):
```bash
brew install gh  # macOS
# or https://github.com/cli/cli for other OS
```

Authenticate:
```bash
gh auth login
```

**Useful commands:**

```bash
# Create new repo
gh repo create social-content-automation --public

# Clone repo
gh repo clone username/social-content-automation

# Create issue for new project
gh issue create --title "Generate content for Q2 project" --body "See config/projects/2026-05-project.json"

# Push changes
git push origin main
```

### Add GitHub Actions (Optional CI/CD)

Create `.github/workflows/validate-configs.yml`:

```yaml
name: Validate Configs

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scripts/validate_configs.py
```

This auto-validates all config files on every push.

---

## 4. MCP Servers (For Advanced Integration)

MCP servers enable Claude to interact with external services. Consider these:

### 4A. Image Storage MCP (AWS S3 / Google Cloud)

**Purpose:** Auto-upload generated images to cloud storage

**Option 1: AWS S3**

Install:
```bash
pip install boto3
```

Create `scripts/s3_uploader.py`:
```python
import boto3
import os

def upload_project_outputs(project_name, bucket_name):
    """Upload generated images to S3"""
    s3 = boto3.client('s3')
    output_dir = f"outputs/{project_name}"
    
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = f"social-content/{project_name}/{file}"
            s3.upload_file(local_path, bucket_name, s3_key)
            print(f"Uploaded: {s3_key}")
```

Usage:
```bash
python scripts/s3_uploader.py my-project my-bucket
```

### 4B. Social Media API MCP (Future)

These would allow auto-posting to social platforms:

**LinkedIn API:**
- Manual setup required (LinkedIn Developer portal)
- Would enable: Auto-post carousels to LinkedIn
- Documentation: https://learn.microsoft.com/en-us/linkedin/marketing/

**Twitter/X API:**
- Free tier available (Twitter Developer portal)
- Would enable: Auto-post threads to Twitter
- Documentation: https://developer.twitter.com/

**Instagram Business API:**
- Requires Facebook Business account
- Would enable: Auto-post carousels to Instagram
- Documentation: https://developers.facebook.com/

**Note:** These are manual integrations (not pre-built MCP servers). Building MCP wrappers is advanced.

---

## 5. Video Generation Tools

### Automated TikTok/Reels Video Creation

Current system generates **scripts** (JSON). To create actual **videos**, you have options:

#### Option A: moviepy (Python library - included in requirements.txt)

Already installed! Create `scripts/video_generator.py`:

```python
from moviepy.editor import *
import json

def create_tiktok_video(script_path, output_path):
    """Create TikTok video from script"""
    
    with open(script_path) as f:
        script = json.load(f)
    
    # Create clips
    clips = []
    
    # Hook text (1-2s)
    hook = TextClip(script['hook'], fontsize=60, color='white')
    clips.append(hook.set_duration(2))
    
    # Finding text (3-5s)
    finding = TextClip(script['finding'], fontsize=40, color='white')
    clips.append(finding.set_duration(4))
    
    # Metric display (3-5s)
    metric = TextClip(script['metric'], fontsize=80, color='yellow')
    clips.append(metric.set_duration(4))
    
    # Concatenate and export
    final = concatenate_videoclips(clips)
    final.write_videofile(output_path, fps=24, verbose=False)
```

Usage:
```bash
python scripts/video_generator.py config/projects/2026-05-project.json
```

#### Option B: CapCut (No-code Desktop App)

Manual but fast approach:
1. Generate carousel images (already done)
2. Import 5 images into CapCut
3. Add text overlays from `tiktok/carousel_name_script.json`
4. Export as vertical video (9:16)

#### Option C: Elevenlabs or Synthesia (AI Video Tools)

For more polished videos with voiceover:
- Upload carousel images
- Add AI-generated voiceover
- Auto-sync text overlays
- Export as MP4

---

## 6. Notification & Scheduling Tools

### 6A. Scheduling Posts (Buffer, Later, or Manual)

**Buffer** (Recommended):
- Integrates with LinkedIn, Instagram, Twitter, TikTok
- Free plan: 3 social channels, 10 posts per calendar month
- Workflow: Generate content → Upload to Buffer → Schedule for week

**Later** (Instagram-focused):
- Visual content calendar
- Team collaboration
- Instagram, TikTok, Pinterest focus

**Hootsuite** (Enterprise):
- Multi-platform scheduling
- Analytics and reporting
- Higher cost but full-featured

### 6B. Reminders & Notifications

**Slack Webhook** (Optional):

Create `scripts/notify_slack.py`:
```python
import requests
import json

def notify_content_ready(project_name):
    """Send Slack notification when content is ready"""
    
    webhook_url = "YOUR_SLACK_WEBHOOK_URL"
    
    message = {
        "text": f"✅ Social content ready for {project_name}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"📱 *{project_name}* content generated\n\n• LinkedIn: 4 carousels\n• Instagram: 4 carousels\n• Twitter: 4 threads\n• TikTok: 4 scripts\n\n👉 Check outputs/ folder"
                }
            }
        ]
    }
    
    requests.post(webhook_url, json=message)
```

### 6C. Cron Jobs (Automated Reminders)

**macOS/Linux:**

Create cron job to remind you to post:
```bash
# Edit crontab
crontab -e

# Add weekly reminder (Monday 9 AM)
0 9 * * 1 /usr/bin/say "Remember to post this week's carousel"
```

---

## 7. Development Tools to Add

### 7A. Code Quality

**Black** (Code formatter):
```bash
pip install black
black scripts/  # Auto-format code
```

**Flake8** (Linter):
```bash
pip install flake8
flake8 scripts/  # Check for errors
```

**mypy** (Type checking):
```bash
pip install mypy
mypy scripts/  # Check types
```

### 7B. Testing

**pytest** (Testing framework):
```bash
pip install pytest
pytest tests/  # Run tests
```

Create `tests/test_carousel_generator.py`:
```python
import pytest
from carousel_generator import CarouselSlideGenerator

def test_hex_to_rgb():
    gen = CarouselSlideGenerator({}, {})
    assert gen.hex_to_rgb("#FF0000") == (255, 0, 0)
```

---

## 8. Documentation Tools

### 8A. Auto-Generate API Docs

**Sphinx** (Documentation generator):
```bash
pip install sphinx
sphinx-quickstart docs/
```

### 8B. Diagram Generation

For visualizing the pipeline, consider:

**Mermaid** (Markdown diagrams):
```markdown
graph TD
    A[Project Config] --> B[Carousel Generator]
    B --> C[Format Converter]
    C --> D[Copy Generator]
    D --> E[Output Folder]
    E --> F[Post to Social]
```

---

## Implementation Timeline

### Phase 1 (Immediate)
- ✅ Set up basic Python environment
- ✅ Test batch_generate.py on Expedia project
- ⚠️ Add `.claude/settings.json` with basic permissions

### Phase 2 (Next Month)
- ⚠️ Set up GitHub repo
- ⚠️ Add GitHub Actions for config validation
- ⚠️ Set up Buffer or Later for scheduling

### Phase 3 (Quarterly)
- ⚠️ Add Claude API integration for AI copy generation
- ⚠️ Implement moviepy video generation
- ⚠️ Set up S3 or cloud storage for outputs

### Phase 4 (As Needed)
- ⚠️ Build MCP wrappers for social media APIs
- ⚠️ Implement Slack notifications
- ⚠️ Add advanced analytics and A/B testing

---

## Summary Table

| Tool | Purpose | Complexity | Cost | Priority |
|------|---------|-----------|------|----------|
| GitHub | Version control | Low | Free | Phase 2 |
| Buffer | Schedule posts | Low | Free | Phase 2 |
| Claude API | AI copy generation | Medium | Pay-per-use | Phase 3 |
| moviepy | Auto-generate videos | Medium | Free | Phase 3 |
| AWS S3 | Cloud storage | Medium | Cheap | Phase 3 |
| Slack | Notifications | Low | Free | Phase 3 |
| Twitter API | Auto-post threads | Medium | Moderate | Phase 4 |
| LinkedIn API | Auto-post carousels | High | Free | Phase 4 |

---

## Getting Help

1. **Documentation:** See README.md, CLAUDE.md, SETUP.md
2. **Config issues:** Check templates/project_config_template.json
3. **Code questions:** Each script has detailed comments
4. **MCP/Integration issues:** Refer to official docs (GitHub, Anthropic, etc.)

---

**Version:** 1.0  
**Last Updated:** 2026-04-18  
**Status:** Reference guide for future enhancements
