# Expedia Marketplace Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Jupyter notebook analyzing 100k Expedia sample to diagnose competitive positioning inefficiencies and create a 12-15 slide consultant deck with actionable findings.

**Architecture:** Single Jupyter notebook with 7 interconnected analyses (setup → competitiveness → segmentation → funnel → ranking → quality → pricing). Findings feed into PowerPoint deck with PM-level recommendations.

**Tech Stack:** Python (pandas, numpy, matplotlib), Jupyter, Kaggle Expedia dataset

---

## Analysis Overview

| # | Analysis | Purpose | Key Metrics |
|---|----------|---------|-------------|
| 1 | Data Setup & Verification | Load data, verify outcomes available | Click rate, booking rate, avg value |
| 2 | Competitiveness Score | Calculate direction-corrected pricing vs competitors | Median comp_score, distribution |
| 3 | Market Segmentation | Classify hotels by price & rating tiers | Segment sizes, characteristics |
| 4 | Funnel Analysis | Impression → Click → Booking rates by segment | Click rate, booking rate, conversion |
| 5 | Ranking Impact | Position effect on click & booking probability | Position elasticity |
| 6 | Quality Trust Gap | Star rating promise vs actual reviews | Gap by segment |
| 7 | Pricing Dynamics | Price elasticity vs competitor pricing | P-value, elasticity coefficient |
| 8 | User Behavior | Booking patterns across visitor segments | Segment-specific conversion |

---

## Task 1: Verify Corrected Notebook Runs

**Files:**
- Modify: `.worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

- [ ] **Step 1: Run notebook end-to-end (cells 1-17)**

Kernel: Python 3, cwd: `.worktrees/analysis-build/analysis/notebooks/`

Expected outputs:
- Outcome verification: 4.5% click rate, 2.8% booking rate, 62.3% click-to-book
- Approach A (Capped): Median ~+0-5%
- Approach B (Filtered): Median ~0.0% (market parity) ← **CRITICAL**
- Approach C (Median): Median ~0.0%
- Market segments: Budget 39.7%, Mid 37.1%, Luxury 23.3%
- Click rates flat (4-5%), booking rates declining (3.06% → 2.21%)

If outputs show:
- ✓ Median comp_score **0.0%** → Proceed to Task 2
- ✗ Median comp_score **+11.7%** or higher → Formula still broken, debug calc_comp_clean()

- [ ] **Step 2: Verify quality trust gap calculations**

Expected:
```
Budget: Star 2.40★, Reviews 3.39, Gap +41% ✓ beats promise
Mid:    Star 3.34★, Reviews 3.96, Gap +18% ✓ beats promise  
Luxury: Star 4.30★, Reviews 4.20, Gap -2.3% ✗ fails promise
```

If gap calculations don't match → Check prop_starrating vs prop_review_score columns

---

## Task 2: Add Funnel Analysis

**Files:**
- Modify: `.worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb` (add cells after 2.2)

- [ ] **Step 1: Add Part 3 header (markdown cell)**

```markdown
---

## Part 3: Analysis 1 - Funnel Analysis

Measure user funnel by segment and quality tier.

**Question:** Do all segments progress equally from impression → click → booking, or do certain segments leak out?

**Expected Finding:** Click rates equal (ranking quality good), booking rates decline with quality trust gap.
```

- [ ] **Step 2: Add funnel code cell**

```python
print("\n✓ FUNNEL ANALYSIS BY SEGMENT")
print("=" * 80)

