# Travel Marketplace Analysis Implementation Plan

> **For collaborative learning:** This plan is designed to be executed WITH understanding checks. After each analysis, we'll pause to interpret results together before moving forward. Use the checkpoint prompts in each task.

**Goal:** Build a Jupyter notebook that conducts 6 interconnected marketplace analyses, generate supporting visualizations, and compile findings into a 12–15 slide consultant deck.

**Architecture:** 
- Notebook-first: Load 10k sample from train.csv, verify data structure, enrich with derived metrics (competitiveness, segment), run analyses sequentially
- Each analysis is exploratory + visual: code cells for calculation, matplotlib for charts
- Collaborative interpretation: After each analysis, pause to discuss findings and validate assumptions
- PM lens: Apply critical thinking to each insight (so what? correlation vs causation? measurement approach?)
- Deck assembly: Select strongest visualizations and findings, build 12–15 slide consultant deck

**Tech Stack:**
- Python: pandas, numpy, matplotlib/seaborn, scipy
- Jupyter: interactive exploration with markdown explanations
- PNG exports: charts saved for deck
- PowerPoint: final deck assembly (manual)

---

## Phase 1: Setup & Data Enrichment

### Task 1: Setup Notebook & Load Data from train.csv

**Files:**
- Create: `.worktrees/analysis-build/analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Steps:**

- [ ] **Step 1: Create notebook structure with headers**

```
# Cell 1: Markdown
# Travel Marketplace Analysis Notebook
## A Data-Driven Diagnosis of Competitive Positioning

This notebook explores:
- Hotel marketplace structure and competitive dynamics
- Ranking impact on user click and booking behavior
- Price competitiveness and its effect on conversions
- Trust signals (ratings, reviews) as decision drivers
- Market segmentation and user behavior patterns

**Data:** 100,000 rows sampled from train.csv (seed=42)  
**Period:** 2012–2013  
**Searches:** 19,406 unique  
**Properties:** 42,870 unique

---

## Part 1: Setup & Data Verification

### 1.1 Load Libraries & Configuration
```

- [ ] **Step 2: Add imports cell**

```python
# Cell 2: Code
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Configuration
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)
pd.set_option('display.max_columns', None)
print("✓ Libraries loaded")
```

- [ ] **Step 3: Add data loading cell**

```python
# Cell 3: Code
# Load pre-sampled 100k dataset
print("Loading sample.csv (100k rows, pre-sampled with seed=42)...")
df = pd.read_csv('../data/sample.csv')

