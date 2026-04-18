# Design Spec: Travel Marketplace Analysis Deck

**Date:** 2026-04-18  
**Project:** Diagnosing and Improving a Travel Booking System  
**Outcome:** 12–15 slide consultant-style deck with supporting analysis  
**Author:** Claude

---

## 1. Overview

This project analyzes hotel search/ranking data to diagnose inefficiencies in a competitive marketplace ranking system. The deck is structured around a **system diagnosis first** narrative, revealing how ranking logic breaks down, what it means for partners and market structure, and what should change.

**Core constraint UPDATED:** Dataset INCLUDES click/booking outcomes! Analysis can now measure causal impact on conversions, not just correlational patterns. This significantly strengthens recommendations.

---

## 2. Analyses to Conduct

### 2.0 Funnel Analysis (NEW - Made possible by outcome data)
**Purpose:** Understand where users drop off: Impression → Click → Booking

**Outputs:**
- Funnel chart: % of impressions that click, % of clicks that book
- Click rate by position
- Booking rate by position
- Post-click conversion rate
- Revenue metrics

**Insight sought:** Where is the biggest friction in the funnel?

---

### 2.1 Competitive Positioning Analysis
**Purpose:** Understand how hotels are priced relative to 8 competitors within the same search.

**Outputs:**
- Price competitiveness score (hotel price - mean competitor price)
- Distribution of over/underpricing by segment
- Scatter plot: price vs competitor average

**Insight sought:** Are hotels in efficient competitive equilibrium, or trapped in bad positions?

---

### 2.1a Ranking Impact on Conversions (NEW - Direct Measurement)
**Purpose:** Measure how ranking position directly affects clicks and bookings.

**Outputs:**
- Click rate by position (position 1 vs 2 vs 3, etc.)
- Booking rate by position
- Revenue per position
- Chart: position vs conversion funnel

**Insight sought:** How much does being first really matter? Quantified impact.

---

### 2.2 Ranking Bias & Quality Correlation
**Purpose:** Understand: Do high-quality hotels rank first?

**Outputs:**
- Correlation: position vs (price, rating, review_score, brand)
- Quality metrics by position
- Booking rate by quality tier

**Insight sought:** Is ranking logic quality-aware? And does quality drive conversions?

---

### 2.3a Price Competitiveness Impact (NEW - Direct Measurement)
**Purpose:** Does being under/overpriced relative to competitors affect booking?

**Outputs:**
- Click rate by competitiveness score (underpriced vs fair vs overpriced)
- Booking rate by competitiveness score
- Revenue impact of pricing strategy
- Chart: competitiveness vs conversion

**Insight sought:** Should hotels lower prices to compete? What's the conversion elasticity?

---

### 2.3 Market Segmentation
**Purpose:** Identify distinct market clusters and competitive dynamics.

**Outputs:**
- Segment definition by: price range, star rating, review score, location
- Hotel distribution across segments
- Market intensity (avg competitors per search per segment)

**Insight sought:** Do markets stratify cleanly (luxury/mid/budget), or is segmentation muddled?

---

### 2.4 Pricing Dynamics
**Purpose:** Analyze price competitiveness patterns and over/underpricing by segment.

**Outputs:**
- Over/underpriced hotels (by segment)
- Consistency: which hotels persistently under/overprice?
- Price dispersion by search (competition intensity)

**Insight sought:** Where is pricing broken? Which hotels are trapped in bad positions?

---

### 2.5 User Behavior Segmentation
**Purpose:** Understand traveler patterns by user type and booking context.

**Outputs:**
- Returning vs new users (proxy: non-NULL visitor history)
- Booking window distribution (urgency proxy)
- Group composition (solo, couple, family)
- Length of stay patterns

**Insight sought:** How does user type correlate with market segments? Does urgency affect competitiveness?

---

### 2.6 Data Structure & Market Overview
**Purpose:** Understand what the dataset represents and overall market composition.

