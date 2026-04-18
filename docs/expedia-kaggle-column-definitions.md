# Expedia Personalized Sort (ICDM 2013) - Column Definitions

**Source:** Kaggle Expedia Personalized Sort Competition  
**Dataset:** Hotel search results with user click/booking outcomes  
**Link:** https://www.kaggle.com/c/expedia-personalized-sort/data

---

## Column Reference

### Search & Session Context

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `srch_id` | Integer | The ID of the search | Links all hotels shown in one search result |
| `date_time` | Date/time | Date and time of the search | Timestamp when user performed search |
| `site_id` | Integer | ID of the Expedia point of sale | e.g., Expedia.com, Expedia.co.uk, Expedia.co.jp |

---

### User Profile

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `visitor_location_country_id` | Integer | Country ID of the customer | Where user is located |
| `visitor_hist_starrating` | Float | Mean star rating of hotels user previously purchased | NULL = no purchase history |
| `visitor_hist_adr_usd` | Float | Mean price per night (USD) of previously purchased hotels | NULL = no purchase history; ADR = Average Daily Rate |

---

### Property Attributes

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `prop_id` | Integer | The ID of the hotel | Hotel identifier |
| `prop_country_id` | Integer | Country ID where hotel is located | Geographic location |
| `prop_starrating` | Integer | Star rating of hotel (1–5) | 0 = no stars / unknown / cannot be publicized |
| `prop_review_score` | Float | Mean customer review score (0–5) | Rounded to 0.5 increments; 0 = no reviews; NULL = info unavailable |
| `prop_brand_bool` | Integer | Brand hotel indicator | 1 = major hotel chain; 0 = independent |
| `prop_location_score1` | Float | Location desirability score (first) | Platform-derived metric |
| `prop_location_score2` | Float | Location desirability score (second) | Platform-derived metric |
| `prop_log_historical_price` | Float | Log of mean historical price | 0 = not sold in period |

---

### Search Parameters

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `srch_destination_id` | Integer | Destination ID where search was performed | Geographic search target |
| `srch_length_of_stay` | Integer | Number of nights stay searched | Trip duration |
| `srch_booking_window` | Integer | Days in future from search to hotel stay | Booking urgency proxy; 1 = same day, 365+ = advance booking |
| `srch_adults_count` | Integer | Number of adults specified | Group composition |
| `srch_children_count` | Integer | Number of (extra occupancy) children specified | Extra occupancy children only |
| `srch_room_count` | Integer | Number of rooms specified in search | Group size accommodation |
| `srch_saturday_night_bool` | Boolean | Weekend trip indicator | 1 if stay includes Saturday night AND (starts Thursday OR ≤4 night stay); else 0 |

---

### Price & Promotions

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `price_usd` | Float | Displayed price of hotel for search | **Important:** May include/exclude taxes & fees depending on country; per night or total stay |
| `promotion_flag` | Integer | Sale price promotion indicator | 1 = special promotion displayed; 0 = regular price |
| `gross_booking_usd` | Float | Total transaction value if booked | **Outcome:** May differ from price_usd due to taxes, fees, room type changes, multi-day conventions |

---

### Ranking & Display

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `position` | Integer | Hotel position on search results page | **Training data only**; not provided in test data |
| `random_bool` | Boolean | Random sort indicator | 1 = random sort displayed; 0 = normal sort order |

---

### Location & Distance

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `orig_destination_distance` | Float | Physical distance from user to hotel | NULL = distance could not be calculated |
| `srch_query_affinity_score` | Float | Log probability of hotel click in internet searches | NULL = no data; negative values (log scale) |

---

## Competitor Data (comp1 through comp8)

Eight competitors are tracked. Data exists for up to 8 different OTA competitors per hotel per search.

### comp*_rate (Price Comparison)

| Value | Meaning |
|-------|---------|
| +1 | Expedia has lower price than competitor |
| 0 | Same price as competitor |
| -1 | Expedia's price is higher than competitor |
| NULL | No competitive data available |

### comp*_inv (Inventory/Availability)

| Value | Meaning |
|-------|---------|
| +1 | Competitor does NOT have availability |
| 0 | Both Expedia and competitor have availability |
| NULL | No competitive data available |

### comp*_rate_percent_diff (Price Difference %)

| Value | Meaning |
|-------|---------|
| Float | Absolute percentage difference between Expedia and competitor price (Expedia = denominator) |
| NULL | No competitive data available |

**Columns:** comp1_rate, comp1_inv, comp1_rate_percent_diff, ... comp8_rate, comp8_inv, comp8_rate_percent_diff

---

## Outcome Variables (Target)

| Column | Type | Definition | Notes |
|--------|------|-----------|-------|
| `click_bool` | Integer (0/1) | User clicked on hotel | 1 = click; 0 = no click |
| `booking_bool` | Integer (0/1) | User booked hotel | 1 = booked; 0 = not booked |

---

## Key Data Notes

### Missingness & Special Values

- **Visitor History (visitor_hist_*):** NULL indicates new user with no prior purchase history
- **Review Score:** 0 = no reviews; NULL = info not available
- **Star Rating:** 0 = property not rated / unknown / cannot be publicized
- **Competitor Data:** NULL = no competitive intelligence for that competitor in that search
- **Affinity Score:** NULL = hotel never appeared in any internet searches
- **Distance:** NULL = distance calculation not possible

### Important Caveat: Price Encoding

⚠️ **CRITICAL:** `comp*_rate` columns are NOT actual prices. They are encoded as:
- **+1, 0, or -1** (price comparison direction)
- Use `comp*_rate_percent_diff` for actual percentage difference
- There is NO `comp*_actual_price` column in the dataset

### Data Collection & Conventions

- **International Pricing:** Different countries have different conventions for displaying taxes, fees, and per-night vs total-stay pricing
- **Transaction Value:** `gross_booking_usd` may differ from `price_usd` due to:
  - Taxes and fees
  - Country pricing conventions
  - Room type changes (user booked different room than shown)
  - Multi-night booking conventions

### Training vs Test Data

- **Position:** Only available in training data; test data has no position values
- **Outcomes:** Only available in training data (click_bool, booking_bool, gross_booking_usd)

---

## Quick Reference: 54 Total Columns

**Search Context (4):** srch_id, date_time, site_id, srch_destination_id  
**User (3):** visitor_location_country_id, visitor_hist_starrating, visitor_hist_adr_usd  
**Property (8):** prop_id, prop_country_id, prop_starrating, prop_review_score, prop_brand_bool, prop_location_score1, prop_location_score2, prop_log_historical_price  
**Search Params (7):** srch_length_of_stay, srch_booking_window, srch_adults_count, srch_children_count, srch_room_count, srch_saturday_night_bool, srch_query_affinity_score  
**Price & Promo (3):** price_usd, promotion_flag, gross_booking_usd  
**Ranking & Display (2):** position, random_bool  
**Location (1):** orig_destination_distance  
**Competitor Data (24):** comp1–8: rate, inv, rate_percent_diff  
**Outcomes (2):** click_bool, booking_bool  

---

## Historical Context

**Competition:** ICDM 2013 (IEEE International Conference on Data Mining)  
**Task:** Personalize hotel search ranking to improve conversion (clicks → bookings)  
**Time Period:** Data from 2012–2013  
**Scale:** ~10M rows (full dataset); this analysis uses 100k row sample

---

**Document Generated:** 2026-04-18  
**Reference:** Kaggle Expedia Personalized Sort Competition