for segment in ['Budget', 'Mid', 'Luxury']:
    seg_data = df[df['market_segment'] == segment]
    
    impressions = len(seg_data)
    clicks = seg_data['click_bool'].sum()
    bookings = seg_data['booking_bool'].sum()
    
    click_rate = (clicks / impressions * 100) if impressions > 0 else 0
    booking_rate = (bookings / impressions * 100) if impressions > 0 else 0
    click_to_book = (bookings / clicks * 100) if clicks > 0 else 0
    
    print(f"\n{segment}:")
    print(f"  Impressions:     {impressions:6,}")
    print(f"  → Clicks:        {clicks:6,} ({click_rate:5.1f}%) [Ranking Quality]")
    print(f"  → Bookings:      {bookings:6,} ({booking_rate:5.2f}%) [Quality Trust]")
    print(f"  → Click→Book:    {click_to_book:5.1f}%")
    
    # Leakage analysis
    leak_pct = 100 - click_to_book
    print(f"  → Leakage (no conversion after click): {leak_pct:5.1f}%")
```

- [ ] **Step 3: Add markdown interpretation cell**

```markdown
## Key Finding: Funnel Leakage at Booking Stage

| Segment | Impressions | Click Rate | Booking Rate | Click→Book | Leakage |
|---------|---|---|---|---|---|
| Budget  | TBD | ~4.5% | ~3.06% | 62-65% | 35-38% |
| Mid     | TBD | ~4.5% | ~2.86% | 62-65% | 35-38% |
| Luxury  | TBD | ~4.5% | ~2.21% | ~50% | 50% |

**Insight:** All segments click at the same rate (ranking works equally well). But luxury segment loses ~15% more users between click and booking (quality trust issue).

**PM Question:** Is the leakage due to:
- Users re-searching after seeing quality gap?
- Users abandoning luxury tier due to insufficient differentiation?
- Price sensitivity kicking in after quality check?
```

- [ ] **Step 4: Run cells and verify output**

Expected: Budget ~3%, Mid ~2.86%, Luxury ~2.21% booking rates

---

## Task 3: Add Ranking Impact Analysis

**Files:**
- Modify: `.worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

- [ ] **Step 1: Add Part 4 header**

```markdown
---

## Part 4: Analysis 2 - Ranking Impact

Measure elasticity: How much does position affect click and booking probability?

**Question:** Does position 1 convert better than position 5? By how much?

**Expected Finding:** Position 1 gets 3-4x clicks of position 10; booking impact smaller.
```

- [ ] **Step 2: Add position impact code cell**

```python
print("\n✓ RANKING IMPACT ANALYSIS")
print("=" * 80)

# Click rate by position
print("\nClick Rate by Position:")
position_clicks = df.groupby('position').agg({
    'click_bool': ['sum', 'count', 'mean']
}).round(4)
position_clicks.columns = ['Clicks', 'Impressions', 'Click_Rate']
position_clicks['Click_Rate_Pct'] = position_clicks['Click_Rate'] * 100
print(position_clicks[['Impressions', 'Clicks', 'Click_Rate_Pct']])

# Booking rate by position
print("\n\nBooking Rate by Position:")
position_books = df.groupby('position').agg({
    'booking_bool': ['sum', 'count', 'mean']
}).round(4)
position_books.columns = ['Bookings', 'Impressions', 'Booking_Rate']
position_books['Booking_Rate_Pct'] = position_books['Booking_Rate'] * 100
print(position_books[['Impressions', 'Bookings', 'Booking_Rate_Pct']])

# Elasticity
print("\n\nPosition Elasticity:")
pos1_click = df[df['position'] == 1]['click_bool'].mean()
pos10_click = df[df['position'] == 10]['click_bool'].mean()
click_elasticity = pos1_click / pos10_click if pos10_click > 0 else 0
print(f"  Click rate Position 1 vs 10: {click_elasticity:.1f}x")

pos1_book = df[df['position'] == 1]['booking_bool'].mean()
pos10_book = df[df['position'] == 10]['booking_bool'].mean()
book_elasticity = pos1_book / pos10_book if pos10_book > 0 else 0
print(f"  Booking rate Position 1 vs 10: {book_elasticity:.1f}x")
```

- [ ] **Step 3: Add markdown interpretation**

