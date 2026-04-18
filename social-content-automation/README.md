# Social Content Automation System

Fully automate social media carousel generation from portfolio projects. Convert any project (data analysis, web app, tool, product analysis) into multi-platform social content with zero manual image editing.

**Goal:** Drop a project deliverable → Run automation → Review copy → Post across LinkedIn, Instagram, TikTok/Reels, Twitter

---

## Quick Start

### 1. Set up environment
```bash
cd social-content-automation
pip install -r requirements.txt
```

### 2. Create project config
```bash
cp templates/project_config_template.json config/projects/2026-05-myproject.json
# Edit the config with your project details
```

### 3. Run full pipeline
```bash
python scripts/batch_generate.py --config config/projects/2026-05-myproject.json
```

### 4. Review & Post
- Images ready in `outputs/2026-05-myproject/[platform]/`
- Copy ready in `outputs/2026-05-myproject/[platform]/[carousel_name]_post.txt`
- Edit copy as needed, upload images/copy to each platform

---

## System Architecture

### Three-Layer Pipeline

```
INPUT
  ↓
[Layer 1] Project Intake
  - Extract insights, metrics, visuals from deliverable
  ↓
[Layer 2] Content Generation
  - Build carousel slides using templates
  - Generate platform-specific copy
  ↓
[Layer 3] Social Export
  - LinkedIn carousels (1080×1350px, 6-8 slides)
  - Instagram carousels (1080×1080px, 5-7 slides, square)
  - TikTok/Reels videos (1080×1920px, 15-60s)
  - Twitter threads (5-8 tweets)
  - Blog teasers (1200×630px)
  ↓
OUTPUT: Ready-to-post content
```

### Key Principle
- **Automation handles:** Visuals, design, layout, formatting
- **You handle:** Copy review and refinement only

---

## Project Structure

```
social-content-automation/
├── README.md                          # This file
├── CLAUDE.md                          # Project guidelines for Claude Code
├── requirements.txt                   # Python dependencies
├── config/
│   ├── branding.yaml                  # Global brand colors, fonts, logo
│   ├── platforms.yaml                 # Platform specs (dimensions, etc.)
│   ├── copy_templates.yaml            # Platform-specific copy patterns
│   └── projects/                      # Per-project configs (create here)
│       └── 2026-05-myproject.json     # Example project config
├── scripts/
│   ├── batch_generate.py              # Main orchestration script
│   ├── carousel_generator.py          # Generate carousel slide images
│   ├── format_converter.py            # Convert to platform formats
│   ├── copy_generator.py              # Generate social copy
│   └── utils.py                       # Shared utilities
├── templates/
│   └── project_config_template.json   # Template for new projects
├── assets/
│   └── logo.png                       # Your logo (customize)
└── outputs/                           # Auto-generated outputs
    └── 2026-05-myproject/             # Per-project folder
        ├── linkedin/                  # LinkedIn carousel images + copy
        ├── instagram/                 # Instagram carousel images + copy
        ├── tiktok/                    # TikTok video script + metadata
        ├── twitter/                   # Twitter thread copy
        └── web/                       # Blog teaser images + metadata
```

---

## Workflow (Monthly)

### Week 1: Project Completion
- Finish your portfolio project (deck, web app, analysis, etc.)
- Document key insights, metrics, findings

### Week 2: Generate Content
```bash
# 1. Create project config
cp templates/project_config_template.json config/projects/2026-05-[name].json

# 2. Fill in your project details (insights, metrics, links)

# 3. Run automation
python scripts/batch_generate.py --config config/projects/2026-05-[name].json

# Output: 4 carousels × 5 formats = 20+ files ready to post
```

### Week 3-6: Weekly Social Posts
- **Monday:** Post carousel 1 on LinkedIn
- **Wednesday:** Post carousel 1 on Instagram (maintains 3×3 grid)
- **Thursday:** Post carousel 1 Twitter thread
- **Friday:** Post carousel 1 TikTok video

- **Week 4:** Post carousel 2 (repeat schedule)
- **Week 5:** Post carousel 3
- **Week 6:** Post carousel 4

One carousel per week across platforms = consistent monthly visibility

---

## Configuration

### Project Config Fields

**Top-level fields:**
```json
{
  "project_name": "Expedia Marketplace Analysis",
  "date": "2026-04-18",
  "project_type": "data_analysis",
  "website_link": "https://yoursite.com/expedia",
  "carousels": [...]
}
```

