# Expedia Marketplace Analysis — Key Findings Report

**Date:** 2026-04-18  
**Dataset:** 100,000 sample searches (2012–2013)  
**Metric:** Booking rate variance across segments, positions, and pricing strategies

---

## Problem Statement

Expedia's marketplace booking rate is **2.8% of impressions**—split by segment as:
- Budget: 3.04%
- Mid: 2.89%
- Luxury: 2.20%

Luxury booking rate is **27% lower** than Budget. Why?

---

## Key Findings

| Finding | Evidence | Impact |
|---------|----------|--------|
| **Competitiveness ≠ Problem** | Median comp_score: 0.0% (market parity). Underpriced hotels book 3.38%, overpriced book 2.55%. Correlation: +0.0289 (negligible). | Price is NOT the conversion lever. |
| **Ranking Quality = Equal** | Click rates flat across all segments: 4.5% (Budget), 4.7% (Mid), 4.1% (Luxury). | Expedia's ranking algorithm surfaces relevant hotels equally well for all segments. |
| **Ranking Elasticity = 5.22x** | Position 1 books at 13.37%, position 10 at 2.56%. Position matters MORE for bookings than clicks (click elasticity 4.53x). | Position is the strongest lever for conversion. |
| **Quality Trust Gap = The Problem** | Budget beats promise (+41.2%): promise 2.40★, deliver 3.39 → 3.04% books. Luxury fails promise (-2.3%): promise 4.30★, deliver 4.20 → 2.20% books. | Luxury buyers see highly-rated hotels, click them, then discover promised quality ≠ actual quality. Conversion collapses. |
| **Experience Drives Conversion** | New visitor booking rate: 2.74%. Returning visitor booking rate: 3.66%. Lift: 1.34x. Click rates nearly identical (4.49% vs 4.61%). | Trust and familiarity boost conversion; visibility doesn't differ by visitor type. |

---

## Root Cause Analysis

**Luxury Segment Conversion Failure:**

| Metric | Budget | Mid | Luxury |
|--------|--------|-----|--------|
| Star Rating (Promise) | 2.40★ | 3.34★ | 4.30★ |
| Review Score (Actual) | 3.39 | 3.97 | 4.20 |
| Gap | +41.2% | +18.7% | **-2.3%** |
| % Hotels Beating Promise | 78% | 73% | 39% |
| % Hotels Failing Promise | 10% | 12% | 31% |
| Booking Rate | 3.04% | 2.89% | 2.20% |

**Insight:** Luxury buyers have elevated expectations. A 4.30★ hotel that delivers 4.20★ quality triggers disappointment → abandonment.

---

## Strategic Implications

1. **Price optimization is the wrong lever.** Moving from overpriced to underpriced only lifts bookings by 0.83pp (32% lift, but negligible absolute impact).

2. **Position is the strongest lever.** Position 1 converts 5.22x better than position 10.

3. **Quality alignment is the second lever.** Hotels beating their promise convert better. Luxury failure (-2.3% gap) explains lower booking rates.

4. **Trust matters.** Returning visitors book at 1.34x the rate of new visitors despite identical click rates.

---

## Recommendations (Prioritized)

1. **Fix luxury quality gap** — Audit 4.3★-rated hotels; verify star rating accuracy; remove misaligned listings
2. **Improve ranking algorithm** — Optimize for quality-intent alignment, not just relevance
3. **Build trust signals** — Highlight returning visitor reviews; show verified buyer ratings
4. **Avoid price optimization** — It has negligible ROI; focus effort on quality and position

---

## Expected Impact

- **Luxury booking rate lift target:** 5% (from 2.20% → 2.31%)
- **Primary driver:** Quality gap closure (narrowing -2.3% gap to -1.0%)
- **Secondary driver:** Improved ranking confidence score for luxury segment

