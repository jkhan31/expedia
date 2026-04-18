# Data Definitions: Hotel Booking Marketplace Dataset

**Source:** Kaggle Expedia Personalized Sort (ICDM 2013) Competition  
**Dataset:** train.csv (sampled: 100,000 rows)  
**Time Period:** 2012–2013  
**Searches:** 19,406 unique  
**Properties:** 42,870 unique  
**Key Feature:** Outcome data available (click_bool, booking_bool, gross_bookings_usd)

**For complete official column definitions, see:** [expedia-kaggle-column-definitions.md](expedia-kaggle-column-definitions.md)

---

## Column Definitions

### Search & Session Identifiers

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| srch_id | int64 | Unique search identifier | Links all hotels in one search |
| date_time | object | Timestamp of search | Format: YYYY-MM-DD HH:MM:SS |
| site_id | int64 | Booking site ID | Which platform (anonymized) |
| srch_destination_id | int64 | Destination numeric ID | Geographic anonymization |

---

### User Context

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| visitor_location_country_id | int64 | Country ID of user | Anonymized |
| visitor_hist_starrating | float64 | User's avg historical rating preference | NaN = new user (no history) |
| visitor_hist_adr_usd | float64 | User's avg historical daily rate (USD) | Historical booking behavior |

---

### Search Parameters

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| srch_length_of_stay | int64 | Night count (checkout - checkin) | 1–30+ nights typical |
| srch_booking_window | int64 | Days advance (checkin - today) | Urgency proxy: 1=last-minute, 365+=advance planner |
| srch_adults_count | int64 | Number of adults | 1–6 typical |
| srch_children_count | int64 | Number of children | 0–4 typical |
| srch_room_count | int64 | Rooms requested | 1–3 typical |
| srch_saturday_night_bool | int64 | Weekend trip? | 1 if checkout includes Saturday |

---

### Property Attributes

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| prop_id | int64 | Unique property identifier | Hotel anonymized |
| prop_country_id | int64 | Property location country ID | Anonymized |
| prop_starrating | int64 | Star rating | 0–5 stars |
| prop_review_score | float64 | Average guest review score | 0.0–5.0 |
| prop_brand_bool | int64 | Is branded chain? | 1=yes (e.g., Marriott), 0=independent |
| prop_location_score1 | float64 | Location relevance to search | Platform-derived scoring |
| prop_location_score2 | float64 | Secondary location relevance | Platform-derived scoring |
| prop_log_historical_price | float64 | Log of historical price | Feature-engineered for modeling |

---

### Pricing & Promotions

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| price_usd | float64 | Final nightly rate shown to user | USD, single currency |
| promotion_flag | int64 | Special promotion active? | 1=promoted deal, 0=regular |
| comp1_rate through comp8_rate | int64 | Competitor 1–8 price comparison (encoded) | **CRITICAL:** +1=Expedia lower, 0=same, -1=Expedia higher (NOT actual prices) |
| comp1_rate_percent_diff through comp8_rate_percent_diff | float64 | % price difference vs competitors | Actual %; Expedia as denominator |

---

### Competitor Inventory

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| comp1_inv through comp8_inv | int64 | Competitor 1–8 availability | +1=competitor no stock, 0=both have stock, NULL=no data |

---

### Engagement & Outcomes

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| click_bool | int64 | User clicked property? | 1=click, 0=no click |
| booking_bool | int64 | User booked property? | 1=booked, 0=not booked |
| gross_bookings_usd | float64 | Revenue from booking | Total USD if booked, NaN if not |

---

### Other Features

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| srch_query_affinity_score | float64 | Search-property relevance | Platform scoring (NaN common) |
| orig_destination_distance | float64 | Distance from origin to destination | Miles/km (NaN for some searches) |
| random_bool | int64 | Random assignment for testing? | 0/1 flag |

---

## Outcome Rates (10,000 row sample)

| Metric | Value |
|--------|-------|
| Total Impressions | 10,000 |
| Clicks | ~2,000–3,000 (20–30%) |
| Bookings | 265 (2.65% of impressions) |
| Click-to-Book Rate | ~13% of clicks convert |
| Revenue per Impression | ~$6 (265 bookings × avg price / 10k impressions) |