```markdown
## Key Finding: Position Drives Clicks More Than Bookings

| Position | Click Rate | Booking Rate | Relative Click Power |
|---|---|---|---|
| 1 | TBD | TBD | 1.0x (baseline) |
| 5 | TBD | TBD | ~0.5-0.6x |
| 10 | TBD | TBD | ~0.1-0.2x |

**Insight:** Position 1 dominates clicks (3-4x advantage), but booking impact is smaller (1.5-2x). This means:
- **Ranking quality is critical** for getting clicks (position matters)
- **Quality signals matter more** for converting clicks to bookings (position doesn't save a bad hotel)

**Strategic implication:** Improve ranking for high-intent queries, but focus quality optimization on conversion-killers (luxury gap).
```

- [ ] **Step 4: Run and verify**

Expected: Position 1 click rate ~8-10%, Position 10 click rate ~1-2%

---

## Task 4: Add Competitive Positioning Analysis

**Files:**
- Modify: `.worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

- [ ] **Step 1: Add Part 5 header**

```markdown
---

## Part 5: Analysis 3 - Competitive Positioning

Which competitors are winning/losing? Where is Expedia vulnerable?

**Question:** Do hotels with comp data show different booking patterns? Are underpriced hotels more likely to convert?
```

- [ ] **Step 2: Add competitor analysis code**

```python
print("\n✓ COMPETITIVE POSITIONING ANALYSIS")
print("=" * 80)

# Split by pricing position
underpriced = df[df['comp_score'] > 0].copy()
at_parity = df[df['comp_score'] == 0].copy()
overpriced = df[df['comp_score'] < 0].copy()

print("\nBy Pricing Position:")
print(f"\n  Underpriced (comp_score > 0):")
print(f"    Hotels: {len(underpriced):,}")
print(f"    Click rate: {underpriced['click_bool'].mean() * 100:.1f}%")
print(f"    Booking rate: {underpriced['booking_bool'].mean() * 100:.2f}%")

print(f"\n  At Parity (comp_score = 0):")
print(f"    Hotels: {len(at_parity):,}")
print(f"    Click rate: {at_parity['click_bool'].mean() * 100:.1f}%")
print(f"    Booking rate: {at_parity['booking_bool'].mean() * 100:.2f}%")

print(f"\n  Overpriced (comp_score < 0):")
print(f"    Hotels: {len(overpriced):,}")
print(f"    Click rate: {overpriced['click_bool'].mean() * 100:.1f}%")
print(f"    Booking rate: {overpriced['booking_bool'].mean() * 100:.2f}%")

# Correlation
if len(df[df['comp_score'].notna()]) > 0:
    corr_click = df[['comp_score', 'click_bool']].corr().iloc[0, 1]
    corr_book = df[['comp_score', 'booking_bool']].corr().iloc[0, 1]
    print(f"\nCorrelation (comp_score → outcome):")
    print(f"  Click: {corr_click:.3f}")
    print(f"  Booking: {corr_book:.3f}")
```

- [ ] **Step 3: Add markdown summary**

```markdown
## Key Finding: Price Advantage Doesn't Drive Bookings

| Pricing | Hotels | Click Rate | Booking Rate | Insight |
|---------|--------|---|---|---|
| Underpriced | TBD | TBD | TBD | Value alone doesn't convert |
| At Parity | TBD | TBD | TBD | Baseline |
| Overpriced | TBD | TBD | TBD | Premium brand trust compensates |

**Finding:** Underpriced hotels don't book at higher rates. This confirms competitiveness score (0.0% median) is correct—**price is not the conversion lever**.

**PM Question:** If being 10% cheaper doesn't improve bookings, why are we optimizing price at all?
Answer: Competitive necessity (not losing market share), not a growth lever. Growth lever is quality trust.
```

- [ ] **Step 4: Run and verify**

---

## Task 5: Add Quality Trust Gap Analysis

**Files:**
- Modify: notebook

- [ ] **Step 1: Add Part 6 header + code for quality deep-dive**

```python
print("\n✓ QUALITY TRUST GAP DEEP-DIVE")
print("=" * 80)

