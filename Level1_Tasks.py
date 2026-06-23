"""
Cognifyz Technologies – Data Analysis Internship
Level 1 – All Tasks (1 to 4)
Author  : [Your Name]
Dataset : Dataset_.csv  (9551 restaurants, 21 columns)
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')          # headless / no display needed
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# ──────────────────────────────────────────────
# Load dataset
# ──────────────────────────────────────────────
df = pd.read_csv('Dataset_.csv')
total = len(df)
print(f"Dataset loaded: {total} rows, {df.shape[1]} columns\n")


# ══════════════════════════════════════════════
# LEVEL 1 – TASK 1: TOP CUISINES
# ══════════════════════════════════════════════
print("=" * 50)
print("TASK 1: TOP CUISINES")
print("=" * 50)

# Each restaurant may list multiple cuisines separated by commas
all_cuisines = []
for entry in df['Cuisines'].dropna():
    for cuisine in entry.split(','):
        all_cuisines.append(cuisine.strip())

cuisine_counts = Counter(all_cuisines)
top3 = cuisine_counts.most_common(3)

print(f"\nTop 3 Most Common Cuisines:")
for rank, (name, count) in enumerate(top3, 1):
    pct = count / total * 100
    print(f"  {rank}. {name}: {count} restaurants ({pct:.2f}%)")


# ══════════════════════════════════════════════
# LEVEL 1 – TASK 2: CITY ANALYSIS
# ══════════════════════════════════════════════
print("\n" + "=" * 50)
print("TASK 2: CITY ANALYSIS")
print("=" * 50)

# City with the highest number of restaurants
city_counts = df['City'].value_counts()
top_city       = city_counts.idxmax()
top_city_count = city_counts.max()
print(f"\nCity with most restaurants : {top_city}  ({top_city_count} restaurants)")

# Average rating per city
city_avg_rating = df.groupby('City')['Aggregate rating'].mean()
best_rated_city = city_avg_rating.idxmax()
best_rating_val = city_avg_rating.max()
print(f"City with highest avg rating: {best_rated_city}  (avg {best_rating_val:.2f})")

print("\nTop 10 Cities by Restaurant Count:")
print(city_counts.head(10).to_string())

print("\nTop 10 Cities by Average Rating:")
print(city_avg_rating.sort_values(ascending=False).head(10).round(2).to_string())


# ══════════════════════════════════════════════
# LEVEL 1 – TASK 3: PRICE RANGE DISTRIBUTION
# ══════════════════════════════════════════════
print("\n" + "=" * 50)
print("TASK 3: PRICE RANGE DISTRIBUTION")
print("=" * 50)

price_counts = df['Price range'].value_counts().sort_index()
price_labels = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}

print("\nPrice Range Breakdown:")
for pr in [1, 2, 3, 4]:
    pct = price_counts[pr] / total * 100
    print(f"  Range {pr} ({price_labels[pr]:9s}): {price_counts[pr]:5d} restaurants  ({pct:.2f}%)")


# ══════════════════════════════════════════════
# LEVEL 1 – TASK 4: ONLINE DELIVERY
# ══════════════════════════════════════════════
print("\n" + "=" * 50)
print("TASK 4: ONLINE DELIVERY")
print("=" * 50)

delivery_counts = df['Has Online delivery'].value_counts()
pct_yes = delivery_counts.get('Yes', 0) / total * 100
pct_no  = delivery_counts.get('No',  0) / total * 100

avg_with    = df[df['Has Online delivery'] == 'Yes']['Aggregate rating'].mean()
avg_without = df[df['Has Online delivery'] == 'No' ]['Aggregate rating'].mean()

print(f"\nRestaurants WITH    online delivery: {delivery_counts.get('Yes',0):5d}  ({pct_yes:.2f}%)")
print(f"Restaurants WITHOUT online delivery: {delivery_counts.get('No', 0):5d}  ({pct_no:.2f}%)")
print(f"\nAverage rating – WITH    delivery : {avg_with:.2f}")
print(f"Average rating – WITHOUT delivery : {avg_without:.2f}")
diff = avg_with - avg_without
print(f"Difference                         : +{diff:.2f} in favour of restaurants with delivery")


# ══════════════════════════════════════════════
# COMBINED VISUALISATION  (8 sub-plots)
# ══════════════════════════════════════════════
COLORS = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
          '#1abc9c', '#e67e22', '#34495e', '#e91e63', '#00bcd4']

fig = plt.figure(figsize=(20, 22), facecolor='#f8f9fa')
fig.suptitle('Cognifyz Data Analysis Internship\nLevel 1 – Complete Task Results',
             fontsize=22, fontweight='bold', color='#2c3e50', y=0.98)

# ── Task 1: Horizontal bar ──
ax1 = fig.add_subplot(4, 2, (1, 2))
t1_names  = [x[0] for x in top3]
t1_counts = [x[1] for x in top3]
t1_pcts   = [x[1] / total * 100 for x in top3]
bars = ax1.barh(t1_names[::-1], t1_counts[::-1],
                color=['#3498db', '#2ecc71', '#e74c3c'], height=0.5, edgecolor='white')
ax1.set_title('Task 1: Top 3 Cuisines', fontsize=16, fontweight='bold', color='#2c3e50', pad=12)
ax1.set_xlabel('Number of Restaurants', fontsize=12)
ax1.set_facecolor('#ffffff')
for bar, pct in zip(bars, t1_pcts[::-1]):
    w = bar.get_width()
    ax1.text(w + 30, bar.get_y() + bar.get_height() / 2,
             f'{w:,}  ({pct:.1f}%)', va='center', fontsize=12,
             color='#2c3e50', fontweight='bold')
ax1.set_xlim(0, max(t1_counts) * 1.25)
ax1.spines[['top', 'right', 'left']].set_visible(False)
ax1.tick_params(left=False)
ax1.set_yticklabels(t1_names[::-1], fontsize=13)

# ── Task 2A: Restaurants per city ──
ax2a = fig.add_subplot(4, 2, 3)
top10_cities = city_counts.head(10)
ax2a.bar(range(len(top10_cities)), top10_cities.values,
         color=COLORS[:10], edgecolor='white', linewidth=0.8)
ax2a.set_title('Task 2A: Top 10 Cities by\nRestaurant Count',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax2a.set_xticks(range(len(top10_cities)))
ax2a.set_xticklabels(top10_cities.index, rotation=45, ha='right', fontsize=8)
ax2a.set_ylabel('No. of Restaurants', fontsize=10)
ax2a.set_facecolor('#ffffff')
ax2a.spines[['top', 'right']].set_visible(False)
for i, v in enumerate(top10_cities.values):
    ax2a.text(i, v + 30, f'{v:,}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')

# ── Task 2B: Average rating per city ──
ax2b = fig.add_subplot(4, 2, 4)
top10_rated = city_avg_rating.sort_values(ascending=False).head(10)
ax2b.bar(range(len(top10_rated)), top10_rated.values,
         color=COLORS[:10], edgecolor='white', linewidth=0.8)
ax2b.set_title('Task 2B: Top 10 Cities by\nAverage Rating',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax2b.set_xticks(range(len(top10_rated)))
ax2b.set_xticklabels(top10_rated.index, rotation=45, ha='right', fontsize=7.5)
ax2b.set_ylabel('Average Rating', fontsize=10)
ax2b.set_ylim(0, 5.5)
ax2b.set_facecolor('#ffffff')
ax2b.spines[['top', 'right']].set_visible(False)
for i, v in enumerate(top10_rated.values):
    ax2b.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

# ── Task 3A: Price range bar chart ──
bar_colors3 = ['#2ecc71', '#3498db', '#e67e22', '#e74c3c']
x_labels3   = ['Low\n(Range 1)', 'Medium\n(Range 2)', 'High\n(Range 3)', 'Very High\n(Range 4)']

ax3a = fig.add_subplot(4, 2, 5)
bars3 = ax3a.bar(x_labels3, price_counts.values, color=bar_colors3,
                 edgecolor='white', linewidth=0.8)
ax3a.set_title('Task 3A: Price Range Distribution\n(Bar Chart)',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax3a.set_ylabel('Number of Restaurants', fontsize=10)
ax3a.set_facecolor('#ffffff')
ax3a.spines[['top', 'right']].set_visible(False)
for bar, pct in zip(bars3, (price_counts / total * 100).values):
    ax3a.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 30,
              f'{int(bar.get_height()):,}\n({pct:.1f}%)',
              ha='center', va='bottom', fontsize=10, fontweight='bold')
ax3a.set_ylim(0, max(price_counts.values) * 1.2)

# ── Task 3B: Price range pie chart ──
ax3b = fig.add_subplot(4, 2, 6)
wedges, texts, autotexts = ax3b.pie(
    price_counts.values, labels=x_labels3,
    autopct='%1.1f%%', colors=bar_colors3,
    explode=(0.05,) * 4, startangle=90,
    textprops={'fontsize': 10})
for at in autotexts:
    at.set_fontweight('bold')
ax3b.set_title('Task 3B: Price Range Distribution\n(Pie Chart)',
               fontsize=13, fontweight='bold', color='#2c3e50')

# ── Task 4A: Delivery availability pie ──
ax4a = fig.add_subplot(4, 2, 7)
ax4a.pie([pct_yes, pct_no],
         labels=[f'With Delivery\n({pct_yes:.1f}%)', f'Without Delivery\n({pct_no:.1f}%)'],
         colors=['#2ecc71', '#e74c3c'],
         autopct='%1.1f%%', startangle=90,
         explode=(0.05, 0), textprops={'fontsize': 10})
ax4a.set_title('Task 4A: Online Delivery\nAvailability',
               fontsize=13, fontweight='bold', color='#2c3e50')

# ── Task 4B: Rating comparison bar ──
ax4b = fig.add_subplot(4, 2, 8)
cats4 = ['With Online Delivery', 'Without Online Delivery']
avgs4 = [avg_with, avg_without]
bars4 = ax4b.bar(cats4, avgs4, color=['#2ecc71', '#e74c3c'],
                 edgecolor='white', linewidth=0.8, width=0.4)
ax4b.set_title('Task 4B: Avg Rating – With vs\nWithout Online Delivery',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax4b.set_ylabel('Average Rating', fontsize=10)
ax4b.set_ylim(0, 5)
ax4b.set_facecolor('#ffffff')
ax4b.spines[['top', 'right']].set_visible(False)
for bar, val in zip(bars4, avgs4):
    ax4b.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
              f'{val:.2f}', ha='center', va='bottom',
              fontsize=13, fontweight='bold', color='#2c3e50')
ax4b.tick_params(axis='x', labelsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.96], h_pad=3.5, w_pad=2.5)
plt.savefig('Level1_Analysis.png', dpi=150, bbox_inches='tight', facecolor='#f8f9fa')
print("\nChart saved as Level1_Analysis.png")