**Per-carousel fields:**
```json
{
  "title": "The Luxury Hotel Problem",
  "subtitle": "Why luxury underperforms",
  "key_insight": "Main finding headline",
  "insights": [
    {
      "headline": "Finding 1",
      "metric_label": "Conversion Rate",
      "metric_value": "2.20%",
      "description": "Why this matters"
    }
  ],
  "metrics": [
    {
      "label": "Key Stat",
      "value": "27% lower"
    }
  ],
  "takeaway": "What this means for strategy"
}
```

### Branding Config

Edit `config/branding.yaml` to customize:
- Primary/secondary colors
- Fonts
- Logo placement
- CTA templates
- Social media handles
- Hashtags

### Platform Specs

Edit `config/platforms.yaml` to adjust:
- Image dimensions per platform
- Slides per carousel
- Posting times/days recommendations
- Copy length guidelines

---

## Generated Outputs

### LinkedIn Carousels
- **Files:** `linkedin/carousel_1_title_1.png`, `carousel_1_title_2.png`, etc.
- **Format:** 1080×1350px PNG
- **Copy:** `linkedin/carousel_1_title_post.txt` (100-150 words, professional tone)
- **Best for:** B2B, thought leadership, portfolio showcase

### Instagram Carousels
- **Files:** `instagram/carousel_1_title_*.jpg` (square, 1080×1080px)
- **Format:** 1080×1080px JPG (optimized for mobile)
- **Copy:** `instagram/carousel_1_title_post.txt` (80-120 words, casual tone + emojis)
- **Grid optimization:** 3 carousels per month = clean 3×3 grid

### Twitter Threads
- **Files:** `twitter/carousel_1_title_thread.txt`
- **Format:** Individual tweets ready to copy/paste
- **Structure:** 5-8 tweets per thread (hook → narrative → CTA)
- **Tone:** Conversational, punchy, no jargon

### TikTok/Reels Scripts
- **Files:** `tiktok/carousel_1_title_script.json`
- **Content:** Text overlay scripts for animation
- **Format:** JSON with hook, finding, metric, takeaway, CTA
- **Note:** Use video editor or AI video tool to animate (moviepy integration coming)

### Blog/Web Teasers
- **Files:** `web/carousel_1_title_teaser.png`
- **Format:** 1200×630px PNG (standard social preview)
- **Use:** Blog embeds, email headers, newsletter covers

---

## Advanced Usage

### Generate for specific platforms only
```bash
python scripts/batch_generate.py \
  --config config/projects/2026-05-myproject.json \
  --platforms linkedin instagram twitter
```

### Run individual scripts
```bash
# Just generate carousels
python scripts/carousel_generator.py config/projects/2026-05-myproject.json linkedin

# Just convert formats
python scripts/format_converter.py config/projects/2026-05-myproject.json

# Just generate copy
python scripts/copy_generator.py config/projects/2026-05-myproject.json
```

---

## Customization

### Add a new platform
1. Add platform specs to `config/platforms.yaml`
2. Update `format_converter.py` to handle new dimensions
3. Add copy template to `config/copy_templates.yaml`
4. Test with sample project

### Change branding
1. Edit `config/branding.yaml` (colors, fonts, logo)
2. Rerun `batch_generate.py` to apply new branding to all projects

### Adjust carousel structure
Edit `carousel_generator.py` to customize:
- Slide layouts
- Font sizes
- Color schemes
- Logo placement

---

## Troubleshooting

### Import errors
```bash
pip install -r requirements.txt --upgrade
```

### Image files not found
- Ensure carousel images generated in `outputs/[project]/linkedin/` first
- Format converter reads from LinkedIn folder and exports to others

### Copy too long
- Edit platform word counts in `config/copy_templates.yaml`
- Adjust `copy_generator.py` to use different templates

### Want to customize generated copy
- All copy is generated from templates in `config/copy_templates.yaml`
- Edit templates or manually refine generated .txt files

---

## Next Steps

1. **Fill in branding:** Edit `config/branding.yaml` with your colors/logo
2. **Create first project config:** Copy template, add your project details
3. **Run automation:** `python scripts/batch_generate.py --config config/projects/2026-05-[name].json`
4. **Review outputs:** Check `outputs/` folder for images and copy
5. **Post to social:** Upload images, copy/paste text to each platform

---

## Integration with Future Repos

When creating a new dedicated repo for this system:
1. Copy entire `social-content-automation/` folder to new repo
2. Initialize git and push
3. Continue using same workflow (configs in `config/projects/`)
4. Outputs can be in `.gitignore` or stored separately

---

## Support & Documentation

- **CLAUDE.md** — Project guidelines and architecture
- **config/** — All customization points
- **templates/** — Examples and templates for new projects
- **scripts/** — Core automation code (well-commented)

---

**Version:** 1.0  
**Last Updated:** 2026-04-18  
**Status:** Ready for MVP testing on Expedia project