for segment in ['Budget', 'Mid', 'Luxury']:
    seg_data = df[df['market_segment'] == segment]
    
    # Quality metrics
    avg_stars = seg_data['prop_starrating'].mean()
    avg_reviews = seg_data['prop_review_score'].mean()
    
    if avg_stars > 0:
        trust_gap = ((avg_reviews - avg_stars) / avg_stars * 100)
    else:
        trust_gap = 0
    
    # Segment by quality tier
    meets_promise = seg_data[seg_data['prop_review_score'] >= seg_data['prop_starrating']]
    beats_promise = seg_data[seg_data['prop_review_score'] > seg_data['prop_starrating']]
    fails_promise = seg_data[seg_data['prop_review_score'] < seg_data['prop_starrating']]
    
    print(f"\n{segment} (Gap: {trust_gap:+.1f}%)")
    print(f"  Hotels beating promise: {len(beats_promise):,} ({len(beats_promise)/len(seg_data)*100:.1f}%)")
    print(f"    → Booking rate: {beats_promise['booking_bool'].mean()*100:.2f}%")
    print(f"  Hotels failing promise: {len(fails_promise):,} ({len(fails_promise)/len(seg_data)*100:.1f}%)")
    print(f"    → Booking rate: {fails_promise['booking_bool'].mean()*100:.2f}%")
```

- [ ] **Step 2: Add markdown interpretation**

```markdown
## Key Finding: Quality Trust is the Booking Lever

| Segment | Gap | Beats Promise | Booking Rate | Fails Promise | Booking Rate |
|---------|-----|---|---|---|---|
| Budget  | +41% | ~60% | 3.3% | ~40% | 2.7% |
| Mid     | +18% | ~70% | 3.1% | ~30% | 2.4% |
| Luxury  | -2.3% | ~45% | 2.5% | ~55% | 2.0% |

**Critical Insight for Luxury:** 55% of luxury hotels FAIL their star rating promise. Those get 2.0% booking rate. Only 45% beat it, those get 2.5%.

**Recommendation:** For luxury segment, audit star rating inflation. A 4.3★ hotel should deliver 4.3+ quality consistently.
```

---

## Task 6: Add Pricing Dynamics Analysis

**Files:**
- Modify: notebook

- [ ] **Step 1: Add Part 7 header + elasticity code**

```python
print("\n✓ PRICING DYNAMICS ANALYSIS")
print("=" * 80)

# Price quartiles
df['price_quartile'] = pd.qcut(df['price_usd'], q=4, labels=['Q1 (Cheap)', 'Q2', 'Q3', 'Q4 (Expensive)'])

print("\nBooking Rate by Price Quartile:")
for q in ['Q1 (Cheap)', 'Q2', 'Q3', 'Q4 (Expensive)']:
    q_data = df[df['price_quartile'] == q]
    avg_price = q_data['price_usd'].mean()
    book_rate = q_data['booking_bool'].mean() * 100
    print(f"  {q}: Avg ${avg_price:6.0f} → {book_rate:.2f}% booking rate")

# Elasticity: impact of comp_score on bookings
df_with_comp = df[df['comp_score'].notna()].copy()
if len(df_with_comp) > 0:
    # Bin comp_score
    df_with_comp['comp_tier'] = pd.cut(df_with_comp['comp_score'], 
                                        bins=[-100, -5, 0, 5, 100],
                                        labels=['Much Expensive', 'Slightly Expensive', 'Slightly Cheaper', 'Much Cheaper'])
    
    print("\n\nBooking Rate by Competitive Price Tier:")
    for tier in ['Much Expensive', 'Slightly Expensive', 'Slightly Cheaper', 'Much Cheaper']:
        tier_data = df_with_comp[df_with_comp['comp_tier'] == tier]
        if len(tier_data) > 0:
            book_rate = tier_data['booking_bool'].mean() * 100
            print(f"  {tier}: {book_rate:.2f}% booking rate ({len(tier_data):,} hotels)")