---

## Data Quality Notes

### Completeness
- **Full:** srch_id, date_time, site_id, prop_id, price_usd, click_bool, booking_bool, position
- **Mostly Full:** prop_starrating, prop_review_score, srch_booking_window
- **Sparse (>35% NaN):** 
  - visitor_hist_starrating, visitor_hist_adr_usd (new users have no history)
  - comp*_rate (not all searches have 8 competitors shown)
  - srch_query_affinity_score, orig_destination_distance

### Outliers
- **price_usd:** Mean $226, but max $176k (luxury or data error; capped analysis at $1k)
- **competitiveness_score:** High variance (std $3,686) due to extreme outliers

### Anonymization
- All identifiers (srch_id, prop_id, visitor_id, country_id) are numeric codes
- No actual names, addresses, or email addresses
- Dates normalized to 2012–2013 period

---

## Derived Columns (Calculated During Analysis)

| Column | Calculation | Purpose |
|--------|-----------|---------|
| position | Row order within search (already exists) | Ranking position (1st, 2nd, etc.) |
| competitiveness_score | price_usd - avg(comp1_rate...comp8_rate) | Price vs competitor average |
| market_segment | Price percentile + star rating bins | Budget/Mid/Luxury classification |

---

## Comparison: Original Definitions vs. Actual Data

### What's Different

| Original Definition | Actual Data | Why |
|-------------------|-------------|-----|
| visitor_visit_nbr (individual count) | visitor_hist_starrating (aggregate) | Data pre-processed; individual visits removed, aggregate metrics kept |
| price_without_discount_usd + price_with_discount_usd | price_usd (single value) | Discount structure aggregated into final shown price |
| prop_room_capacity | Not present | Removed in preprocessing |
| srch_ci, srch_co (explicit dates) | srch_booking_window, srch_length_of_stay (numeric) | Dates abstracted to numeric values |
| device, mobile_bool, mobile_app | Not present | Device info removed |
| posa_* (point-of-sale details) | site_id (anonymized) | PoS info abstracted to single ID |
| prop_market_id, prop_submarket_id | Not present | Geo hierarchy removed; inferred from price/rating |

### What's New

| Column | Source | Purpose |
|--------|--------|---------|
| click_bool, booking_bool, gross_bookings_usd | Outcome data | Direct measurement of user actions |
| comp*_rate_percent_diff | Derived | Pre-calculated % difference |
| prop_location_score1, prop_location_score2 | Feature engineering | Location relevance scoring |
| prop_log_historical_price | Feature engineering | Price normalization for modeling |
| srch_query_affinity_score | Feature engineering | Search-property match scoring |

---

## Analysis Implications

### What We Can Measure (Because Outcome Data Exists)
✅ Causal impact of ranking position on clicks & bookings  
✅ Price sensitivity and competitiveness elasticity  
✅ Quality signal effectiveness (ratings, reviews)  
✅ User segment differences (new vs returning)  
✅ Funnel friction (impression → click → booking)

### What We Cannot Measure (Due to Anonymization)
❌ Individual property names or actual locations (only IDs)  
❌ Specific geographic markets (only destination IDs)  
❌ Device or mobile impact  
❌ Repeat user behavior (aggregated to averages)  
❌ Detailed discount rules (abstracted to final price)

### What We Can Infer (But Not Directly Measure)
🔄 Market segmentation (from price/rating distribution)  
🔄 Urgency effects (from srch_booking_window)  
🔄 Search relevance (from location scores)  
🔄 Property popularity (from repeat appearances)

---

## Key Constraints for Analysis

1. **Sample Bias:** 10,000 rows from ~10M total; may not represent all booking patterns
2. **Outlier Treatment:** Price outliers ($176k) need capping for meaningful analysis
3. **Sparse Competitor Data:** 35% of rows have no competitor prices; analysis limited to rows with ≥3 competitors
4. **Outcome Imbalance:** 2.65% booking rate; use proportional sampling for class balance in any ML
5. **Temporal Scope:** 2012–2013 only; may not reflect current booking behavior

---

**Last Updated:** 2026-04-18  
**Prepared by:** Claude Code Analysis  
**Status:** Ready for analysis
