# Setup Instructions for Social Content Automation

## Initial Setup (Do Once)

### 1. Python Environment
```bash
cd social-content-automation
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create Config Folders
```bash
mkdir -p config/projects
mkdir -p outputs
```

### 3. Customize Branding
Edit `config/branding.yaml`:
- Update `primary_color`, `secondary_color` with your brand colors
- Replace `logo.png` in `assets/` with your logo
- Update social media handles in `social_handles` section
- Update CTA templates with your website link

### 4. Create First Project Config
```bash
cp templates/project_config_template.json config/projects/2026-05-[yourproject].json
# Edit with your project details
```

### 5. Run Initial Pipeline Test
```bash
python scripts/batch_generate.py --config config/projects/2026-05-[yourproject].json
```

---

## Tools & Integration List

### Required (Included)
- ✅ Python 3.8+
- ✅ Pillow (image processing)
- ✅ python-pptx (PowerPoint handling)
- ✅ PyYAML (config parsing)
- ✅ matplotlib (chart handling)

### Optional but Recommended
- ⚠️ **moviepy** — For automated TikTok/Reels video generation
  - Currently: Video scripts auto-generated (JSON format)
  - Future: Can animate videos programmatically
  - Installation: Already in requirements.txt

### For When You Move to New Repo

#### GitHub Integration
You'll want to set up these GitHub tools in the new repo:
1. **GitHub CLI (gh)** — For pushing updates and managing repo
   ```bash
   gh repo create social-content-automation --public
   gh repo clone social-content-automation
   ```
2. **GitHub Actions** (optional) — For automated CI/CD
   - Could auto-generate content on schedule
   - Or trigger on new project config upload

#### Claude Code Integration
When using Claude Code in the new repo:
1. **Create `.claude/settings.json`** to configure:
   ```json
   {
     "permissions": {
       "read": ["config/", "scripts/", "templates/"],
       "write": ["scripts/", "config/"],
       "execute": ["python"]
     },
     "environment": {
       "PYTHONPATH": "./scripts"
     }
   }
   ```

2. **Optional: Setup hooks in `.claude/settings.json`**:
   ```json
   {
     "hooks": {
       "before-commit": "python scripts/validate_configs.py"
     }
   }
   ```

#### MCP Servers (for future enhancement)
If you want to integrate with external APIs:

1. **Image Storage MCP** (e.g., AWS S3, Google Cloud Storage)
   - Would allow automatic upload of generated images to cloud
   - Configuration: Add to `.claude/mcp-servers.json`

2. **Social Media API MCP** (future integration)
   - LinkedIn API MCP — Auto-post carousels
   - Twitter API MCP — Auto-post threads
   - Instagram Business API MCP — Auto-upload

3. **Email/Notification MCP** (optional)
   - Send notification when content is ready
   - Daily digest of what to post

**Note:** MCP integration is optional — current system works standalone.

---

## Recommended Claude Code Skills to Set Up

When working in Claude Code on this project, these skills would be helpful:

1. **`simplify` skill** — Review generated code for efficiency
   - Run after adding new features
   - Command: `/simplify` in Claude Code

2. **`security-review` skill** — Check for security issues
   - Run before pushing to public repo
   - Command: `/security-review`

3. **`init` skill** — Create/update CLAUDE.md
   - Already done, but can refresh
   - Command: `/init`

4. **`update-config` skill** — Manage .claude settings
   - Useful for adding permissions as needed
   - Command: `/update-config`

---

## Installation Checklist

- [ ] Clone or download `social-content-automation` folder
- [ ] Create Python virtual environment
- [ ] Run `pip install -r requirements.txt`
- [ ] Create `config/projects/` folder
- [ ] Edit `config/branding.yaml` with your branding
- [ ] Replace `assets/logo.png` with your logo
- [ ] Copy `templates/project_config_template.json` to `config/projects/[project].json`
- [ ] Edit project config with your first project details
- [ ] Run `python scripts/batch_generate.py --config config/projects/[project].json`
- [ ] Check `outputs/[project]/` for generated content
- [ ] Review and edit generated copy
- [ ] Upload to LinkedIn, Instagram, Twitter, TikTok

---

## Future Repo Migration

When you create a new GitHub repo for this:

```bash
# Step 1: Create new repo on GitHub
gh repo create social-content-automation --public --description "Auto-generate social media content from portfolio projects"

# Step 2: Push this folder to new repo
cd social-content-automation
git init
git add .
git commit -m "Initial commit: Social content automation system"
git branch -M main
git remote add origin https://github.com/[username]/social-content-automation.git
git push -u origin main

# Step 3: Set up .claude/settings.json in new repo
# (See recommended Claude Code setup above)

# Step 4: Optionally set up GitHub Actions, MCP integrations, etc.
```

---

## Troubleshooting

### Error: "No module named 'PIL'"
```bash
pip install Pillow --upgrade
```

### Error: "YAML file not found"
```bash
# Make sure you're running from social-content-automation root
cd social-content-automation
python scripts/batch_generate.py --config config/projects/2026-05-test.json
```

### Config validation fails
Check `config/projects/[project].json` has all required fields:
- `project_name`
- `date`
- `website_link`
- `carousels` (list with at least 1 carousel)
- Each carousel needs: `title`, `insights`, `metrics`, `takeaway`

### Images aren't being generated
1. Check `outputs/[project]/linkedin/` exists
2. Verify carousel_generator.py ran without errors
3. Ensure config has valid carousel data

---

## Support

- **Error with scripts?** Check CLAUDE.md for architecture overview
- **Want to customize?** Edit config files in `config/`
- **Need new features?** See README.md "Customization" section

---

**Version:** 1.0  
**Last Updated:** 2026-04-18