print(f"\nDataset shape: {df.shape}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"\nUnique searches: {df['srch_id'].nunique():,}")
print(f"Unique properties: {df['prop_id'].nunique():,}")
print(f"Unique sites: {df['site_id'].nunique()}")
```

Expected output: 100,000 rows × 54 columns, 19,406 searches, 42,870 properties

- [ ] **Step 4: Verify outcome data exists**

```python
# Cell 4: Code
# Verify outcome columns exist and check rates
print("Outcome Data Verification:")
print(f"click_bool in columns? {('click_bool' in df.columns)}")
print(f"booking_bool in columns? {('booking_bool' in df.columns)}")
print(f"gross_bookings_usd in columns? {('gross_bookings_usd' in df.columns)}")

print("\nOutcome Rates:")
print(f"Total impressions: {len(df):,}")
print(f"Clicks: {(df['click_bool'] == 1).sum():,} ({(df['click_bool'] == 1).sum() / len(df) * 100:.1f}%)")
print(f"Bookings: {(df['booking_bool'] == 1).sum():,} ({(df['booking_bool'] == 1).sum() / len(df) * 100:.2f}%)")
print(f"Click-to-book rate: {(df['booking_bool'] == 1).sum() / (df['click_bool'] == 1).sum() * 100:.1f}%")
print(f"\nTotal revenue: ${df[df['gross_bookings_usd'].notna()]['gross_bookings_usd'].sum():,.0f}")
```

Expected: ~2.65% booking rate, ~25% click rate, ~13% click-to-book conversion

- [ ] **Step 5: Verify data structure against definitions**

```python
# Cell 5: Code
# Quick data quality check
print("Data Type Summary:")
print(df.dtypes)

print("\n\nMissing Data (%):")
missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
print(missing_pct[missing_pct > 0].head(15))

print("\n\nPrice Range:")
print(f"Min: ${df['price_usd'].min():.2f}")
print(f"Max: ${df['price_usd'].max():.2f}")
print(f"Mean: ${df['price_usd'].mean():.2f}")
print(f"Median: ${df['price_usd'].median():.2f}")

print("\n\nCompetitor Data Coverage:")
comp_coverage = []
for i in range(1, 9):
    col = f'comp{i}_rate'
    pct = (df[col].notna().sum() / len(df) * 100)
    comp_coverage.append(pct)
print(f"Avg competitor data coverage: {np.mean(comp_coverage):.1f}%")
```

- [ ] **Step 6: Commit notebook**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb
git commit -m "task: setup notebook, load train.csv, verify outcome data"
```

---

### Task 2: Verify & Enrich Data with Competitiveness & Segmentation

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Background:** The position column in the data has gaps (positions 5, 11, 17, 23 missing), likely from filtering or A/B testing. We'll regenerate it as true ranking position. Then add two derived columns:
1. **Competitiveness Score**: Percentage difference vs competitors (from comp*_rate_percent_diff)
2. **Market Segment**: Budget/Mid/Luxury classification (based on price & rating)

**Steps:**

- [ ] **Step 1: Add markdown cell explaining enrichment**

```python
# Cell 6: Markdown
## Part 2: Data Enrichment & Validation

### 2.1 Position Column Regeneration

The dataset includes a `position` column with gaps (positions 5, 11, 17, 23 missing), indicating it may be from filtered/A/B test data. We'll regenerate true ranking position as row order within each search.

### 2.2 Competitiveness Score

We'll calculate price competitiveness relative to competitors:
- **Source:** comp*_rate_percent_diff (actual % difference vs competitors)
- **Metric:** Average % difference across all available competitors
- Positive = overpriced vs competitors, Negative = underpriced

**Why:** Understand if hotels are competitively positioned relative to direct competitors.

### 2.3 Market Segmentation

We'll classify hotels into segments based on price and rating:
- **Budget:** Low price OR low rating (≤2 stars)
- **Mid:** Medium price AND medium rating (3–4 stars)
- **Luxury:** High price AND high rating (≥4 stars)

**Why:** Enable segment-level analysis of competitive dynamics and booking behavior.
```

- [ ] **Step 2: Regenerate position column**

```python
# Cell 7: Code
print("Regenerating Position Column (True Ranking Position)...")
print(f"Before: position range {df['position'].min():.0f}–{df['position'].max():.0f}')

# Recalculate position as row order within each search
df['position'] = df.groupby('srch_id').cumcount() + 1

print(f'After: position range {df["position"].min():.0f}–{df["position"].max():.0f}')
print(f"\nPosition distribution:")
print(df['position'].value_counts().sort_index().head(10))

print(f"\nPosition stats by search:")
position_stats = df.groupby('srch_id')['position'].agg(['count', 'min', 'max', 'mean'])
print(position_stats.describe())
```

Expected: Position 1–16, with roughly 20k rows at each position (10k unique searches × ~5 hotels each).

- [ ] **Step 3: Add competitiveness score (with outlier handling)**

```python
# Cell 8: Code
# Calculate competitiveness score: average % difference vs competitors
def calculate_competitiveness(row):
    """
    Calculate price competitiveness: % difference vs competitors
    Uses comp*_rate_percent_diff (actual % difference with Expedia as denominator)
    Returns:
      Positive = overpriced relative to competitors
      Negative = underpriced
      NaN = no competitor data
    """
    comp_diffs = []
    for i in range(1, 9):  # comp1 through comp8
        diff = row[f'comp{i}_rate_percent_diff']
        if pd.notna(diff):
            comp_diffs.append(diff)
    
    if len(comp_diffs) == 0:
        return np.nan  # No competitor data
    
    # Average percentage difference across available competitors
    return np.mean(comp_diffs)

df['competitiveness_score'] = df.apply(calculate_competitiveness, axis=1)

print("Competitiveness Score Calculated:")
print(f"Non-NaN rows: {df['competitiveness_score'].notna().sum():,} ({df['competitiveness_score'].notna().sum() / len(df) * 100:.1f}%)")
print(f"Mean: {df['competitiveness_score'].mean():.2f}%")
print(f"Median: {df['competitiveness_score'].median():.2f}%")
print(f"Std: {df['competitiveness_score'].std():.2f}%")
print(f"\nRange:")
print(f"  Most underpriced: {df['competitiveness_score'].min():.2f}%")
print(f"  Most overpriced: {df['competitiveness_score'].max():.2f}%")
print(f"\nInterpretation:")
print(f"  Negative value = cheaper than competitors")
print(f"  Positive value = more expensive than competitors")
```

Expected: ~65% with competitor data, mean near $0 (some underpriced, some overpriced).

- [ ] **Step 4: Add market segmentation cell**

```python
# Cell 9: Code
# Define market segments based on price and rating percentiles
price_p33 = df['price_usd'].quantile(0.33)
price_p66 = df['price_usd'].quantile(0.66)
price_p95 = df['price_usd'].quantile(0.95)

def assign_segment(row):
    price = row['price_usd']
    rating = row['prop_starrating']
    
    # Clear luxury: high price AND high rating
    if price > price_p66 and rating >= 4:
        return 'Luxury'
    # Clear budget: low price OR low rating
    elif price < price_p33 or rating <= 2:
        return 'Budget'
    # Everything else: mid-market
    else:
        return 'Mid'

df['market_segment'] = df.apply(assign_segment, axis=1)

print("Market Segmentation Complete:")
print(f"\nSegment Counts:")
print(df['market_segment'].value_counts().sort_values(ascending=False))

print(f"\n\nSegment Characteristics:")
print(f"\nBudget Threshold: price < ${price_p33:.0f} OR rating ≤ 2 stars")
print(f"Luxury Threshold: price > ${price_p66:.0f} AND rating ≥ 4 stars")
print(f"Mid: Everything else")

print(f"\n\nBy Rating:")
print(df.groupby('market_segment')['prop_starrating'].agg(['count', 'mean', 'min', 'max']).round(2))

print(f"\n\nBy Price:")
print(df.groupby('market_segment')['price_usd'].agg(['count', 'mean', 'min', 'max']).round(2))

print(f"\n\nBy Booking Rate:")
booking_by_seg = df.groupby('market_segment').agg({
    'booking_bool': ['sum', 'mean'],
    'click_bool': ['sum', 'mean']
})
booking_by_seg.columns = ['Bookings', 'Booking_Rate', 'Clicks', 'Click_Rate']
print((booking_by_seg * 100).round(2))
```

Expected: Segments roughly balanced; luxury has higher booking rate.

- [ ] **Step 5: Verify enriched columns**

```python
# Cell 10: Code
print("Data Enrichment Summary:")
print(f"\nNew columns added:")
print(f"  ✓ competitiveness_score: {df['competitiveness_score'].notna().sum():,} non-NaN values")
print(f"  ✓ market_segment: {len(df):,} rows classified")

print(f"\nFinal dataset shape: {df.shape}")
print(f"\nColumns ready for analysis:")
analysis_cols = ['srch_id', 'position', 'price_usd', 'prop_starrating', 'prop_review_score',
                 'competitiveness_score', 'market_segment', 'click_bool', 'booking_bool', 
                 'gross_bookings_usd', 'srch_booking_window', 'srch_length_of_stay',
                 'visitor_hist_starrating', 'prop_brand_bool']
print([col for col in analysis_cols if col in df.columns])
```

- [ ] **Step 6: Commit enriched notebook**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb
git commit -m "task: verify position, add competitiveness score, segment market"
```

---

### ✋ **Understanding Checkpoint 1**

After completing Task 2, explain back in your own words:

1. **Position Column:** What values does it contain? How are hotels ordered within a search?
2. **Competitiveness Score:** 
   - How is it calculated?
   - What does a positive value mean? Negative?
   - Why did we cap at ±$1000?
3. **Market Segments:**
   - What are the price thresholds for each segment?
   - Which segment has the highest booking rate? Why?
   - Do the segments seem balanced and sensible?

---

**Why this matters:** If you can explain these derived metrics clearly, you understand the foundation for all subsequent analyses.

---

## Phase 2: Analysis 1 — Data Structure & Market Overview

### Task 3: Market Overview Analysis (Analysis 6)

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Understand what the dataset represents: time range, searches, properties, sites, seasonality.

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 9: Markdown
## Part 2: Analysis 1 — Market Overview

What is this dataset? Who is represented? What period, properties, and searches?

This gives us context for everything that follows.
```

- [ ] **Step 2: Add temporal analysis cell**

```python
# Cell 10: Code
# Temporal coverage
df['date_time'] = pd.to_datetime(df['date_time'])

print("Temporal Coverage:")
print(f"Date range: {df['date_time'].min()} to {df['date_time'].max()}")
print(f"Duration: {(df['date_time'].max() - df['date_time'].min()).days} days")
print(f"\nSearches per site:")
print(df.groupby('site_id').size())
print(f"\nSearches by destination:")
print(df.groupby('srch_destination_id').size())
```

- [ ] **Step 3: Add property distribution cell**

```python
# Cell 11: Code
# Property composition
print("Property Coverage:")
print(f"Unique properties: {df['prop_id'].nunique()}")
print(f"Properties appear in multiple searches: {(df['prop_id'].value_counts() > 1).sum()}")
print(f"Avg appearances per property: {df.groupby('prop_id').size().mean():.1f}")

print(f"\nStar rating distribution:")
print(df['prop_starrating'].value_counts().sort_index())

print(f"\nBrand presence:")
print(f"Branded hotels: {(df['prop_brand_bool'] == 1).sum()} ({(df['prop_brand_bool'] == 1).sum() / len(df) * 100:.1f}%)")
print(f"Non-branded: {(df['prop_brand_bool'] == 0).sum()} ({(df['prop_brand_bool'] == 0).sum() / len(df) * 100:.1f}%)")
```

- [ ] **Step 4: Add search behavior cell**

```python
# Cell 12: Code
# Search behavior
print("Search Behavior:")
print(f"\nBooking window (days until arrival):")
print(df['srch_booking_window'].describe())

print(f"\nLength of stay:")
print(df['srch_length_of_stay'].describe())

print(f"\nGroup composition (adults/children):")
print(f"Adult distribution: {df['srch_adults_count'].value_counts().sort_index().to_dict()}")
print(f"Has children: {(df['srch_children_count'] > 0).sum()} searches")

print(f"\nSaturday inclusion:")
print(f"Includes Saturday: {(df['srch_saturday_night_bool'] == 1).sum()} / {len(df)}")
```

- [ ] **Step 5: Run all cells and review output**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb
git commit -m "analysis: add market overview (dataset composition, temporal coverage)"
```

---

### ✋ **Understanding Checkpoint 2**

1. What time period does the dataset cover? How many days?
2. How many unique properties are in this dataset, and do they appear in multiple searches?
3. What do the booking window and length of stay distributions tell you about user urgency?

---

## Phase 3: Analysis 2 — Ranking Bias

### Task 4: Ranking Bias Analysis (Position vs Quality Signals)

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Understand: Do high-quality hotels actually rank first? Is ranking correlated with observable quality metrics?

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 13: Markdown
## Part 3: Analysis 2 — Ranking Bias

**Hypothesis:** If ranking logic is sound, higher-quality hotels should rank higher (lower position numbers).

**Metrics we'll test:**
- Position vs star rating
- Position vs review score  
- Position vs brand status

**If ranking is random:** We'd see no correlation.
**If ranking favors quality:** We'd see negative correlation (high quality = lower position number).
**If ranking is broken:** We'd see scattered/weak relationships.
```

- [ ] **Step 2: Add correlation analysis cell**

```python
# Cell 14: Code
# Correlation: position vs quality metrics
print("Ranking Bias Analysis:")
print("=" * 60)

print("\nCorrelation between position and quality signals:")
print(f"Position vs Star Rating: {df[['position', 'prop_starrating']].corr().iloc[0, 1]:.3f}")
print(f"Position vs Review Score: {df[['position', 'prop_review_score']].corr().iloc[0, 1]:.3f}")
print(f"Position vs Price: {df[['position', 'price_usd']].corr().iloc[0, 1]:.3f}")

# Brand effect
print(f"\nBrand vs Position:")
branded = df[df['prop_brand_bool'] == 1]['position'].mean()
non_branded = df[df['prop_brand_bool'] == 0]['position'].mean()
print(f"Branded hotels avg position: {branded:.1f}")
print(f"Non-branded hotels avg position: {non_branded:.1f}")
print(f"Difference: {branded - non_branded:.1f} positions")
```

Expected: Negative correlations are expected (high quality = early position). Strength varies.

- [ ] **Step 3: Add position by segment analysis cell**

```python
# Cell 15: Code
# Position by market segment
print("\nAverage position by market segment:")
position_by_segment = df.groupby('market_segment')['position'].agg(['mean', 'min', 'max', 'std', 'count'])
print(position_by_segment)

print("\nQuality metrics by position (ranking effect):")
for pos in sorted(df['position'].unique())[:5]:  # First 5 positions
    subset = df[df['position'] == pos]
    print(f"\nPosition {pos} (n={len(subset)}):")
    print(f"  Avg rating: {subset['prop_starrating'].mean():.2f}")
    print(f"  Avg review score: {subset['prop_review_score'].mean():.2f}")
    print(f"  Avg price: ${subset['price_usd'].mean():.2f}")
    print(f"  % branded: {(subset['prop_brand_bool'].mean() * 100):.1f}%")
```

- [ ] **Step 4: Create ranking bias visualization**

```python
# Cell 16: Code
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Position vs Star Rating
axes[0, 0].scatter(df['position'], df['prop_starrating'], alpha=0.6, s=50)
axes[0, 0].set_xlabel('Position')
axes[0, 0].set_ylabel('Star Rating')
axes[0, 0].set_title('Ranking Bias: Position vs Star Rating')
z = np.polyfit(df['position'].dropna(), df['prop_starrating'].dropna(), 1)
p = np.poly1d(z)
axes[0, 0].plot(sorted(df['position'].unique()), p(sorted(df['position'].unique())), "r--", alpha=0.8, label=f'Trend (r={df[["position", "prop_starrating"]].corr().iloc[0, 1]:.3f})')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Position vs Review Score
axes[0, 1].scatter(df['position'], df['prop_review_score'], alpha=0.6, s=50, color='orange')
axes[0, 1].set_xlabel('Position')
axes[0, 1].set_ylabel('Review Score')
axes[0, 1].set_title('Ranking Bias: Position vs Review Score')
z = np.polyfit(df['position'].dropna(), df['prop_review_score'].dropna(), 1)
p = np.poly1d(z)
axes[0, 1].plot(sorted(df['position'].unique()), p(sorted(df['position'].unique())), "r--", alpha=0.8, label=f'Trend (r={df[["position", "prop_review_score"]].corr().iloc[0, 1]:.3f})')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Average rating by position (top 8 positions)
top_positions = df[df['position'] <= 8].groupby('position')['prop_starrating'].mean()
axes[1, 0].bar(top_positions.index, top_positions.values, color='steelblue', alpha=0.7)
axes[1, 0].set_xlabel('Position')
axes[1, 0].set_ylabel('Avg Star Rating')
axes[1, 0].set_title('Quality by Position (Top 8)')
axes[1, 0].set_ylim([0, 5])
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Branded vs non-branded by position
branded_pos = df[df['prop_brand_bool'] == 1].groupby('position').size()
non_branded_pos = df[df['prop_brand_bool'] == 0].groupby('position').size()
x = np.arange(min(8, len(branded_pos)))
axes[1, 1].bar(x - 0.2, branded_pos.iloc[:8].values, 0.4, label='Branded', alpha=0.7)
axes[1, 1].bar(x + 0.2, non_branded_pos.iloc[:8].values, 0.4, label='Non-branded', alpha=0.7)
axes[1, 1].set_xlabel('Position')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Brand Distribution by Position (Top 8)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../outputs/charts/02_ranking_bias.png', dpi=300, bbox_inches='tight')
print("Chart saved: 02_ranking_bias.png")
plt.show()
```

- [ ] **Step 5: Run and verify visualization creates 02_ranking_bias.png**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/outputs/charts/02_ranking_bias.png
git commit -m "analysis: ranking bias (position vs quality signals)"
```

---

### ✋ **Understanding Checkpoint 3**

Before moving to the next analysis, answer:
1. What's the correlation between position and star rating? Does it suggest ranking logic is quality-aware?
2. Do branded hotels rank higher than non-branded? By how much?
3. Looking at the charts, does ranking seem fair, or are there high-quality hotels buried at lower positions?

---

## Phase 4: Analysis 3 — Competitive Positioning

### Task 5: Competitive Positioning Analysis (Price vs Quality)

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Understand market equilibrium: Are prices aligned with quality, or trapped in inefficient positions?

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 17: Markdown
## Part 4: Analysis 3 — Competitive Positioning

**Question:** Are hotels priced efficiently relative to their quality?

**Method:** For each hotel, compare its price to:
1. Average competitor price (competitiveness_score we calculated earlier)
2. Market equilibrium (expected price for rating/quality)

**Insights we're looking for:**
- Underpriced high-quality hotels (opportunity)
- Overpriced low-quality hotels (exposed)
- Clear price-quality relationship (efficient market) vs scattered (inefficient)
```

- [ ] **Step 2: Add competitiveness distribution analysis**

```python
# Cell 18: Code
# Price competitiveness analysis
print("Price Competitiveness Analysis:")
print("=" * 60)

print(f"\nCompetitiveness Score (price vs competitors):")
print(df['competitiveness_score'].describe())

print(f"\nCompetitiveness by market segment:")
competitiveness_by_segment = df.groupby('market_segment')['competitiveness_score'].agg(['count', 'mean', 'std', 'min', 'max'])
print(competitiveness_by_segment)

print(f"\nUnderpriced (saving vs competitors):")
underpriced = df[df['competitiveness_score'] < -10]
print(f"Hotels: {len(underpriced)} ({len(underpriced)/len(df)*100:.1f}%)")
print(f"Avg rating: {underpriced['prop_starrating'].mean():.2f}")
print(f"Avg review score: {underpriced['prop_review_score'].mean():.2f}")

print(f"\nOverpriced (premium vs competitors):")
overpriced = df[df['competitiveness_score'] > 10]
print(f"Hotels: {len(overpriced)} ({len(overpriced)/len(df)*100:.1f}%)")
print(f"Avg rating: {overpriced['prop_starrating'].mean():.2f}")
print(f"Avg review score: {overpriced['prop_review_score'].mean():.2f}")
```

- [ ] **Step 3: Add price-quality scatter analysis**

```python
# Cell 19: Code
# Price vs rating (market equilibrium)
print("\nPrice-Quality Relationship:")
print(f"Correlation (price vs rating): {df[['price_usd', 'prop_starrating']].corr().iloc[0, 1]:.3f}")
print(f"Correlation (price vs review score): {df[['price_usd', 'prop_review_score']].corr().iloc[0, 1]:.3f}")

# Identify outliers: high quality, low price (opportunity) and low quality, high price (risk)
df['price_percentile'] = df['price_usd'].rank(pct=True)
df['rating_percentile'] = df['prop_starrating'].rank(pct=True)

high_value = df[(df['rating_percentile'] > 0.75) & (df['price_percentile'] < 0.25)]
poor_value = df[(df['rating_percentile'] < 0.25) & (df['price_percentile'] > 0.75)]

print(f"\nHigh value opportunities (high rating, low price): {len(high_value)} hotels")
if len(high_value) > 0:
    print(f"  Avg price: ${high_value['price_usd'].mean():.2f}")
    print(f"  Avg rating: {high_value['prop_starrating'].mean():.2f}")
    print(f"  Avg position: {high_value['position'].mean():.1f}")

print(f"\nPoor value (low rating, high price): {len(poor_value)} hotels")
if len(poor_value) > 0:
    print(f"  Avg price: ${poor_value['price_usd'].mean():.2f}")
    print(f"  Avg rating: {poor_value['prop_starrating'].mean():.2f}")
    print(f"  Avg position: {poor_value['position'].mean():.1f}")
```

- [ ] **Step 4: Create competitive positioning visualization**

```python
# Cell 20: Code
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Price vs Rating (all properties)
scatter = axes[0, 0].scatter(df['price_usd'], df['prop_starrating'], 
                            c=df['position'], cmap='viridis', s=80, alpha=0.6)
axes[0, 0].set_xlabel('Price (USD)')
axes[0, 0].set_ylabel('Star Rating')
axes[0, 0].set_title('Competitive Positioning: Price vs Rating (colored by position)')
cbar = plt.colorbar(scatter, ax=axes[0, 0])
cbar.set_label('Position')
axes[0, 0].grid(True, alpha=0.3)

# Competitiveness by segment
segment_order = ['Budget', 'Mid', 'Luxury']
competitiveness_data = [df[df['market_segment'] == seg]['competitiveness_score'].dropna() for seg in segment_order]
axes[0, 1].boxplot(competitiveness_data, labels=segment_order)
axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Fair price')
axes[0, 1].set_ylabel('Competitiveness Score ($)')
axes[0, 1].set_title('Price Competitiveness by Market Segment')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# High value vs poor value
colors = []
for idx, row in df.iterrows():
    if idx in high_value.index:
        colors.append('green')
    elif idx in poor_value.index:
        colors.append('red')
    else:
        colors.append('gray')

axes[1, 0].scatter(df['price_usd'], df['prop_starrating'], c=colors, s=80, alpha=0.6)
axes[1, 0].set_xlabel('Price (USD)')
axes[1, 0].set_ylabel('Star Rating')
axes[1, 0].set_title('Value Positioning (Green=high value, Red=poor value)')
axes[1, 0].grid(True, alpha=0.3)

# Price distribution by segment
for segment in segment_order:
    segment_df = df[df['market_segment'] == segment]
    axes[1, 1].hist(segment_df['price_usd'], alpha=0.6, label=segment, bins=10)
axes[1, 1].set_xlabel('Price (USD)')
axes[1, 1].set_ylabel('Count')
axes[1, 1].set_title('Price Distribution by Market Segment')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../outputs/charts/03_competitive_positioning.png', dpi=300, bbox_inches='tight')
print("Chart saved: 03_competitive_positioning.png")
plt.show()
```

- [ ] **Step 5: Run and verify visualization**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/outputs/charts/03_competitive_positioning.png
git commit -m "analysis: competitive positioning (price vs quality, market equilibrium)"
```

---

### ✋ **Understanding Checkpoint 4**

1. Is there a strong correlation between price and rating? Does that indicate an efficient market or scattered inefficiency?
2. How many high-value hotels (high rating, low price) exist, and where are they ranked?
3. What do underpriced vs overpriced hotels have in common?

---

## Phase 5: Analysis 4 — Market Segmentation

### Task 6: Market Segmentation Analysis

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Are budget, mid-tier, and luxury markets clearly separated, or muddled?

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 21: Markdown
## Part 5: Analysis 4 — Market Segmentation

**Question:** Do clear market segments exist, or is the market commoditized?

**Segmentation approach:** We classified hotels into Budget/Mid/Luxury earlier. Now we'll validate that these are actually distinct markets with:
- Different pricing
- Different quality expectations
- Different competitive dynamics
```

- [ ] **Step 2: Add segment composition analysis**

```python
# Cell 22: Code
print("Market Segmentation Analysis:")
print("=" * 60)

# Segment sizes and composition
print("\nSegment composition:")
segment_stats = df.groupby('market_segment').agg({
    'prop_id': 'count',
    'price_usd': ['mean', 'min', 'max'],
    'prop_starrating': ['mean', 'min', 'max'],
    'prop_review_score': ['mean', 'min', 'max'],
    'prop_brand_bool': lambda x: (x == 1).sum() / len(x) * 100,  # % branded
    'position': 'mean'
}).round(2)

print(segment_stats)

# Within-segment competition
print("\nWithin-segment analysis:")
for segment in ['Budget', 'Mid', 'Luxury']:
    segment_df = df[df['market_segment'] == segment]
    print(f"\n{segment} Segment:")
    print(f"  Properties: {len(segment_df)}")
    print(f"  Price range: ${segment_df['price_usd'].min():.2f} – ${segment_df['price_usd'].max():.2f}")
    print(f"  Price std dev: ${segment_df['price_usd'].std():.2f}")
    print(f"  Rating range: {segment_df['prop_starrating'].min():.1f} – {segment_df['prop_starrating'].max():.1f}")
    print(f"  Brand presence: {(segment_df['prop_brand_bool'] == 1).sum()} / {len(segment_df)}")
```

- [ ] **Step 3: Add cross-segment analysis**

```python
# Cell 23: Code
# Do segments compete with each other?
print("Cross-segment comparison:")
print(f"\nAverage price premium by segment:")
prices_by_segment = df.groupby('market_segment')['price_usd'].mean().sort_values()
for segment in prices_by_segment.index:
    price = prices_by_segment[segment]
    print(f"{segment}: ${price:.2f}")

print(f"\nOverlap: Do segment price ranges overlap?")
for i, segment1 in enumerate(['Budget', 'Mid', 'Luxury']):
    df1 = df[df['market_segment'] == segment1]
    for segment2 in ['Budget', 'Mid', 'Luxury'][i+1:]:
        df2 = df[df['market_segment'] == segment2]
        overlap = (df1['price_usd'].max() >= df2['price_usd'].min()) and (df2['price_usd'].max() >= df1['price_usd'].min())
        overlap_pct = len(df1[(df1['price_usd'] >= df2['price_usd'].min()) & (df1['price_usd'] <= df2['price_usd'].max())]) / len(df1) * 100
        print(f"{segment1} ↔ {segment2}: {overlap_pct:.1f}% of {segment1} properties overlap in price")
```

- [ ] **Step 4: Create market segmentation visualization**

```python
# Cell 24: Code
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Segment distribution (pie)
segment_counts = df['market_segment'].value_counts()
axes[0, 0].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', startangle=90)
axes[0, 0].set_title('Market Segment Distribution')

# Price by segment (box plot)
segment_order = ['Budget', 'Mid', 'Luxury']
price_data = [df[df['market_segment'] == seg]['price_usd'].values for seg in segment_order]
bp = axes[0, 1].boxplot(price_data, labels=segment_order, patch_artist=True)
for patch, color in zip(bp['boxes'], ['lightblue', 'lightgreen', 'lightyellow']):
    patch.set_facecolor(color)
axes[0, 1].set_ylabel('Price (USD)')
axes[0, 1].set_title('Price Distribution by Segment')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Rating by segment
rating_data = [df[df['market_segment'] == seg]['prop_starrating'].values for seg in segment_order]
axes[1, 0].boxplot(rating_data, labels=segment_order, patch_artist=True)
axes[1, 0].set_ylabel('Star Rating')
axes[1, 0].set_title('Quality (Rating) Distribution by Segment')
axes[1, 0].set_ylim([0, 5.5])
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Segment composition by position
position_segment = pd.crosstab(df['position'], df['market_segment'])
position_segment_pct = position_segment.div(position_segment.sum(axis=1), axis=0)
position_segment_pct.iloc[:10].plot(kind='bar', stacked=True, ax=axes[1, 1], color=['lightblue', 'lightgreen', 'lightyellow'])
axes[1, 1].set_xlabel('Position')
axes[1, 1].set_ylabel('% of Hotels')
axes[1, 1].set_title('Segment Distribution by Ranking Position (Top 10)')
axes[1, 1].legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../outputs/charts/04_market_segmentation.png', dpi=300, bbox_inches='tight')
print("Chart saved: 04_market_segmentation.png")
plt.show()
```

- [ ] **Step 5: Run and verify visualization**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/outputs/charts/04_market_segmentation.png
git commit -m "analysis: market segmentation (budget/mid/luxury stratification)"
```

---

### ✋ **Understanding Checkpoint 5**

1. Are the three market segments (Budget/Mid/Luxury) clearly distinct, or do they overlap significantly?
2. Do different segments have different quality expectations (ratings)?
3. Looking at position distribution: does ranking favor one segment over others?

---

## Phase 6: Analysis 5 — Pricing Dynamics

### Task 7: Pricing Dynamics Analysis

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Which hotels are trapped in bad pricing positions? How intense is price competition by segment?

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 25: Markdown
## Part 6: Analysis 5 — Pricing Dynamics

**Question:** Are prices efficient within segments, or trapped?

**Analysis:** Look at competitiveness scores within segments, identify over/underpriced hotels, measure competition intensity.
```

- [ ] **Step 2: Add pricing efficiency analysis**

```python
# Cell 26: Code
print("Pricing Dynamics Analysis:")
print("=" * 60)

# Competitiveness by segment
print("\nPricing efficiency by segment:")
for segment in ['Budget', 'Mid', 'Luxury']:
    segment_df = df[df['market_segment'] == segment]
    competitiveness = segment_df['competitiveness_score'].dropna()
    if len(competitiveness) > 0:
        print(f"\n{segment} Segment:")
        print(f"  Mean competitiveness: ${competitiveness.mean():.2f}")
        print(f"  Std dev: ${competitiveness.std():.2f}")
        print(f"  Underpriced (< -$10): {(competitiveness < -10).sum()} hotels")
        print(f"  Overpriced (> +$10): {(competitiveness > 10).sum()} hotels")
        print(f"  Fair priced (±$10): {((competitiveness >= -10) & (competitiveness <= 10)).sum()} hotels")

# Competition intensity (price dispersion)
print("\nCompetition intensity (price dispersion) by segment:")
for segment in ['Budget', 'Mid', 'Luxury']:
    segment_df = df[df['market_segment'] == segment]
    price_std = segment_df['price_usd'].std()
    price_mean = segment_df['price_usd'].mean()
    cv = (price_std / price_mean) * 100  # Coefficient of variation
    print(f"{segment}: Price CV = {cv:.1f}% (higher = more competition/differentiation)")
```

- [ ] **Step 3: Add trap identification analysis**

```python
# Cell 27: Code
# Identify hotels trapped in bad positions
print("\nTrapped Hotels Analysis:")
print("=" * 60)

# High rating but underpriced AND low position
trapped_underpriced = df[(df['prop_starrating'] >= 4) & 
                          (df['competitiveness_score'] < -15) & 
                          (df['position'] > 5)]

print(f"\nHigh-quality underpriced hotels ranked > position 5: {len(trapped_underpriced)}")
if len(trapped_underpriced) > 0:
    print(f"  Avg rating: {trapped_underpriced['prop_starrating'].mean():.2f}")
    print(f"  Avg price: ${trapped_underpriced['price_usd'].mean():.2f}")
    print(f"  Avg position: {trapped_underpriced['position'].mean():.1f}")
    print(f"  Avg competitiveness: ${trapped_underpriced['competitiveness_score'].mean():.2f}")

# Low quality but overpriced AND high position
trapped_overpriced = df[(df['prop_starrating'] <= 2) & 
                        (df['competitiveness_score'] > 15) & 
                        (df['position'] <= 3)]

print(f"\nLow-quality overpriced hotels ranked ≤ position 3: {len(trapped_overpriced)}")
if len(trapped_overpriced) > 0:
    print(f"  Avg rating: {trapped_overpriced['prop_starrating'].mean():.2f}")
    print(f"  Avg price: ${trapped_overpriced['price_usd'].mean():.2f}")
    print(f"  Avg position: {trapped_overpriced['position'].mean():.1f}")
```

- [ ] **Step 4: Create pricing dynamics visualization**

```python
# Cell 28: Code
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Competitiveness by segment (violin)
segment_order = ['Budget', 'Mid', 'Luxury']
competitiveness_data = [df[df['market_segment'] == seg]['competitiveness_score'].dropna().values for seg in segment_order]
parts = axes[0, 0].violinplot(competitiveness_data, positions=range(len(segment_order)), showmeans=True)
axes[0, 0].axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Fair price')
axes[0, 0].set_xticks(range(len(segment_order)))
axes[0, 0].set_xticklabels(segment_order)
axes[0, 0].set_ylabel('Competitiveness Score ($)')
axes[0, 0].set_title('Price Competitiveness Distribution by Segment')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Price vs competitiveness (with segment colors)
colors_map = {'Budget': 'blue', 'Mid': 'green', 'Luxury': 'orange'}
for segment in segment_order:
    segment_df = df[df['market_segment'] == segment]
    axes[0, 1].scatter(segment_df['price_usd'], segment_df['competitiveness_score'], 
                      label=segment, alpha=0.6, s=80, color=colors_map[segment])
axes[0, 1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
axes[0, 1].set_xlabel('Price (USD)')
axes[0, 1].set_ylabel('Competitiveness Score ($)')
axes[0, 1].set_title('Price vs Competitiveness by Segment')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Price dispersion (competition intensity)
segment_cv = []
for segment in segment_order:
    segment_df = df[df['market_segment'] == segment]
    cv = (segment_df['price_usd'].std() / segment_df['price_usd'].mean()) * 100
    segment_cv.append(cv)

axes[1, 0].bar(segment_order, segment_cv, color=['blue', 'green', 'orange'], alpha=0.7)
axes[1, 0].set_ylabel('Coefficient of Variation (%)')
axes[1, 0].set_title('Price Competition Intensity by Segment\n(Higher = more competition)')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Trapped hotels (rating vs competitiveness)
colors = []
for idx, row in df.iterrows():
    if row['prop_starrating'] >= 4 and row['competitiveness_score'] < -15:
        colors.append('green')  # Underpriced high-quality
    elif row['prop_starrating'] <= 2 and row['competitiveness_score'] > 15:
        colors.append('red')  # Overpriced low-quality
    else:
        colors.append('gray')

axes[1, 1].scatter(df['prop_starrating'], df['competitiveness_score'], c=colors, s=80, alpha=0.6)
axes[1, 1].axhline(y=0, color='k', linestyle='-', alpha=0.2)
axes[1, 1].set_xlabel('Star Rating')
axes[1, 1].set_ylabel('Competitiveness Score ($)')
axes[1, 1].set_title('Hotel Quality vs Pricing\n(Green=underpriced value, Red=overpriced)')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../outputs/charts/05_pricing_dynamics.png', dpi=300, bbox_inches='tight')
print("Chart saved: 05_pricing_dynamics.png")
plt.show()
```

- [ ] **Step 5: Run and verify visualization**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/outputs/charts/05_pricing_dynamics.png
git commit -m "analysis: pricing dynamics (competition intensity, trapped hotels)"
```

---

### ✋ **Understanding Checkpoint 6**

1. Which segment (Budget/Mid/Luxury) has the most intense price competition?
2. How many high-quality hotels are trapped being underpriced?
3. What does the competitiveness score distribution tell you about each segment's pricing strategy?

---

## Phase 7: Analysis 6 — User Behavior Segmentation

### Task 8: User Behavior Segmentation Analysis

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Understand traveler profiles: urgency, group composition, repeat behavior.

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 29: Markdown
## Part 7: Analysis 6 — User Behavior Segmentation

**Key insight:** All users in this dataset are NEW users (100% NULL visitor history).

This tells us we can't segment returning vs new users, but we CAN understand their travel urgency and context from:
- Booking window (how far in advance?)
- Length of stay
- Group composition (solo, couple, family)
- Saturday inclusion (leisure vs business)
```

- [ ] **Step 2: Add user behavior segmentation analysis**

```python
# Cell 30: Code
print("User Behavior Segmentation Analysis:")
print("=" * 60)

# Booking window segments
print("\nBooking Window (advance planning):")
df['booking_window_segment'] = pd.cut(df['srch_booking_window'], 
                                      bins=[0, 2, 21, 90, 250],
                                      labels=['Last-minute (0-2 days)', 
                                             'Short-term (3-21 days)', 
                                             'Mid-term (22-90 days)', 
                                             'Long-term (90+ days)'])

booking_seg = df['booking_window_segment'].value_counts().sort_index()
print(booking_seg)
print(f"  % last-minute: {(df['srch_booking_window'] <= 2).sum() / len(df) * 100:.1f}%")

# Length of stay segments
print("\nLength of Stay:")
df['stay_segment'] = pd.cut(df['srch_length_of_stay'],
                            bins=[0, 1, 3, 7, 10],
                            labels=['1 night', '2-3 nights', '4-7 nights', '7+ nights'],
                            right=False)

stay_seg = df['stay_segment'].value_counts().sort_index()
print(stay_seg)

# Group composition
print("\nGroup Composition:")
print(f"Solo travelers (1 adult, no children): {((df['srch_adults_count'] == 1) & (df['srch_children_count'] == 0)).sum()}")
print(f"Couples (2 adults, no children): {((df['srch_adults_count'] == 2) & (df['srch_children_count'] == 0)).sum()}")
print(f"Families with children: {(df['srch_children_count'] > 0).sum()}")
print(f"Larger groups (3+ adults): {(df['srch_adults_count'] >= 3).sum()}")

# Weekend travel
print(f"\nWeekend travel (includes Saturday): {(df['srch_saturday_night_bool'] == 1).sum()} / {len(df)} ({(df['srch_saturday_night_bool'] == 1).sum() / len(df) * 100:.1f}%)")

# Room count
print(f"\nRooms booked:")
print(df['srch_room_count'].value_counts().sort_index())
```

- [ ] **Step 3: Add cross-segment analysis**

```python
# Cell 31: Code
# Which market segments do different user types prefer?
print("\nUser type vs market segment preference:")
print("=" * 60)

# Last-minute bookers
last_minute = df[df['srch_booking_window'] <= 2]
print(f"\nLast-minute bookers (n={len(last_minute)}):")
print(f"  Preferred segment: {last_minute['market_segment'].mode().values}")
print(f"  Avg price: ${last_minute['price_usd'].mean():.2f}")
print(f"  Avg position of clicked hotel: {last_minute['position'].mean():.1f}")

# Long-term planners
long_term = df[df['srch_booking_window'] > 90]
print(f"\nLong-term planners (n={len(long_term)}):")
print(f"  Preferred segment: {long_term['market_segment'].mode().values if len(long_term) > 0 else 'N/A'}")
if len(long_term) > 0:
    print(f"  Avg price: ${long_term['price_usd'].mean():.2f}")
    print(f"  Avg position: {long_term['position'].mean():.1f}")

# Families
families = df[df['srch_children_count'] > 0]
print(f"\nFamilies with children (n={len(families)}):")
print(f"  Preferred segment: {families['market_segment'].mode().values if len(families) > 0 else 'N/A'}")
if len(families) > 0:
    print(f"  Avg hotel rating: {families['prop_starrating'].mean():.2f}")
    print(f"  Avg stay length: {families['srch_length_of_stay'].mean():.1f} nights")
```

- [ ] **Step 4: Create user behavior visualization**

```python
# Cell 32: Code
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Booking window distribution (log scale for readability)
booking_window_bins = [0, 2, 7, 21, 90, 250]
booking_window_labels = ['0-2\n(last-min)', '3-7\n(urgent)', '8-21\n(planned)', '22-90\n(casual)', '90+\n(early)']
booking_window_cat = pd.cut(df['srch_booking_window'], bins=booking_window_bins)
booking_counts = booking_window_cat.value_counts().sort_index()

axes[0, 0].bar(range(len(booking_counts)), booking_counts.values, color='steelblue', alpha=0.7)
axes[0, 0].set_xticks(range(len(booking_counts)))
axes[0, 0].set_xticklabels(booking_window_labels)
axes[0, 0].set_ylabel('Number of Searches')
axes[0, 0].set_title('Booking Window Distribution (User Urgency)')
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Length of stay
stay_counts = df['stay_segment'].value_counts().sort_index()
axes[0, 1].bar(range(len(stay_counts)), stay_counts.values, color='green', alpha=0.7)
axes[0, 1].set_xticks(range(len(stay_counts)))
axes[0, 1].set_xticklabels(stay_counts.index)
axes[0, 1].set_ylabel('Number of Searches')
axes[0, 1].set_title('Length of Stay Distribution')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Group composition
group_labels = ['Solo\n(1 adult)', 'Couple\n(2 adults)', '3+ Adults', 'With\nChildren']
group_counts = [
    ((df['srch_adults_count'] == 1) & (df['srch_children_count'] == 0)).sum(),
    ((df['srch_adults_count'] == 2) & (df['srch_children_count'] == 0)).sum(),
    (df['srch_adults_count'] >= 3).sum(),
    (df['srch_children_count'] > 0).sum()
]
axes[1, 0].bar(group_labels, group_counts, color='orange', alpha=0.7)
axes[1, 0].set_ylabel('Number of Searches')
axes[1, 0].set_title('Group Composition Distribution')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Booking window vs market segment preference
booking_window_segment_crosstab = pd.crosstab(df['booking_window_segment'], df['market_segment'])
booking_window_segment_crosstab_pct = booking_window_segment_crosstab.div(booking_window_segment_crosstab.sum(axis=1), axis=0)

booking_window_segment_crosstab_pct.plot(kind='bar', stacked=True, ax=axes[1, 1], 
                                          color=['lightblue', 'lightgreen', 'lightyellow'])
axes[1, 1].set_xlabel('Booking Window')
axes[1, 1].set_ylabel('% of Searches')
axes[1, 1].set_title('Market Segment Preference by Booking Window')
axes[1, 1].legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45, ha='right')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../outputs/charts/06_user_behavior.png', dpi=300, bbox_inches='tight')
print("Chart saved: 06_user_behavior.png")
plt.show()
```

- [ ] **Step 5: Run and verify visualization**

- [ ] **Step 6: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb analysis/outputs/charts/06_user_behavior.png
git commit -m "analysis: user behavior segmentation (urgency, group composition, stay length)"
```

---

### ✋ **Understanding Checkpoint 7**

1. What percentage of searches are last-minute (0-2 days)? What does this suggest about user urgency?
2. Do different booking windows correspond to different market segment preferences?
3. Are families more likely to book higher-rated hotels than solo travelers?

---

## Phase 8: Synthesis & Deck Assembly

### Task 9: Synthesize Findings & Create Data Summary

**Files:**
- Modify: `analysis/notebooks/2026-04-18-marketplace-analysis.ipynb`

**Purpose:** Summarize the key findings across all analyses in preparation for deck building.

**Steps:**

- [ ] **Step 1: Add markdown section**

```python
# Cell 33: Markdown
## Part 8: Synthesis — Key Findings

Based on the six analyses, we've identified patterns in:
1. Market structure and composition
2. Ranking logic and potential biases
3. Competitive positioning and pricing efficiency
4. Market segmentation and stratification
5. Pricing dynamics and competition intensity
6. User behavior and travel urgency

Now we synthesize these into actionable insights for the deck.
```

- [ ] **Step 2: Add finding summary cell**

```python
# Cell 34: Code
print("KEY FINDINGS SUMMARY")
print("=" * 80)

# Finding 1: Ranking bias
print("\n1. RANKING BIAS")
print(f"   Position-Rating Correlation: {df[['position', 'prop_starrating']].corr().iloc[0, 1]:.3f}")
print(f"   → Interpretation: {'Weak' if abs(df[['position', 'prop_starrating']].corr().iloc[0, 1]) < 0.3 else 'Moderate' if abs(df[['position', 'prop_starrating']].corr().iloc[0, 1]) < 0.6 else 'Strong'} correlation")
branded_avg_pos = df[df['prop_brand_bool'] == 1]['position'].mean()
non_branded_avg_pos = df[df['prop_brand_bool'] == 0]['position'].mean()
print(f"   Brand advantage: {abs(branded_avg_pos - non_branded_avg_pos):.1f} positions")

# Finding 2: Competitive positioning
high_value_count = len(df[(df['prop_starrating'] >= 4) & (df['price_usd'] < df['price_usd'].quantile(0.25))])
print(f"\n2. COMPETITIVE POSITIONING")
print(f"   High-value hotels (high quality, low price): {high_value_count}")
print(f"   Avg position of high-value hotels: {df[(df['prop_starrating'] >= 4) & (df['price_usd'] < df['price_usd'].quantile(0.25))]['position'].mean():.1f}")
print(f"   → Indicates potential inefficiency in ranking/visibility")

# Finding 3: Market segmentation
print(f"\n3. MARKET SEGMENTATION")
segment_sizes = df['market_segment'].value_counts()
print(f"   Budget: {segment_sizes['Budget']} hotels")
print(f"   Mid: {segment_sizes['Mid']} hotels")
print(f"   Luxury: {segment_sizes['Luxury']} hotels")
overlap_pct = len(df[(df['price_usd'] >= df[df['market_segment']=='Budget']['price_usd'].max()) & 
                      (df['price_usd'] <= df[df['market_segment']=='Luxury']['price_usd'].min())]) / len(df) * 100
print(f"   Price overlap: {overlap_pct:.0f}% of hotels in overlapping price ranges")

# Finding 4: Pricing dynamics
underpriced_high_quality = len(df[(df['prop_starrating'] >= 4) & (df['competitiveness_score'] < -10)])
print(f"\n4. PRICING DYNAMICS")
print(f"   Underpriced high-quality hotels: {underpriced_high_quality}")
print(f"   Overpriced low-quality hotels: {len(df[(df['prop_starrating'] <= 2) & (df['competitiveness_score'] > 10)])}")

# Finding 5: User urgency
last_minute_pct = (df['srch_booking_window'] <= 2).sum() / len(df) * 100
print(f"\n5. USER BEHAVIOR")
print(f"   Last-minute bookings (0-2 days): {last_minute_pct:.1f}%")
print(f"   → High urgency may reduce price sensitivity")

# Finding 6: Data limitations
print(f"\n6. DATA LIMITATIONS")
print(f"   No outcome data (clicks, bookings)")
print(f"   All users are new (100% NULL visitor history)")
print(f"   Limited competitor data (sparse across searches)")
print(f"   → Cannot measure direct impact of ranking/pricing on bookings")
```

- [ ] **Step 3: Add recommendations preview**

```python
# Cell 35: Code
print("\n" + "=" * 80)
print("RECOMMENDATION PREVIEW FOR DECK")
print("=" * 80)

print("""
DIAGNOSTIC TOOLS
─────────────────
→ Partner Competitiveness Dashboard
   Shows: Your price vs competitors, position in market, segment ranking
   Expected benefit: Helps partners understand their competitive position
   
→ Market Benchmarking Reports
   Shows: Segment averages, price bands, quality ranges
   Expected benefit: Partners self-serve insights instead of support tickets

A/B TEST HYPOTHESES (To validate with outcome data)
──────────────────────────────────────────────────
→ Hypothesis 1: Clear market segmentation improves user confidence
   Test: Show budget/mid/luxury separately vs mixed results
   Expected: 5-15% CTR improvement if segment clarity matters
   
→ Hypothesis 2: Highlight high-value hotels improves conversions
   Test: Boost underpriced high-quality hotels in ranking
   Expected: Higher booking rate for repositioned hotels
   
→ Hypothesis 3: Partner transparency increases satisfaction
   Test: Release "why am I ranked here?" dashboard
   Expected: Improved partner NPS, reduced support load

STRATEGIC QUESTIONS (Require business clarification)
───────────────────────────────────────────────────
→ Q1: What is ranking optimized for? (Revenue-per-search vs conversion rate?)
→ Q2: Do users engage with ranking, or sort by price/rating?
→ Q3: Is current market segmentation efficient, or should we reshape it?
""")
```

- [ ] **Step 4: Run and review output**

- [ ] **Step 5: Commit**

```bash
git add analysis/notebooks/2026-04-18-marketplace-analysis.ipynb
git commit -m "analysis: synthesize findings and preview recommendations"
```

---

### ✋ **Understanding Checkpoint 8 — Final Interpretation Check**

Before moving to deck building, summarize in your own words:

1. What are the 3 strongest findings from all analyses?
2. Which findings suggest ranking might be broken vs working-as-designed?
3. What data gaps prevent us from making causal claims?
4. Which A/B test hypothesis excites you most, and why?

---

## Phase 9: Deck Assembly

### Task 10: Build Consultant Deck (12–15 slides)

**Files:**
- Create: `analysis/outputs/deck/Travel_Marketplace_Analysis.pptx` (manual creation recommended, or Python+python-pptx if preferred)

**Purpose:** Assemble findings into a professional 12–15 slide consultant deck.

**Slides to create:**

1. **Title** — "Marketplace Positioning Analysis: Where Efficiency Breaks Down"
2. **Executive Summary** — 1-2 key findings
3. **System Overview** — Dataset scope, searches, properties, time period
4. **Ranking Bias** — Position vs quality correlations + 02_ranking_bias.png
5. **Competitive Positioning** — Price vs quality + 03_competitive_positioning.png + high-value discovery
6. **Market Segmentation** — Budget/mid/luxury stratification + 04_market_segmentation.png
7. **Pricing Dynamics** — Competition intensity + trapped hotels + 05_pricing_dynamics.png
8. **User Behavior** — Urgency and demographics + 06_user_behavior.png
9. **Key Findings** — 3-4 core insights with caveats
10. **Diagnostic Tools** — Partner dashboard, benchmarking
11. **A/B Test Ideas** — 3 hypotheses with expected outcomes (framed as testable)
12. **Strategic Questions** — 3-4 questions that need answers before optimization
13. **Data Gaps to Close** — What we need to move from diagnosis to action
14. **Expected Impact** — Qualitative reasoning on partner/platform benefits
15. **Closing** — Why this analysis matters strategically

**Steps:**

- [ ] **Step 1: Gather all chart assets**

Collect the 6 PNG charts generated earlier:
- `02_ranking_bias.png`
- `03_competitive_positioning.png`
- `04_market_segmentation.png`
- `05_pricing_dynamics.png`
- `06_user_behavior.png`

- [ ] **Step 2: Create PowerPoint structure (if using python-pptx)**

```python
# Cell 36: Code
# Optional: Generate deck skeleton with python-pptx
# For now, recommend manual assembly in PowerPoint for polish

from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# Slide 1: Title
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
title_box = slide1.shapes.add_textbox(Inches(0.5), Inches(3), Inches(9), Inches(1.5))
title_frame = title_box.text_frame
title_frame.text = "Marketplace Positioning Analysis\nWhere Efficiency Breaks Down"
title_frame.paragraphs[0].font.size = Pt(54)
title_frame.paragraphs[0].font.bold = True

prs.save('../outputs/deck/Travel_Marketplace_Analysis.pptx')
print("Deck skeleton created. Open in PowerPoint and add:")
print("- Slide content from findings")
print("- Chart images (02–06)")
print("- Text and formatting")
```

- [ ] **Step 3: Alternatively, assemble manually in PowerPoint**

Use PowerPoint desktop app:
- Create new presentation
- Add 15 slides
- Copy text from findings summary (Cell 34) into slides 2, 9
- Insert 6 PNG charts into slides 4–8
- Add text for slides 10–15 from Cell 35 recommendations
- Format with consistent branding (title fonts, colors, layout)

- [ ] **Step 4: Review for narrative flow**

Read through slides 1–15 in order. Check:
- Does it tell a coherent story? (structure → findings → implications)
- Are caveats clear? (no causal claims without data)
- Are recommendations framed as hypotheses?
- Does closing reinforce value?

- [ ] **Step 5: Commit**

```bash
git add analysis/outputs/deck/Travel_Marketplace_Analysis.pptx
git commit -m "deliverable: compile 12-15 slide consultant deck"
```

---

## Summary Checklist

- [ ] Notebook complete with 6 analyses
- [ ] 6 visualizations generated and saved
- [ ] Findings synthesized and documented
- [ ] 12–15 slide deck assembled and formatted
- [ ] All analyses have interpretation checkpoints completed
- [ ] Recommendations framed as hypotheses (not certainties)
- [ ] Data gaps and limitations documented
- [ ] All commits pushed
