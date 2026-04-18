# Expedia Hotel Booking Dataset - Column Definitions

**Source:** Kaggle Expedia Personalized Sort (ICDM 2013) Competition  
**Reference File:** `data/expedia_col_definitions.csv` (authoritative)  
**Dataset:** train.csv, test.csv (full), sample.csv (100k row sample from train)  
**Total Columns:** 54

---

## Search & Session Context (4 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `srch_id` | Integer | The ID of the search |
| `date_time` | Date/time | Date and time of the search |
| `site_id` | Integer | ID of the Expedia point of sale (e.g., Expedia.com, Expedia.co.uk, Expedia.co.jp) |
| `srch_destination_id` | Integer | ID of the destination where the hotel search was performed |

---

## User Profile (3 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `visitor_location_country_id` | Integer | Country ID of the customer (where user is located) |
| `visitor_hist_starrating` | Float | Mean star rating of hotels the customer has previously purchased; NULL = no purchase history |
| `visitor_hist_adr_usd` | Float | Mean price per night (USD) of hotels the customer has previously purchased; NULL = no purchase history (ADR = Average Daily Rate) |

---

## Property Attributes (8 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `prop_id` | Integer | The ID of the hotel |
| `prop_country_id` | Integer | Country ID where hotel is located |
| `prop_starrating` | Integer | Star rating of hotel (1–5); 0 = no stars / unknown / cannot be publicized |
| `prop_review_score` | Float | Mean customer review score (0–5), rounded to 0.5 increments; 0 = no reviews; NULL = unavailable |
| `prop_brand_bool` | Integer | Brand hotel indicator: +1 = major hotel chain, 0 = independent |
| `prop_location_score1` | Float | Location desirability score (first) |
| `prop_location_score2` | Float | Location desirability score (second) |
| `prop_log_historical_price` | Float | Logarithm of mean historical price; 0 = not sold in period |

---

## Search Parameters (7 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `srch_length_of_stay` | Integer | Number of nights stay that was searched |
| `srch_booking_window` | Integer | Number of days in the future from search date to hotel stay (booking urgency proxy) |
| `srch_adults_count` | Integer | Number of adults specified in the hotel room |
| `srch_children_count` | Integer | Number of (extra occupancy) children specified in the hotel room |
| `srch_room_count` | Integer | Number of hotel rooms specified in the search |
| `srch_saturday_night_bool` | Boolean | +1 if stay includes Saturday night AND (starts Thursday OR ≤4 night stay); else 0 |
| `srch_query_affinity_score` | Float | Log of the probability a hotel will be clicked on in Internet searches (NULL = no data; negative values) |

---

## Price & Promotions (3 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `price_usd` | Float | Displayed price of hotel for the given search. Note: different countries have different conventions regarding taxes, fees, per-night vs total stay |
| `promotion_flag` | Integer | +1 if hotel had a sale price promotion specifically displayed; 0 = regular price |
| `gross_booking_usd` | Float | **[Outcome]** Total value of transaction if booked. May differ from `price_usd` due to taxes, fees, room type changes, or multi-night conventions |

---

## Ranking & Display (2 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `position` | Integer | Hotel position on Expedia's search results page. **Training data only**; not in test data |
| `random_bool` | Boolean | +1 when displayed sort was random; 0 when normal sort order was displayed |

---

## Location & Distance (1 column)

| Column | Type | Definition |
|--------|------|-----------|
| `orig_destination_distance` | Float | Physical distance between user and hotel at search time; NULL = distance could not be calculated |

---

## Competitor Data (24 columns: comp1–comp8, each with 3 fields)

For each competitor (1–8):

### `comp*_rate` (Price Direction Encoding)

| Value | Meaning |
|-------|---------|
| +1 | Expedia has **lower** price than competitor |
| 0 | Same price as competitor |
| -1 | Expedia's price is **higher** than competitor |
| NULL | No competitive data available |

### `comp*_inv` (Availability)

| Value | Meaning |
|-------|---------|
| +1 | Competitor does **NOT** have availability |
| 0 | Both Expedia and competitor have availability |
| NULL | No competitive data available |

### `comp*_rate_percent_diff` (Price Difference %)

| Value | Meaning |
|-------|---------|
| Float | Absolute percentage difference between Expedia and competitor price (Expedia = denominator) |
| NULL | No competitive data available |

**Columns:** `comp1_rate`, `comp1_inv`, `comp1_rate_percent_diff` ... `comp8_rate`, `comp8_inv`, `comp8_rate_percent_diff`

---

## Outcome Variables (2 columns)

| Column | Type | Definition |
|--------|------|-----------|
| `click_bool` | Integer (0/1) | **[Outcome]** User clicked on hotel: 1 = click, 0 = no click |
| `booking_bool` | Integer (0/1) | **[Outcome]** User booked hotel: 1 = booked, 0 = not booked |

---

## Critical Notes

### Price Encoding

⚠️ **`comp*_rate` columns are NOT actual prices.** They encode direction only:
- Use `comp*_rate` for: price direction (+1 = Expedia lower, -1 = higher)
- Use `comp*_rate_percent_diff` for: actual percentage price differences
- There is NO `comp*_actual_price` column

### Outcome Data Availability

✅ **Click, booking, and revenue outcome data IS available** in training data:
- `click_bool`: Direct measurement of user clicks
- `booking_bool`: Direct measurement of conversions
- `gross_booking_usd`: Revenue from successful bookings

This enables **causal measurement** of ranking, pricing, and quality signal impact on conversions.

### Missing Data Conventions

| Column | NULL Meaning |
|--------|--------------|
| `visitor_hist_starrating`, `visitor_hist_adr_usd` | New user with no purchase history |
| `prop_review_score` | Review info unavailable (distinct from 0 = no reviews) |
| `srch_query_affinity_score` | Hotel never appeared in any Internet searches |
| `orig_destination_distance` | Distance calculation not possible |
| `comp*_*` | No competitive intelligence for that competitor in that search |

---

**Last Updated:** 2026-04-18  
**Authoritative Source:** `data/expedia_col_definitions.csv`
