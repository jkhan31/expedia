# Getting Started: 5-Minute Quick Start

## What You Have

✅ **Fully functional social content automation system** ready to generate carousels for the Expedia project and future projects.

```
social-content-automation/
├── Automation scripts (carousel, copy, format generation)
├── Configuration files (branding, platforms, copy templates)
├── Documentation (README, CLAUDE.md, SETUP.md)
└── Templates (project config template)
```

---

## Quick Start (5 Minutes)

### Step 1: Install Dependencies (2 min)
```bash
cd /home/user/expedia/social-content-automation
pip install -r requirements.txt
```

### Step 2: Create Project Config (2 min)

Copy and edit template:
```bash
cp templates/project_config_template.json config/projects/2026-04-expedia.json
```

Edit `config/projects/2026-04-expedia.json` and fill in:
- Project name: "Expedia Marketplace Analysis"
- Website link: Your project URL
- Carousels: 4 (Problem, Price Myth, Ranking Impact, Quality Gap)
- Insights: Key metrics from each carousel

**Example for Carousel 1 (Luxury Hotel Problem):**
```json
{
  "title": "The Luxury Hotel Problem",
  "key_insight": "Luxury hotels convert 27% less often than budget hotels",
  "insights": [
    {
      "headline": "The Booking Rate Gap",
      "metric_label": "Luxury Booking Rate",
      "metric_value": "2.20%",
      "description": "Luxury hotels book at significantly lower rates"
    }
  ],
  "metrics": [
    {
      "label": "Conversion Gap",
      "value": "27% lower"
    }
  ],
  "takeaway": "Price isn't the problem—positioning and trust are"
}
```

### Step 3: Run Automation (1 min)
```bash
python scripts/batch_generate.py --config config/projects/2026-04-expedia.json
```

### Step 4: Check Outputs
```bash
ls -la outputs/Expedia\ Marketplace\ Analysis/
# Should see: linkedin/, instagram/, twitter/, tiktok/, web/
```

---

## What Gets Generated

After running batch_generate.py:

```
outputs/Expedia Marketplace Analysis/
├── linkedin/
│   ├── carousel_1_*.png          ← Ready to upload
│   ├── carousel_2_*.png
│   └── carousel_1_post.txt       ← Copy to review/edit
├── instagram/
│   ├── carousel_1_*.jpg          ← Square format
│   ├── carousel_2_*.jpg
│   └── carousel_1_post.txt       ← Copy (casual tone)
├── twitter/
│   ├── carousel_1_thread.txt     ← 5-8 tweets ready to copy/paste
│   ├── carousel_2_thread.txt
│   └── ...
├── tiktok/
│   ├── carousel_1_script.json    ← Text overlay script
│   ├── carousel_2_script.json
│   └── ...
└── web/
    ├── carousel_1_teaser.json    ← Blog preview text
    ├── carousel_2_teaser.json
    └── ...
```

---

## Next Steps (30 Minutes)

### 1. Review Generated Copy (10 min)
Open and read:
- `outputs/Expedia.../linkedin/carousel_1_post.txt`
- `outputs/Expedia.../instagram/carousel_1_post.txt`
- `outputs/Expedia.../twitter/carousel_1_thread.txt`

Edit for tone, accuracy, and CTAs. Keep the auto-generated version as baseline.

### 2. Test on LinkedIn (10 min)
- Open LinkedIn → Post → Create a carousel post
- Upload images from `outputs/Expedia.../linkedin/`
- Paste copy from `.txt` file
- Schedule or publish

### 3. Repeat for Instagram, Twitter (10 min)
- Instagram: Use square JPG images from `instagram/` folder
- Twitter: Copy/paste thread text into Twitter reply chain
- Post or schedule

---

## Understanding the System

### How It Works