**Outputs:**
- Timeline (dates covered)
- Search volume by destination
- Hotel distribution (unique properties, repeat rate)
- Temporal patterns (seasonal, day-of-week)

**Insight sought:** Is this a representative sample? What biases exist in the data?

---

## 3. Deck Architecture (12–15 slides)

### Section 1: Funnel & Conversion Impact (Slides 1–6)

**Slide 1: Title + Executive Summary**
- One sentence: "How marketplace mechanics drive (or block) conversions"
- Subtitle: "A data-driven diagnosis of friction in the hotel booking funnel"

**Slide 2: System Overview**
- What is the dataset? (10k hotels, 3,542 searches, 100k+ rows)
- The funnel: Impression → Click → Booking
- Why this matters: Each stage has different friction

**Slide 3: Funnel Analysis**
- Chart: Waterfall showing impression → click → booking rates
- Finding: % of impressions that click? % of clicks that book?
- Data: Total revenue impact of conversions

**Slide 4: Ranking Impact on Conversions**
- Chart: Click rate by position, Booking rate by position
- Finding: How much does position #1 matter? (quantified)
- Data: Position 1 click rate vs position 2, 3, etc.

**Slide 5: Quality Impact on Conversions**
- Chart: Click/booking rate by star rating and review score
- Finding: Do high-quality hotels actually convert more?
- Data: Quality signals vs actual booking behavior

**Slide 6: Price Competitiveness Impact**
- Chart: Click/booking rate by price competitiveness (underpriced vs overpriced)
- Finding: Booking elasticity — does cheaper = more bookings?
- Data: Revenue impact of pricing strategy

---

### Section 2: Market Structure & Segmentation (Slides 7–9)

**Slide 7: Market Segmentation**
- Chart: Price vs rating, with market segments overlaid (luxury, mid, budget)
- Finding: Clear market stratification?
- Hotel distribution across segments

**Slide 8: Pricing Dynamics by Segment**
- Chart: Distribution of price competitiveness by segment
- Finding: Over/underpriced hotels and conversion rates
- Insight: Which segments are most price-sensitive?

**Slide 9: User Behavior & Urgency**
- Chart: Booking window, group composition, length of stay
- Finding: Does user urgency affect conversion rates?
- Insight: Last-minute bookers vs planners—different behavior?

---

### Section 3: Data-Backed Recommendations (Slides 10–15)

**Slide 10: Key Findings Summary**
- 3–4 core insights with quantified impact
  - E.g., "Position 1 has X% booking rate vs position 2 has Y%"
  - E.g., "Quality hotels underpriced convert at Z% rate"
- Clear framing: These are facts, not hypotheses

**Slide 11: Ranking Optimization Opportunities**
- Finding: Position impact on conversions (backed by data)
- Recommendation: Test ranking logic changes to improve conversion
- Expected impact: Estimated lift based on position/quality correlation
- **Rationale:** We measured the effect, so we know what matters

**Slide 12: Pricing Strategy Recommendations**
- Finding: Price competitiveness impact on booking rate (backed by data)
- Recommendation: Partner pricing guidance based on segment elasticity
- Expected impact: Higher conversion for competitively-priced hotels
- **Rationale:** Data shows which hotels are trapped in bad positions

**Slide 13: Partner Enablement Tools**
- Competitiveness dashboard: Show price vs competitors + conversion impact
- Conversion benchmarks: "Your booking rate is X%, segment average is Y%"
- Positioning transparency: "Here's why you're ranked there + how to improve"
- **Rationale:** Armed with data, partners can optimize themselves

**Slide 14: Segmentation & Personalization**
- Finding: Different user segments (urgency, group size) convert differently
- Recommendation: Show different market segments to different users
- Expected impact: Improved relevance + conversion
- **Rationale:** Data shows which segments matter most

**Slide 15: Closing**
- What we measured: Direct impact of ranking, quality, price, positioning on conversions
- What changed: From "ranking might matter" to "ranking DOES matter, by X%"
- Next steps: Implement top-impact changes, measure results, iterate
- Connection to Partner Excellence: Data-driven decisions + partner transparency = better outcomes

