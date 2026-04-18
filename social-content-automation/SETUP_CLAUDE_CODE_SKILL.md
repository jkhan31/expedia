# Setting Up Social Copy Skill in Claude Code

**TL;DR:** Register this as a custom Claude Code skill to invoke with `/social-copy` command on your laptop.

---

## Quick Setup (When Using Claude Code on Laptop)

### Option 1: Add to `.claude/settings.json` (Recommended)

```json
{
  "skills": {
    "social-copy": {
      "description": "Generate 3 A/B social media copy variants with memory & refinement",
      "command": "python social-content-automation/scripts/social_copy_skill.py",
      "cwd": "/path/to/expedia",
      "args": "--project {project} --platform {platform} --save"
    }
  }
}
```

Then use in Claude Code:
```bash
/social-copy --project "Expedia Marketplace Analysis" --platform linkedin
```

### Option 2: Add Shell Alias (Quick & Dirty)

Add to your `~/.zshrc` or `~/.bashrc`:
```bash
alias social-copy='cd /path/to/expedia/social-content-automation && python scripts/social_copy_skill.py'
```

Then use:
```bash
social-copy --project "Expedia Marketplace Analysis" --platform linkedin --save
```

### Option 3: Create Claude Code Workflow Hook

Add to `.claude/settings.json`:
```json
{
  "hooks": {
    "on-open": "echo '📝 Social Copy Skill ready. Use: python scripts/social_copy_skill.py --help'"
  }
}
```

---

## What the Skill Does

✅ **Generates 3 A/B copy variants** per carousel per platform  
✅ **Remembers everything** (per-project memory files)  
✅ **Progressive refinement** (ask Claude to refine on the fly)  
✅ **No API key** needed  
✅ **Super fast** (instant generation)  

---

## Basic Usage Commands

```bash
# Generate LinkedIn variants for carousel 1
python scripts/social_copy_skill.py \
  --project "Expedia Marketplace Analysis" \
  --platform linkedin \
  --carousel 1 \
  --save

# Generate Instagram variants
python scripts/social_copy_skill.py \
  --project "Expedia Marketplace Analysis" \
  --platform instagram \
  --carousel 2 \
  --save

# Generate Twitter variants
python scripts/social_copy_skill.py \
  --project "Expedia Marketplace Analysis" \
  --platform twitter \
  --save

# View all previously generated copies (memory)
python scripts/social_copy_skill.py \
  --project "Expedia Marketplace Analysis" \
  --memory

# Refine previous variants (ask Claude after seeing output)
# Then in Claude Code conversation:
# > "The LinkedIn variants are good but Variant A needs to be punchier"
# Claude will regenerate with refinement applied
```

---

## Advanced: Progressive Workflow in Claude Code

1. **Generate initial variants:**
   ```bash
   python scripts/social_copy_skill.py --project "..." --platform linkedin --carousel 1
   ```

2. **Ask Claude for refinement** in the same session:
   > "Make Variant B more contrarian and add a hook"

3. **Claude refines** (you can implement this by asking me to call refine method)

4. **Generate next platform without losing previous:**
   ```bash
   python scripts/social_copy_skill.py --project "..." --platform instagram --carousel 1
   ```
   Memory auto-loads previous generation!

---

## Memory Files

Each project has its own memory file:
```
.social_copy_memory_[project-hash].json
```

Examples:
- `.social_copy_memory_a1b2c3d4.json` → Expedia Marketplace Analysis
- `.social_copy_memory_e5f6g7h8.json` → Next project

**Location:** Same directory as `scripts/` (social-content-automation root)

Check memory anytime:
```bash
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --memory
```

---

## Integration with Batch Automation

Full workflow:
```bash
# 1. Generate carousel images (batch automation)
python scripts/batch_generate.py --config config/projects/2026-04-expedia.json

# 2. Generate copy variants (skill, in Claude Code)
python scripts/social_copy_skill.py --project "Expedia..." --platform linkedin --save
python scripts/social_copy_skill.py --project "Expedia..." --platform instagram --save
python scripts/social_copy_skill.py --project "Expedia..." --platform twitter --save

# 3. Review outputs/ folder and post
```

---

## What Changed (Improved)

✅ **Fixed per-project memory** — Each project has own memory file  
✅ **Actual refinement logic** — Refinements are tracked and applied  
✅ **Better variants** — More distinct hooks, less repetitive  
✅ **Fixed Twitter copy** — Real data, no placeholders  
✅ **Error handling** — Corrupted JSON gracefully handled  
✅ **Memory tracking** — Refinement count per carousel  

---

## Future: Make it a Real Claude Code Skill

When you're ready to make this a full Claude Code skill:

1. Create `.claude/skills/social-copy-generator/`
2. Add `manifest.json`:
   ```json
   {
     "name": "social-copy",
     "description": "Generate 3 A/B social copy variants with memory",
     "version": "1.0",
     "command": "python scripts/social_copy_skill.py",
     "args": {
       "project": "string",
       "platform": "string",
       "carousel": "optional int",
       "save": "optional boolean",
       "memory": "optional boolean"
     }
   }
   ```
3. Register in `.claude/settings.json`
4. Use with `/social-copy` shorthand

---

## Notes

- Memory persists across sessions (auto-loads when you open the project)
- No API key needed (pure local generation)
- Skill works offline
- Safe to call repeatedly (won't duplicate in memory)

---

**Set this up next time you open with Claude on laptop! 🚀**