```
1. You create project_config.json with:
   - Project title
   - Key insights
   - Metrics
   - Website link

2. batch_generate.py orchestrates:
   ├─ carousel_generator.py
   │  └─ Creates slide images from your data
   ├─ format_converter.py
   │  └─ Resizes for each platform (LinkedIn, IG, TikTok, etc.)
   ├─ copy_generator.py
   │  └─ Writes platform-specific text
   └─ outputs/ folder
      └─ Ready-to-post content

3. You review copy, upload images/text to social
```

### Key Principle
- **Automation creates:** Images, layouts, initial copy, formatting
- **You refine:** Only the text/copy (images are auto-designed)

---

## File Explanations

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project guidelines and architecture |
| `README.md` | Full documentation |
| `SETUP.md` | Detailed installation guide |
| `TOOLS_AND_INTEGRATIONS.md` | Optional tools to add later |
| `config/branding.yaml` | Your brand colors, fonts, logo |
| `config/platforms.yaml` | Platform specs (dimensions, etc.) |
| `config/copy_templates.yaml` | Social copy templates by platform |
| `scripts/batch_generate.py` | Main automation script (run this) |
| `templates/project_config_template.json` | Template for new projects |

---

## Customization

### Change Brand Colors
Edit `config/branding.yaml`:
```yaml
branding:
  primary_color: "#1F3A5D"      # Change to your color
  secondary_color: "#FF6B35"
```

### Change Social Copy Tone
Edit `config/copy_templates.yaml`:
```yaml
copy_templates:
  linkedin:
    example: |
      🔍 {insight_headline}
      
      [Your custom text here...]
```

### Add New Carousel
Add to `config/projects/2026-04-expedia.json`:
```json
{
  "carousel_number": 4,
  "title": "New Carousel Title",
  "key_insight": "Main finding",
  "insights": [...],
  "metrics": [...]
}
```

---

## When You're Ready to Create New Repo

1. **Copy entire folder** to new GitHub repo
2. **Add to CLAUDE.md** any Claude Code-specific instructions
3. **See TOOLS_AND_INTEGRATIONS.md** for GitHub Actions, MCP servers, etc.

```bash
# Create new repo, push this folder
gh repo create social-content-automation --public
git init
git add .
git commit -m "Initial commit: Social content automation"
git push -u origin main
```

---

## FAQ

**Q: Do I need to edit images?**
A: No! All images are auto-generated. You only review/edit text copy.

**Q: Can I use this for other projects (web apps, tools, etc.)?**
A: Yes! Create a new project config and run the pipeline. Same system works for any project.

**Q: How long does it take to generate content?**
A: ~30 seconds to run automation. Then 10-15 minutes to review/edit copy.

**Q: Can I customize the design?**
A: Edit `scripts/carousel_generator.py` to change fonts, colors, layouts. Or update `config/branding.yaml` for colors/fonts.

**Q: How many platforms can I post to?**
A: Currently supports: LinkedIn, Instagram, Twitter, TikTok/Reels, Blog. Easy to add more.

**Q: What if the copy isn't perfect?**
A: Edit the `.txt` files before uploading. Templates are starting points, not final copy.

---

## Support & Documentation

- **Setup issues:** See SETUP.md
- **Usage questions:** See README.md
- **Integration ideas:** See TOOLS_AND_INTEGRATIONS.md
- **Code questions:** Check script comments or ask Claude Code

---

## What's Next?

### Right Now
- [ ] Install requirements.txt
- [ ] Create first project config
- [ ] Run batch_generate.py
- [ ] Review and post to one platform

### This Week
- [ ] Post to all 4 platforms (LinkedIn, IG, Twitter, TikTok scripts)
- [ ] Customize branding.yaml with your colors
- [ ] Create 2-3 more project configs for variety

### Later (Phase 2)
- [ ] Create new GitHub repo
- [ ] Set up GitHub Actions for config validation
- [ ] Integrate with Buffer/Later for scheduling
- [ ] Consider AI-powered copy generation

---

**Ready?** Run: `python scripts/batch_generate.py --config config/projects/2026-04-expedia.json`

Questions? Check README.md or ask Claude Code.

---

**Version:** 1.0  
**Status:** Ready to use  
**Last Updated:** 2026-04-18