---

## 4. Data Transformations Required

### 4.1 Ranking Position Inference
```
Within each search (srch_id), assign position 1, 2, 3... by row order
This assumes row order = ranking order in the original dataset
```

### 4.2 Price Competitiveness Score
```
For each row:
  - Extract all comp#_rate values for that search
  - Calculate mean competitor price (excluding NULLs)
  - Competitiveness = price_usd - mean(comp#_rate)
  - Positive = overpriced, Negative = underpriced
```

### 4.3 Market Segment Assignment
```
Segment hotels by price range + star rating:
  - Luxury: 4–5 stars, price > 75th percentile
  - Mid: 3–4 stars, price in 25–75th percentile
  - Budget: 2–3 stars, price < 25th percentile
  - (Exact thresholds to be refined during analysis)
```

### 4.4 User Type Classification
```
Returning user: visitor_hist_starrating IS NOT NULL
New user: visitor_hist_starrating IS NULL
```

---

## 5. Visualizations (Summary)

| Analysis | Chart Type | Key Variables |
|----------|-----------|---|
| Funnel Analysis | Waterfall | Impression → Click → Booking rates |
| Ranking Impact | Line chart | Position vs click rate, booking rate |
| Quality Impact | Bar chart | Star rating vs booking rate |
| Price Competitiveness Impact | Scatter | Competitiveness score vs booking rate |
| Market Segmentation | Scatter (clustered) | Price vs rating with market zones |
| Pricing Dynamics | Histogram/Box | Price competitiveness distribution by segment |
| User Behavior | Bar/Distribution | Booking window, group size by conversion |
| Data Overview | Timeline/Bar | Search volume, property count, temporal patterns |

---

## 6. Outputs

### Primary Deliverable
- **Consultant deck** (12–15 slides, PDF/PowerPoint)
  - Professional layout with data-driven visuals
  - Clear findings and recommendations
  - Appendix with methodology (optional)

### Supporting Artifacts
- **Analysis notebook** (Python/Jupyter)
  - Data exploration and transformations
  - Chart generation code
  - Statistical summaries
- **Raw data** (CSV)
  - Enhanced dataset with position, competitiveness score, segment assignments

---

## 7. Success Criteria

1. ✅ Deck tells a coherent diagnosis story (marketplace structure → patterns → implications)
2. ✅ Each analysis is data-driven with clear visualizations
3. ✅ Insights are honest about causation limits (correlation, not proof)
4. ✅ Recommendations are framed as hypotheses-to-test, not certainties
5. ✅ A/B test ideas and strategic questions include plausible expected outcomes
6. ✅ Design is consultant-grade (visual polish, clear hierarchy, narrative flow)

---

## 8. Scope & Constraints

**In scope:**
- All six analyses: market structure, positioning, pricing, segmentation, user behavior, ranking patterns
- Structural observations and competitive positioning diagnosis
- A/B test hypotheses with expected outcomes (framed as testable ideas, not proven solutions)
- Strategic questions with implications (framed as clarifications needed, not answers)
- Partner enablement recommendations (dashboards, benchmarks, transparency)
- Data collection diagnostics (identifying what's missing)
- 12–15 slide deck
- Supporting notebook with charts and code
- Presentation-ready visuals

**Out of scope:**
- Causal claims without outcome data
- "Change ranking to X" without A/B test backing
- Outcome prediction (no click/booking data)
- Implementation of recommendations (scope is diagnosis only)
- Extended blog post (can be added later if time permits)

---

## 9. Dependencies

- **Data:** sample.csv + train.csv (if needed for volume)
- **Tools:** Python (pandas, matplotlib/seaborn, numpy)
- **Timeline:** 1–2 weeks for analysis + deck creation

---

## 10. Next Steps

1. ✅ Design approved
2. → Write detailed implementation plan (writing-plans skill)
3. → Execute analyses in order
4. → Build deck with charts
5. → Iterate and finalize
