# Social Content Automation System

## Project Purpose
This system converts portfolio projects (decks, web apps, analyses, tools) into multi-platform social media content. **Goal:** Fully automate carousel + video + copy generation so you only review and edit copy.

**Workflow:** Drop project deliverable → Run automation → Review generated copy → Post across LinkedIn, Instagram, TikTok/Reels, Twitter

---

## Architecture

### Three-Layer Pipeline
1. **Project Intake:** Extract insights, metrics, visuals from any project format (PowerPoint, Jupyter, HTML, etc.)
2. **Content Generation:** Build carousels, videos, threads using templates and styling
3. **Social Export:** Generate platform-specific formats (images, videos, copy)

### Key Design Principle
- **Automation handles visuals/design:** No manual image editing
- **User handles copy only:** Review and refine generated text
- **Config-driven:** Easily adapt to new projects via YAML/JSON config files

---

## Project Structure

```
social-content-automation/
├── CLAUDE.md                          # This file
├── README.md                          # Usage guide
├── requirements.txt                   # Python dependencies
├── config/
│   ├── branding.yaml                  # Global branding (colors, fonts, logo)
│   ├── platforms.yaml                 # Platform specs (dimensions, slide counts)
│   └── templates/
│       ├── carousel_template.pptx     # Base PowerPoint template
│       └── copy_templates.yaml        # Platform-specific copy patterns
├── scripts/
│   ├── carousel_generator.py          # Generate carousel slides from data
│   ├── format_converter.py            # Convert to platform-specific formats
│   ├── copy_generator.py              # Generate social copy
│   ├── video_generator.py             # Generate TikTok/Reels videos
│   ├── batch_generate.py              # Orchestrate full pipeline
│   └── utils.py                       # Shared utilities
├── templates/
│   └── project_config_template.json   # Template for new projects
├── assets/
│   ├── logo.png                       # Your logo
│   └── branding_guide.md              # Visual brand guidelines
└── outputs/
    └── [project-name]/                # Output folders (auto-created per project)
        ├── linkedin/
        ├── instagram/
        ├── tiktok/
        ├── twitter/
        └── web/
```

---

## Workflow

### For Each New Project (Monthly)

**Step 1: Create Project Config**
```bash
cp templates/project_config_template.json config/projects/2026-05-[project-name].json
# Edit with insights, metrics, slides, branding
```

**Step 2: Run Full Pipeline**
```bash
python scripts/batch_generate.py --config config/projects/2026-05-[project-name].json
```

**Step 3: Review Generated Copy**
- Open `outputs/[project-name]/twitter/thread_1.txt` (and other platforms)
- Edit for tone, accuracy, CTAs
- Keep auto-generated copy as starting point

**Step 4: Export to Social**
- LinkedIn: Upload carousel images directly
- Instagram: Use square JPG images
- TikTok/Reels: Upload generated .mp4 files
- Twitter: Copy/paste text from generated .txt files

---

## Key Files & Their Responsibilities

### `carousel_generator.py`
- Reads project config (which insights, slide ranges, metrics)
- Extracts visuals from source (PowerPoint, matplotlib charts, etc.)
- Builds carousel slides using template
- Outputs: PNG/JPG files (one per slide, per carousel)

### `format_converter.py`
- Takes carousel images as input
- Resizes/crops for each platform (LinkedIn widescreen, IG square, etc.)
- Applies platform-specific styling
- Outputs: Format-ready images

### `copy_generator.py`
- Takes insight data (headline, metric, finding)
- Generates platform-specific copy:
  - LinkedIn: Professional, 100-150 words
  - Instagram: Casual, 80-120 words, emoji-friendly
  - Twitter: 5-8 tweets, conversational
  - Email/Web: Formal copy for embeds
- Outputs: Text files (.txt, .md)

### `video_generator.py`
- Creates animated TikTok/Reels videos
- Animated data reveal + text overlays + CTA
- Outputs: .mp4 files (9:16 aspect ratio)

### `batch_generate.py`
- Orchestrates the full pipeline
- Runs: carousel → format converter → copy generator → video generator
- Error handling and progress tracking
- Single command: `python batch_generate.py --config <config.json>`

---

## Customization Points

### Add New Project Type
1. Edit `project_config_template.json` with new fields
2. Update `carousel_generator.py` to extract visuals from new format
3. Test with sample project

### Add New Platform
1. Add platform specs to `config/platforms.yaml`
2. Add conversion logic to `format_converter.py`
3. Add copy template to `config/templates/copy_templates.yaml`
4. Test output format

### Update Branding
1. Edit `config/branding.yaml` (colors, fonts, logo path)
2. Ensure logo uploaded to `assets/logo.png`
3. Rerun batch_generate for all projects to apply new branding

---

## Dependencies & Setup (See Setup Instructions Below)

Required Python packages:
- `python-pptx` — PowerPoint generation
- `pillow` — Image processing
- `matplotlib` — Chart generation
- `imageio` — Video frame generation
- `moviepy` — Video file creation
- `pyyaml` — Config file parsing
- `pandas` — Data handling

Optional but recommended:
- `beautifulsoup4` — HTML parsing (for web app projects)
- `jupyter` — Notebook analysis

---

## Important Notes

1. **Automation is template-based:** New projects need a config file to specify what to generate
2. **Copy is AI-generated but needs review:** Always edit generated copy for tone and accuracy
3. **Visuals are automatic:** No manual image editing required
4. **Reusable across projects:** Same scripts work for decks, web apps, analyses, tools
5. **Incrementally testable:** Can run each script independently or full pipeline via batch_generate.py

---

## For Future Reference

When moving this to a new repo:
- This CLAUDE.md documents the system design
- See SETUP.md for installation instructions
- See README.md for usage examples
