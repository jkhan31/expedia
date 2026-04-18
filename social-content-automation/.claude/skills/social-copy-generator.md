# Social Copy Generator Skill

Generate creative social media copy variants in Claude Code with memory and progressive refinement.

## Quick Commands

### Generate Copy Variants
```bash
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform linkedin --save
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform instagram --carousel 2 --save
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform twitter --carousel 1 --save
```

### Show Memory (Previous Generations)
```bash
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --memory
```

### Refine Previous Variants
Ask Claude to refine using the refinement prompt:
- "Generate copy for carousel 1 LinkedIn, then refine to be punchier"
- "Generate Twitter copy and make it more contrarian"

---

## Features

✅ **Progressive Calling**: Generate, review, refine in one session  
✅ **Memory**: Tracks all generated copies, refinements, history  
✅ **3 Variants**: A/B/C options for every carousel  
✅ **Platform-Specific**: Optimized hooks per platform  
✅ **Refinement**: Ask Claude to refine on the fly  
✅ **No API Key**: Uses Claude Code environment  

---

## Usage in Claude Code

### Step 1: Generate Initial Variants
In Claude Code terminal:
```bash
cd social-content-automation
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform linkedin --save
```

Output:
```
VARIANT A (Option 1)
────────────────────
Luxury hotels book 27% less often than budget hotels. But the reason isn't what you'd expect.

📊 Booking Rate Gap: 27% lower | Sample Size: 100k searches analyzed

Understanding the root cause unlocks a massive revenue opportunity


VARIANT B (Option 2)
────────────────────
What if luxury hotels fail not because of price, but because of expectations?

📊 Booking Rate Gap: 27% lower | Sample Size: 100k searches analyzed

Understanding the root cause unlocks a massive revenue opportunity


VARIANT C (Option 3)
────────────────────
You'd think The Luxury Hotel Problem. Wrong.

📊 Booking Rate Gap: 27% lower | Sample Size: 100k searches analyzed

Understanding the root cause unlocks a massive revenue opportunity
```

### Step 2: Review & Pick
- Read all 3 variants
- Pick your favorite
- Copy to social platform

### Step 3: If You Want Refinement
Ask me in Claude Code:
> "The LinkedIn variants are good but Variant A could be punchier. Refine it to be more surprising."

I'll regenerate or refine based on your feedback.

### Step 4: Generate for Other Platforms
```bash
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform instagram --carousel 1 --save
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --platform twitter --carousel 1 --save
```

---

## Memory System

The skill remembers:
- All generated copies (never regenerate the same unless refined)
- Refinement history (tracks what you asked for)
- Timestamps and metadata
- Your selections

View memory anytime:
```bash
python scripts/social_copy_skill.py --project "Expedia Marketplace Analysis" --memory
```

Output:
```
MEMORY: Previously Generated Copies

✓ The Luxury Hotel Problem (linkedin)
  Generated: 2026-04-18T15:32:00.000000
  Variants: 3

✓ The Luxury Hotel Problem (instagram)
  Generated: 2026-04-18T15:33:45.000000
  Variants: 3
```

---

## Progressive Refinement Example

```
Session 1:
> python social_copy_skill.py --project "Expedia..." --platform linkedin --save
[See 3 variants]
> "I like Variant B but make it more data-heavy"

Session 2 (same day, different task):
> python social_copy_skill.py --project "Expedia..." --memory
[Shows all previous work]
> "Let's do Instagram now, carousel 2"
```

Memory persists across sessions!

---

## Platform-Specific Output

### LinkedIn (3 variants)
- **A:** Direct statement hook
- **B:** Question hook
- **C:** Contrarian hook
- Each: 100-150 words, professional tone

### Instagram (3 variants)
- **A:** "Plot twist:" opening
- **B:** Question opening
- **C:** Surprising fact opening
- Each: 80-120 words, casual tone, emojis

### Twitter (3 variants)
- **A:** Data paradox thread
- **B:** Problem-solution thread
- **C:** Misconception thread
- Each: 4-5 tweets, punchy

---

## Integration with Batch Automation

The skill works alongside your batch automation:

```
Batch Automation (images):
  carousel_generator.py → generates slide images
  format_converter.py → optimizes for each platform

+ Social Copy Skill (copy):
  social_copy_skill.py → generates 3 copy variants per platform
```

Together: **Complete social content pipeline** (images + copy)

---

## Tips

- **First time?** Start with one carousel, one platform
- **Fast workflow?** Generate all 3 platforms in 1 minute
- **Need refinement?** Ask me to tweak mid-session
- **Save everything?** Use `--save` flag to write to files
- **Reuse?** Use `--memory` to see what's already generated

---

## Files Created

- `.social_copy_memory.json` — Persistent memory file (auto-created)
- `outputs/[project]/[platform]/[carousel]_variants.txt` — Saved variants (with `--save`)

---

**No API key. No billing. Just Claude Code + skill.**
