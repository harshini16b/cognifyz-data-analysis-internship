# 🍽️ Cognifyz Technologies — Data Analysis Internship

![Cognifyz](https://img.shields.io/badge/Cognifyz-Data%20Analysis%20Internship-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

## 📌 About This Project

This repository contains my complete submission for the **Cognifyz Technologies Data Analysis Internship Program**.

The dataset used is a restaurant dataset with **9,551 restaurants** and **21 features** including cuisine types, city locations, ratings, votes, price ranges, and service availability.

All three levels have been completed across **11 tasks** covering exploratory data analysis, statistical insights, and data visualization.

---

## 📁 Repository Structure

```
cognifyz-data-analysis-internship/
│
├── Dataset_.csv                  # Original dataset
│
├── Level1/
│   ├── Level1_Tasks.py           # Python code for all Level 1 tasks
│   └── Level1_Analysis.png       # Output charts
│
├── Level2/
│   ├── Level2_Tasks.py           # Python code for all Level 2 tasks
│   └── Level2_Analysis.png       # Output charts
│
├── Level3/
│   ├── Level3_Tasks.py           # Python code for all Level 3 tasks
│   └── Level3_Analysis.png       # Output charts
│
└── README.md                     # This file
```

---

## 📊 Level 1 — Exploratory Analysis

### Task 1 — Top Cuisines
- Identified the **top 3 most common cuisines** across 9,551 restaurants
- Calculated the percentage of restaurants serving each cuisine

| Rank | Cuisine | Count | % |
|------|---------|-------|---|
| 🥇 1 | North Indian | 3,960 | 41.46% |
| 🥈 2 | Chinese | 2,735 | 28.64% |
| 🥉 3 | Fast Food | 1,986 | 20.79% |

### Task 2 — City Analysis
- **City with most restaurants:** New Delhi (5,473 restaurants)
- **City with highest average rating:** Inner City (avg 4.90 / 5)
- Analyzed top 10 cities by both count and average rating

### Task 3 — Price Range Distribution
- Created bar chart and pie chart of price range distribution
- Nearly **46.5%** of restaurants fall in the lowest price range (Range 1)

| Range | Label | % |
|-------|-------|---|
| 1 | Low | 46.53% |
| 2 | Medium | 32.59% |
| 3 | High | 14.74% |
| 4 | Very High | 6.14% |

### Task 4 — Online Delivery
- **25.66%** of restaurants offer online delivery
- Restaurants **with** delivery have a higher avg rating (3.25 vs 2.47)

---

## 📊 Level 2 — Intermediate Analysis

### Task 1 — Restaurant Ratings
- Most common rating range: **3–4** (45.94% of restaurants)
- Average votes per restaurant: **156.91**
- Analyzed full rating distribution with histogram

### Task 2 — Cuisine Combinations
- Most common combination: **North Indian + Chinese** (616 restaurants)
- Burger + Fast Food combinations had the **highest average rating (3.30)**

### Task 3 — Geographic Analysis
- Plotted **9,052 restaurants** on a world scatter map using coordinates
- **Key clusters:** Massive concentration in New Delhi, India; secondary cluster in Philippines

### Task 4 — Restaurant Chains
- **734 restaurant chains** identified (names appearing more than once)
- Largest chain: **Cafe Coffee Day** (83 outlets)
- Best rated chain: **Barbeque Nation** (avg 4.35 ⭐)

---

## 📊 Level 3 — Advanced Analysis

### Task 1 — Restaurant Reviews
- Analyzed `Rating text` sentiment distribution (Excellent → Poor)
- "Excellent" rated restaurants get **18x more votes** than "Average" ones
- Strong alignment between rating text labels and aggregate scores confirmed

### Task 2 — Votes Analysis
- **Highest votes:** Toit, Bangalore — 10,934 votes (★ 4.8)
- **Pearson correlation** between votes and rating: **r = 0.31** (moderate positive)
- Clear trend: more votes → consistently higher ratings

| Votes Bucket | Avg Rating |
|---|---|
| 0–50 | 2.39 |
| 51–200 | 3.51 |
| 201–500 | 3.88 |
| 501–1000 | 4.08 |
| 1000+ | 4.20 |

### Task 3 — Price Range vs Services
- **Online Delivery** peaks at Range 2 / Medium priced restaurants (41.3%)
- **Table Booking** peaks at Range 4 / Very High priced restaurants (46.8%)
- Budget restaurants almost never offer Table Booking (0.0% at Range 1)
- **Conclusion:** Higher price → Table Booking; Mid-range → Online Delivery

---

## 🛠️ Libraries Used

```python
import pandas as pd         # Data loading and manipulation
import numpy as np          # Numerical operations
import matplotlib.pyplot as plt   # Visualizations
from collections import Counter   # Counting cuisine combinations
```

---

## ▶️ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cognifyz-data-analysis-internship.git
   cd cognifyz-data-analysis-internship
   ```

2. Install required libraries:
   ```bash
   pip install pandas numpy matplotlib
   ```

3. Run any level:
   ```bash
   cd Level1
   python Level1_Tasks.py

   cd ../Level2
   python Level2_Tasks.py

   cd ../Level3
   python Level3_Tasks.py
   ```

> ⚠️ Make sure `Dataset_.csv` is in the same folder as the script you're running, or update the file path inside the script.

---

## 📈 Key Takeaways

- **North Indian cuisine** dominates the restaurant landscape
- **New Delhi** is the restaurant capital of the dataset
- Restaurants with **online delivery** are rated higher by customers
- **More votes = higher ratings** (r = 0.31 correlation)
- **Premium restaurants** prefer table booking; budget restaurants prefer delivery
- **Barbeque Nation** is the highest-rated restaurant chain (4.35 avg)

---

## 🏢 About Cognifyz Technologies

Cognifyz Technologies is a leading technology company specializing in data science, AI, and machine learning. This internship program provided hands-on experience with real-world restaurant data.

🔗 [www.cognifyz.com](https://www.cognifyz.com) | 📧 contact@cognifyz.com

---

*#cognifyz #cognifyzTech #cognifyzTechnologies #DataAnalysis #Python #Internship*
