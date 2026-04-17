# 🧭 Project Brief: Travel Marketplace System Analysis

## 🏷️ Title
**Diagnosing and Improving a Travel Booking System: A Data-Driven Case Study**

---

## 🧠 1. Overview

This project analyzes a real-world hotel search dataset to understand how users make booking decisions within a competitive marketplace.

It focuses on identifying:
- Where users drop off in the booking journey
- How platform mechanics (ranking, pricing, exposure) influence outcomes
- Where inefficiencies exist for both customers and hotel partners

---

## 🎯 2. Objective

To diagnose inefficiencies in a travel booking system and propose improvements that:

- Increase booking conversion
- Improve partner (hotel) performance
- Reduce operational friction and cost-to-serve
- Enable better decision-making through data and tooling

---

## 🧩 3. System Context

Each search represents a competitive environment:
Search → Ranked Hotels → Click → Booking

- Each row = one hotel competing within a search
- Hotels compete on:
  - Price
  - Trust signals (reviews, ratings)
  - Visibility (ranking position)

---

## 👥 4. Stakeholders

### Customers
- Want relevant, trustworthy, and well-priced options

### Partners (Hotels)
- Want visibility and bookings
- Limited insight into competitiveness

### Platform (Agoda-like system)
- Optimizes for conversion, efficiency, and revenue

---

## 📥 5. Inputs

### Dataset Features

#### Search Context
- `srch_id`, dates, number of guests
- booking window, length of stay

#### Property Attributes
- `price_usd`
- `prop_review_score`, `prop_starrating`
- `prop_brand_bool`

#### User Context
- `visitor_visit_nbr`
- historical preferences

#### Competition Data
- competitor price signals

#### Outcomes
- `click_bool`
- `booking_bool`

---

## 📤 6. Outputs

### Primary
- Consultant-style slide deck (12–15 slides)

### Secondary
- Blog post (article format with visualizations)

### Optional
- Supporting analysis notebook

---

## 🔍 7. Target Insights

### 1. Funnel Friction
- Where users drop off (click vs booking)

### 2. Ranking Bias
- How position affects visibility and clicks

### 3. Price Competitiveness
- Relative price vs competitors drives booking

### 4. Trust Signals
- Reviews and ratings influence decisions

### 5. User Segmentation
- Different behaviors across user types

### 6. System Inefficiencies
- Competitive hotels underexposed due to ranking

---

## ⚙️ 8. Methodology (With Claude)

### Step 1 — Data Understanding
- Explore dataset structure
- Define hypotheses

**Claude Role:**
- Categorize variables
- Suggest hypotheses

---

### Step 2 — Funnel Analysis
- Compute CTR, booking rate, post-click conversion

**Goal:**
- Identify where friction occurs

---

### Step 3 — Ranking Analysis
- Analyze click rate vs position

**Goal:**
- Understand visibility bias

---

### Step 4 — Pricing Analysis
- Create price competitiveness metric
- Analyze booking vs relative price

**Goal:**
- Understand decision drivers

---

### Step 5 — Trust Signals
- Analyze reviews, ratings, brand

**Goal:**
- Compare trust vs price influence

---

### Step 6 — User Segmentation
- Analyze returning vs new users
- Analyze booking window (urgency)

---

### Step 7 — Identify Inefficiencies
- Detect:
  - low-ranked but high-performing hotels

---

### Step 8 — Synthesis
- Group insights into core system problems

---

### Step 9 — Recommendations
Generate:
- Process improvements
- Partner-facing tools
- Automation opportunities

---

## 🤖 9. Claude Usage Strategy

Claude is used to:
- Suggest analysis approaches
- Interpret results
- Refine insights into business language
- Generate structured outputs (deck, blog)

User retains control over:
- Analysis logic
- Insight validation
- Narrative direction

---

## 📊 10. Key Visualizations

### Core Charts

1. Funnel Chart
   - Impression → Click → Booking

2. Position vs Click Rate
   - Line chart

3. Price vs Booking Rate
   - Line or scatter

4. Price Difference vs Booking Rate
   - Shows competitiveness

5. Review Score vs Booking Rate
   - Trust impact

6. Booking Rate by Segment
   - Bar chart

7. Position vs Performance Scatter
   - Highlights inefficiencies

---

## 🧱 11. Deck Structure

1. Title  
2. Executive Summary  
3. Problem Definition  
4. System Overview  
5. Funnel Analysis  
6. Ranking Bias  
7. Pricing Impact  
8. Trust Signals  
9. User Behavior  
10. System Inefficiencies  
11. Recommendations  
12. Business Impact  

---

## 🧩 12. Key Recommendations (Expected)

### Partner Tools
- Pricing competitiveness dashboard
- Performance alerts

### Process Improvements
- Ranking logic refinement
- Better exposure allocation

### Automation / AI
- Price recommendations
- Underperformance detection

---

## 💼 13. Relevance to Partner Excellence Role

This project demonstrates:

### Partner Experience (PX)
- Identifies how system design impacts hotel performance

### Process Optimization
- Diagnoses inefficiencies in ranking and exposure

### Automation & Tooling
- Proposes scalable partner tools and alerts

### Cost-to-Serve Reduction
- Enables self-service insights → reduces support load

### Cross-functional Thinking
- Connects data → product → operations → business impact

---

## ⏱️ 14. Timeline

### Week 1 — Analysis
- Funnel, pricing, ranking, segmentation

### Week 2 — Output
- Deck creation
- Blog writing

---

## ✍️ 15. Blog Direction

### Title
**What Makes People Book Hotels? A Data-Driven Look at Pricing, Ranking, and Decision Behavior**

### Structure
1. The system  
2. Where users drop off  
3. Why price matters  
4. Why ranking matters  
5. What platforms get wrong  
6. What should change  

---

## 💡 16. Final Positioning

This project demonstrates:

> The ability to analyze complex systems, identify friction points, and design scalable improvements across customer experience, partner performance, and operational efficiency.