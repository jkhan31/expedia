# LLM-Powered Copy Generation

Generate creative, unique social media copy using Claude API instead of templates.

## Quick Start

### 1. Set Your API Key

In Claude Code or terminal:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or in Claude Code settings (`.claude/settings.json`):
```json
{
  "environment": {
    "ANTHROPIC_API_KEY": "your-key"
  }
}
```

### 2. Run with LLM Copy

```bash
python scripts/batch_generate.py --config config/projects/2026-04-expedia.json --use-llm
```

### 3. Review Variants

Output: 3 copy variants per carousel per platform
```
outputs/Expedia Marketplace Analysis/
├── linkedin/
│   ├── carousel_1_variants.txt      ← 3 A/B options
│   ├── carousel_2_variants.txt
│   └── ...
├── instagram/
│   ├── carousel_1_variants.txt      ← 3 A/B options
│   └── ...
└── twitter/
    ├── carousel_1_variants.txt      ← 3 A/B options
    └── ...
```

Each file contains:
```
============================================================
VARIANT A (Option 1)
============================================================

[Creative copy variant 1]


============================================================
VARIANT B (Option 2)
============================================================

[Creative copy variant 2]


============================================================
VARIANT C (Option 3)
============================================================

[Creative copy variant 3]
```

### 4. Pick & Post

1. Open each `_variants.txt` file
2. Read all 3 options
3. Copy the one you like best
4. Paste into LinkedIn, Instagram, Twitter, etc.

---

## What LLM Generation Does

### LinkedIn (3 variants with different hooks)
- **Variant A:** Surprising statement hook
- **Variant B:** Contrarian question hook  
- **Variant C:** Data paradox hook

Each variant:
- 100-150 words
- Professional tone
- Punchy opening (no fluff)
- Natural metric integration
- Clear CTA

### Instagram (3 casual variants)
- **Variant A:** "Plot twist:" opening
- **Variant B:** Question opening
- **Variant C:** Surprising fact opening

Each variant:
- 80-120 words
- Conversational tone
- 2-4 emojis
- Mobile-optimized
- Hashtags included

### Twitter (3 thread structures)
- **Variant A:** Data paradox angle
- **Variant B:** Problem-solution angle
- **Variant C:** Misconception-correction angle

Each variant:
- 4-5 tweets per thread
- Punchy, no explanation
- Different narrative flow
- Link CTA at end

---

## How to Use in Claude Code

### In Claude Code Session:

1. **Set API key:**
   ```bash
   export ANTHROPIC_API_KEY="sk-..."
   ```

2. **Run automation with LLM flag:**
   ```bash
   cd social-content-automation
   python scripts/batch_generate.py --config config/projects/2026-04-expedia.json --use-llm
   ```

3. **Check outputs:**
   - All carousel images generated (same as before)
   - Plus: 3 copy variants per carousel per platform

4. **Review & choose:**
   - Read `outputs/[project]/[platform]/[carousel]_variants.txt`
   - Pick your favorite
   - Copy to social platform

---

## Cost & Performance

### Cost (per project with 4 carousels)
- 4 carousels × 3 platforms × 3 variants = 36 API calls
- ~$0.20-0.50 total cost (very cheap)
- You only pay when you use `--use-llm` flag

### Performance
- ~2-3 minutes to generate all variants (slower than templates)
- Run once, pick best, reuse across all platforms

---

## Compare: Template vs LLM

### Template-Based (Default)
```
python scripts/batch_generate.py --config config.json
```
✅ Fast (instant)
✅ Consistent
✅ Cheap (free)
❌ Predictable after seeing a few

### LLM-Based (Recommended)
```
python scripts/batch_generate.py --config config.json --use-llm
```
✅ Unique every time
✅ Creative hooks
✅ 3 A/B options to choose from
❌ Slower (2-3 min)
❌ Tiny cost (~$0.20)

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key"
# Verify it's set:
echo $ANTHROPIC_API_KEY
```

### Error: "Failed to reach API"
- Check internet connection
- Verify API key is valid (test at console.anthropic.com)
- Retry the command

### Copy quality not great
- Check that `key_insight`, `metrics`, `takeaway` in your project config are strong
- LLM quality depends on input quality
- Better carousel data = better generated copy

---

## Advanced: Customize Generation

Edit prompts in `scripts/llm_copy_generator.py`:

```python
def generate_linkedin_variants(self, carousel_data: Dict) -> List[str]:
    prompt = f"""
    [... customize this prompt ...]
    """
```

Want different hooks? Different tone? Edit the prompt and rerun.

---

## Environment Variables

**Required for LLM:**
- `ANTHROPIC_API_KEY` — Your Claude API key

**Optional:**
- Set in `.claude/settings.json` for Claude Code session
- Set in shell for terminal use
- Set in OS for global access

---

## FAQ

**Q: Which should I use, templates or LLM?**
A: LLM. The tiny cost is worth the unique, creative copy.

**Q: Can I use both?**
A: Not in one run, but yes you can:
- Run template version: `batch_generate.py --config config.json`
- Run LLM version: `batch_generate.py --config config.json --use-llm`
- Compare outputs, pick best from each

**Q: Do I need to pay for Claude Pro?**
A: No, you already have API access. Claude Pro is separate. API key is from console.anthropic.com.

**Q: Can I use Gemini or OpenRouter instead?**
A: Yes, but you'd need to modify `llm_copy_generator.py`. Currently built for Claude API only.

**Q: What if I want more than 3 variants?**
A: Edit `llm_copy_generator.py` and change `variants[:3]` to `variants[:5]` or whatever. Or run it twice and merge the outputs.

---

**Status:** Ready to use  
**Cost:** ~$0.20-0.50 per project  
**Time:** 2-3 minutes per project  
**Quality:** Much better than templates