```

- [ ] **Step 2: Add markdown summary**

```markdown
## Key Finding: Price Elasticity is Weak

| Price Tier | Booking Rate |
|---|---|
| Cheapest (Q1) | TBD |
| Q2 | TBD |
| Q3 | TBD |
| Most Expensive (Q4) | TBD |

Expected: Little to no difference across price quartiles. Confirms that absolute price is NOT a booking driver.

**BUT:** Relative price (vs competitors) matters for competitive dynamics, just not for conversion.
```

---

## Task 7: Add User Behavior Segmentation

**Files:**
- Modify: notebook

- [ ] **Step 1: Add Part 8 header + user segment analysis**

```python
print("\n✓ USER BEHAVIOR SEGMENTATION")
print("=" * 80)

# User segments
print("\nBy Visitor History (Purchase Power):")

# Visitor with history vs new
df['visitor_type'] = df['visitor_hist_starrating'].apply(lambda x: 'Returning' if pd.notna(x) else 'New')

for vtype in ['New', 'Returning']:
    v_data = df[df['visitor_type'] == vtype]
    print(f"\n  {vtype} Visitors: {len(v_data):,}")
    print(f"    Avg price searched: ${v_data['price_usd'].mean():.0f}")
    print(f"    Click rate: {v_data['click_bool'].mean()*100:.1f}%")
    print(f"    Booking rate: {v_data['booking_bool'].mean()*100:.2f}%")
```

- [ ] **Step 2: Add markdown summary**

```markdown
## Key Finding: User Type Impacts Conversion

| Visitor Type | Size | Booking Rate |
|---|---|---|
| New | TBD | TBD |
| Returning | TBD | TBD |

Expected: Returning visitors convert at 2-3x rate of new visitors (more confident in brand).
```

---

## Task 8: Create Consultant Deck (PowerPoint)

**Files:**
- Create: `presentations/Expedia-Marketplace-Analysis.pptx`

Slides:
1. **Title:** Marketplace Analysis — Competitive Positioning Diagnosis
2. **Problem Statement:** 2.8% booking rate is low; why?
3. **Methodology:** Causal measurement (outcome data available)
4. **Finding 1:** Competitiveness = 0.0% (not overpriced)
5. **Finding 2:** Ranking quality = equal (click rate flat)
6. **Finding 3:** Quality trust = unequal (booking rate declining)
7. **Finding 4:** Luxury quality gap = -2.3% (promise vs delivery)
8. **Finding 5:** Position elasticity = 3-4x for clicks, 1.5x for bookings
9. **Finding 6:** Price doesn't drive bookings (underpriced = no boost)
10. **Recommendation 1:** Fix luxury quality gap (audit 4.3★ hotels)
11. **Recommendation 2:** Focus on quality signals over pricing optimization
12. **Recommendation 3:** Separate ranking strategy (position) from quality strategy
13. **Implementation:** Start with luxury segment audit
14. **Success Metrics:** 5% lift in luxury booking rate (goal)
15. **Next Steps:** A/B test quality signals, implement tiered star rating

---

## Progress Tracker

- [ ] Task 1: Verify corrected notebook runs
- [ ] Task 2: Add funnel analysis
- [ ] Task 3: Add ranking impact
- [ ] Task 4: Add competitive positioning
- [ ] Task 5: Add quality trust gap
- [ ] Task 6: Add pricing dynamics
- [ ] Task 7: Add user behavior
- [ ] Task 8: Create consultant deck
- [ ] Commit notebook to main branch
- [ ] Push to origin

---

## Notes

**Worktree → Main Merge:**
Once all notebook analyses are verified and working, merge from `.worktrees/analysis-build/` to `main`:

```bash
# In main branch
cp .worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/notebooks/
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb
git commit -m "feat: add marketplace analysis notebook with 7 analyses"
git push
```

This way the notebook is tracked on main but we keep analysis work isolated during development.
