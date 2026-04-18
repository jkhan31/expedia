# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 5. Collaborative Learning (This Project)

**Don't execute analyses and hand off results. Teach the methodology.**

- Before running an analysis: explain the hypothesis, data needed, and how to interpret results
- Walk through code together; ask the user to implement parts when meaningful
- After analysis: interpret results collaboratively, not just show what they mean
- Create notebooks/intermediate outputs the user can inspect and understand
- **Pause frequently:** "Does that make sense so far?" "Do you see why we did that?"
- Have user summarize key insights back in their own words to validate understanding
- Don't move to next analysis until current one is understood

---

## 6. PM Lens (This Project)

**Apply critical OTA product manager thinking throughout.**

Before accepting any analysis insight or recommendation, question it:

1. **So what?** — If this pattern is true, what decision does it actually change?
2. **Causation vs correlation** — Are we confusing correlation with proof?
3. **What's the constraint we're ignoring?** — Why isn't this already optimized if it's so obvious?
4. **Customer impact vs hotel impact** — Are we optimizing the right side?
5. **Is the data representative?** — Sample bias? Time period bias? Does this hold broadly?
6. **How would we measure success?** — Can we A/B test it?
7. **What's the unintended consequence?** — Gaming risk? Breaks another metric?

---

## 7. Token Efficiency (Large Files)

**Never directly read train.csv or test.csv. Use Python only.**

- `sample.csv`: Safe to read directly with Read tool (small, under 1000 rows)
- `train.csv` / `test.csv`: Use Python scripts to examine and process them
- Report findings from Python output, never from direct file reads
- Prevents token bloat from loading massive datasets

---

## 8. Hypothesis Framing (Recommendations)

**For A/B test ideas and strategic questions: include expected outcomes, frame as hypothesis-test-learn.**

- **A/B tests:** "If [hypothesis] is correct, we'd expect [outcome]. Here's how we'd measure it and what success looks like."
- **Strategic questions:** "If the answer is [scenario], it would mean [implication]. Here's what we'd need to validate."
- Always label as: "hypothesis," "expected," "would suggest," "might indicate"
- Never claim causation—only correlation and implications for next steps
- Make clear: this is one interpretation; the data doesn't prove it

---

## 9. Worktree Setup (This Project)

**All analysis work happens in `.worktrees/analysis-build/`, not on main branch.**

- Main branch stays clean and untouched
- Analysis work is isolated in worktree
- If something breaks, we can delete worktree and start over
- Before implementation: user and Claude Code understand worktree location and purpose
- Easy to cleanup: `git worktree remove .worktrees/analysis-build`

---

## 10. Analysis & Data Guidelines (This Project)

**Data-driven analysis WITH causal measurement (outcome data available!).**

**DISCOVERY:** Dataset includes click_bool, booking_bool, and gross_bookings_usd. This allows direct measurement of what drives conversions, not just correlation.

**Key analyses (now with outcome data):**
- Funnel analysis: Impression → Click → Booking rates
- Ranking impact: Direct measurement of position effect on clicks/bookings
- Quality impact: Does quality actually drive conversions?
- Price impact: Elasticity of demand vs competitors
- User behavior: Do different segments convert differently?

**Framing changes:**
- OLD: "Data shows X, which suggests Y, but we'd need outcome data to prove Z"
- NEW: "Data shows position 1 gets X% booking rate vs position 2 gets Y% — here's the impact"

**Recommendations are now:**
- Data-backed (proven by conversion data, not hypothetical)
- Quantified (specific impact numbers)
- Actionable (we know what levers matter most)

**Still maintain:**
- Understanding checkpoints after each analysis
- Collaborative learning (explain methodology, not just results)
- Python code readable and documented
- Professional-grade visualizations
- Charts saved as PNG files for deck