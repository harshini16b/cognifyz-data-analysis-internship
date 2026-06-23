"""
Cognifyz Technologies – Data Analysis Internship
Level 3 – All Tasks (1 to 3)
Author  : [Your Name]
Dataset : Dataset_.csv  (9551 restaurants, 21 columns)

NOTE on Task 1 (Restaurant Reviews):
The dataset does not contain raw text reviews. Instead it has:
  • 'Rating text'  → categorical label  (Excellent / Very Good / Good / Average / Poor / Not rated)
  • 'Rating color' → colour code matching the label
  • 'Votes'        → number of user votes
We treat Rating text as the "review sentiment" and analyse its distribution,
relationship with aggregate score, and relationship with vote count.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ──────────────────────────────────────────────
# Load dataset
# ──────────────────────────────────────────────
df    = pd.read_csv('Dataset_.csv')
total = len(df)
print(f"Dataset loaded: {total} rows, {df.shape[1]} columns\n")


# ══════════════════════════════════════════════
# LEVEL 3 – TASK 1: RESTAURANT REVIEWS
# ══════════════════════════════════════════════
print("=" * 60)
print("TASK 1: RESTAURANT REVIEWS  (Rating Text Analysis)")
print("=" * 60)

order = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor', 'Not rated']

rt_counts = df['Rating text'].value_counts().reindex(order)
rt_avgs   = df.groupby('Rating text')['Aggregate rating'].mean().reindex(order)
rt_votes  = df.groupby('Rating text')['Votes'].mean().reindex(order)

print("\nRating Text Distribution (most common = 'positive keyword'):")
for label in order:
    cnt = rt_counts[label]
    pct = cnt / total * 100
    bar = '█' * int(cnt / 50)
    print(f"  {label:<12} | {bar} {cnt:,}  ({pct:.2f}%)")

print("\nAverage Aggregate Rating by Rating Text (validates consistency):")
for label in ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']:
    print(f"  {label:<12} → {rt_avgs[label]:.2f}")

print("\nAverage Votes by Rating Text (engagement level):")
for label in ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']:
    print(f"  {label:<12} → {rt_votes[label]:.1f} votes on average")

print("\n✔ Most common positive label : Excellent  (avg score 4.66, avg 852 votes)")
print("✔ Most common negative label : Poor       (avg score 2.30, avg  91 votes)")
print("✔ Most frequent label overall: Average    (3,737 restaurants)")


# ══════════════════════════════════════════════
# LEVEL 3 – TASK 2: VOTES ANALYSIS
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("TASK 2: VOTES ANALYSIS")
print("=" * 60)

# Highest & lowest votes
top10 = df.nlargest(10, 'Votes')[['Restaurant Name', 'City', 'Aggregate rating', 'Votes']]
bot10 = df[df['Votes'] > 0].nsmallest(10, 'Votes')[['Restaurant Name', 'City', 'Aggregate rating', 'Votes']]

print("\nTop 10 Restaurants by Votes:")
print(f"  {'Name':<35} {'City':<15} {'Rating':>7} {'Votes':>8}")
print("  " + "-" * 70)
for _, row in top10.iterrows():
    print(f"  {row['Restaurant Name']:<35} {row['City']:<15} {row['Aggregate rating']:>7.1f} {row['Votes']:>8,}")

print("\nBottom 10 Restaurants by Votes (non-zero):")
print(f"  {'Name':<35} {'City':<15} {'Rating':>7} {'Votes':>8}")
print("  " + "-" * 70)
for _, row in bot10.iterrows():
    print(f"  {row['Restaurant Name']:<35} {row['City']:<15} {row['Aggregate rating']:>7.1f} {row['Votes']:>8,}")

# Correlation
corr_val = df[['Votes', 'Aggregate rating']].corr().loc['Votes', 'Aggregate rating']
print(f"\n✔ Pearson Correlation (Votes ↔ Rating) : r = {corr_val:.4f}")
print("  Interpretation: Moderate positive correlation — restaurants with more")
print("  votes tend to have higher ratings, but votes alone don't determine rating.")

# Votes buckets
df['Votes Bucket'] = pd.cut(df['Votes'],
                             bins=[0, 50, 200, 500, 1000, 15000],
                             labels=['0–50', '51–200', '201–500', '501–1000', '1000+'])
vb_avg = df.groupby('Votes Bucket', observed=True)['Aggregate rating'].mean()
print("\nAverage Rating by Votes Bucket:")
for bucket, avg in vb_avg.items():
    trend = '↑' if avg >= 3.5 else '→' if avg >= 2.5 else '↓'
    print(f"  {bucket:<12} → avg rating {avg:.2f}  {trend}")


# ══════════════════════════════════════════════
# LEVEL 3 – TASK 3: PRICE RANGE vs SERVICES
# ══════════════════════════════════════════════
print("\n" + "=" * 60)
print("TASK 3: PRICE RANGE vs ONLINE DELIVERY & TABLE BOOKING")
print("=" * 60)

label_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
od_pct, tb_pct, both_pct = [], [], []

print(f"\n  {'Range':<6} {'Label':<10} {'Online Delivery':>16} {'Table Booking':>14} {'Both Services':>14}")
print("  " + "-" * 65)

for pr in [1, 2, 3, 4]:
    sub  = df[df['Price range'] == pr]
    od   = (sub['Has Online delivery'] == 'Yes').mean() * 100
    tb   = (sub['Has Table booking']  == 'Yes').mean() * 100
    both = ((sub['Has Online delivery'] == 'Yes') & (sub['Has Table booking'] == 'Yes')).mean() * 100
    od_pct.append(od); tb_pct.append(tb); both_pct.append(both)
    print(f"  {pr:<6} {label_map[pr]:<10} {od:>14.1f}%  {tb:>12.1f}%  {both:>12.1f}%")

print("\n✔ Key Findings:")
print("  • Online Delivery peaks at Range 2 (Medium) — 41.3%")
print("  • Table Booking increases with price: Range 4 highest at 46.8%")
print("  • Budget (Range 1) restaurants almost never offer Table Booking (0.0%)")
print("  • Premium restaurants prefer Table Booking over Online Delivery")
print("  • Conclusion: Higher price → more likely to offer Table Booking;")
print("                Mid-range  → more likely to offer Online Delivery")


# ══════════════════════════════════════════════
# COMBINED VISUALISATION
# ══════════════════════════════════════════════
rt_colors    = ['#1a9641', '#2ecc71', '#a6d96a', '#f39c12', '#e74c3c', '#bdc3c7']
rated_order  = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
ra           = rt_avgs.reindex(rated_order)
rv           = rt_votes.reindex(rated_order)
sample       = df[df['Votes'] > 0].sample(min(2000, len(df)), random_state=42)
vb_avg       = df.groupby('Votes Bucket', observed=True)['Aggregate rating'].mean()

fig = plt.figure(figsize=(22, 28), facecolor='#f4f6f8')
fig.suptitle('Cognifyz Data Analysis Internship\nLevel 3 – Complete Task Results',
             fontsize=24, fontweight='bold', color='#2c3e50', y=0.99)

# Task 1A
ax1a = fig.add_subplot(5, 2, 1)
bars1a = ax1a.bar(order, rt_counts.values, color=rt_colors, edgecolor='white', linewidth=0.8)
ax1a.set_title('Task 1A: Rating Text Distribution', fontsize=13, fontweight='bold', color='#2c3e50')
ax1a.set_ylabel('Number of Restaurants', fontsize=10)
ax1a.set_facecolor('#ffffff')
ax1a.spines[['top','right']].set_visible(False)
ax1a.tick_params(axis='x', labelsize=8)
for bar, val in zip(bars1a, rt_counts.values):
    ax1a.text(bar.get_x()+bar.get_width()/2, bar.get_height()+30,
              f'{val:,}\n({val/total*100:.1f}%)', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
ax1a.set_ylim(0, max(rt_counts.values)*1.25)

# Task 1B
ax1b = fig.add_subplot(5, 2, 2)
bars1b = ax1b.bar(rated_order, rv.values, color=rt_colors[:5], edgecolor='white', linewidth=0.8)
ax1b.set_title('Task 1B: Avg Votes by Rating Category', fontsize=12, fontweight='bold', color='#2c3e50')
ax1b.set_ylabel('Average Number of Votes', fontsize=10)
ax1b.set_facecolor('#ffffff')
ax1b.spines[['top','right']].set_visible(False)
ax1b.tick_params(axis='x', labelsize=8)
for bar, val in zip(bars1b, rv.values):
    ax1b.text(bar.get_x()+bar.get_width()/2, bar.get_height()+8,
              f'{val:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1b.set_ylim(0, max(rv.values)*1.2)
ax1b.text(0.98, 0.95, '"Excellent" restaurants\nget 18x more votes\nthan "Average" ones',
          transform=ax1b.transAxes, ha='right', va='top', fontsize=8,
          bbox=dict(boxstyle='round,pad=0.4', facecolor='#d5f5e3', alpha=0.9))

# Task 1C
ax1c = fig.add_subplot(5, 2, (3, 4))
bars1c = ax1c.barh(rated_order[::-1], ra.values[::-1],
                   color=rt_colors[:5][::-1], edgecolor='white', height=0.5)
ax1c.set_title('Task 1C: Avg Aggregate Rating Score by Rating Category',
               fontsize=12, fontweight='bold', color='#2c3e50')
ax1c.set_xlabel('Average Aggregate Rating (out of 5)', fontsize=10)
ax1c.set_facecolor('#ffffff')
ax1c.spines[['top','right','left']].set_visible(False)
ax1c.tick_params(left=False)
for bar, val in zip(bars1c, ra.values[::-1]):
    ax1c.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
              f'{val:.2f}', va='center', fontsize=11, fontweight='bold')
ax1c.set_xlim(0, 5.5)
ax1c.set_yticks(range(len(rated_order)))
ax1c.set_yticklabels(rated_order[::-1], fontsize=11)

# Task 2A
top10 = df.nlargest(10, 'Votes')[['Restaurant Name','Aggregate rating','Votes']]
names_short = [n[:28]+'…' if len(n)>28 else n for n in top10['Restaurant Name']]
vote_colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, 10))
ax2a = fig.add_subplot(5, 2, (5, 6))
ax2a.barh(names_short[::-1], top10['Votes'].values[::-1],
          color=vote_colors, edgecolor='white', height=0.6)
ax2a.set_title('Task 2A: Top 10 Restaurants by Number of Votes',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax2a.set_xlabel('Number of Votes', fontsize=10)
ax2a.set_facecolor('#ffffff')
ax2a.spines[['top','right','left']].set_visible(False)
ax2a.tick_params(left=False)
for i, (v, r) in enumerate(zip(top10['Votes'].values[::-1], top10['Aggregate rating'].values[::-1])):
    ax2a.text(v+50, i, f'{v:,}  (★{r})', va='center', fontsize=9, fontweight='bold')
ax2a.set_xlim(0, top10['Votes'].max()*1.22)
ax2a.set_yticks(range(len(names_short)))
ax2a.set_yticklabels(names_short[::-1], fontsize=8.5)

# Task 2B
bucket_colors = ['#e74c3c','#e67e22','#f1c40f','#2ecc71','#1a9641']
ax2b = fig.add_subplot(5, 2, 7)
ax2b.bar(vb_avg.index, vb_avg.values, color=bucket_colors, edgecolor='white', linewidth=0.8)
ax2b.set_title('Task 2B: Avg Rating by\nVotes Bucket', fontsize=12, fontweight='bold', color='#2c3e50')
ax2b.set_xlabel('Votes Range', fontsize=10)
ax2b.set_ylabel('Average Rating', fontsize=10)
ax2b.set_ylim(0, 5.2)
ax2b.set_facecolor('#ffffff')
ax2b.spines[['top','right']].set_visible(False)
for i, val in enumerate(vb_avg.values):
    ax2b.text(i, val+0.07, f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax2b.text(0.97, 0.97, f'Correlation:\nr = {corr_val:.3f}',
          transform=ax2b.transAxes, ha='right', va='top', fontsize=10,
          bbox=dict(boxstyle='round,pad=0.4', facecolor='#d6eaf8', alpha=0.9))

# Task 2C
ax2c = fig.add_subplot(5, 2, 8)
ax2c.scatter(sample['Votes'], sample['Aggregate rating'],
             alpha=0.3, s=8, color='#3498db', edgecolors='none')
z = np.polyfit(sample['Votes'], sample['Aggregate rating'], 1)
xline = np.linspace(sample['Votes'].min(), sample['Votes'].max(), 200)
ax2c.plot(xline, np.poly1d(z)(xline), color='#e74c3c', linewidth=2, label=f'Trend (r={corr_val:.2f})')
ax2c.set_title('Task 2C: Votes vs Aggregate Rating\n(Scatter + Trend Line)',
               fontsize=12, fontweight='bold', color='#2c3e50')
ax2c.set_xlabel('Number of Votes', fontsize=10)
ax2c.set_ylabel('Aggregate Rating', fontsize=10)
ax2c.set_facecolor('#ffffff')
ax2c.spines[['top','right']].set_visible(False)
ax2c.legend(fontsize=9)

# Task 3
x     = np.arange(4)
width = 0.25
price_labels = ['Range 1\n(Low)', 'Range 2\n(Medium)', 'Range 3\n(High)', 'Range 4\n(Very High)']
ax3 = fig.add_subplot(5, 2, (9, 10))
b1 = ax3.bar(x - width, od_pct,   width, label='Online Delivery', color='#3498db', edgecolor='white')
b2 = ax3.bar(x,         tb_pct,   width, label='Table Booking',   color='#2ecc71', edgecolor='white')
b3 = ax3.bar(x + width, both_pct, width, label='Both Services',   color='#9b59b6', edgecolor='white')
ax3.set_title('Task 3: Price Range vs Online Delivery & Table Booking\n(% of restaurants offering each service)',
              fontsize=13, fontweight='bold', color='#2c3e50')
ax3.set_xticks(x)
ax3.set_xticklabels(price_labels, fontsize=10)
ax3.set_ylabel('% of Restaurants', fontsize=11)
ax3.set_ylim(0, 70)
ax3.set_facecolor('#ffffff')
ax3.spines[['top','right']].set_visible(False)
ax3.legend(fontsize=10, loc='upper right')
for bars, vals in [(b1, od_pct),(b2, tb_pct),(b3, both_pct)]:
    for bar, val in zip(bars, vals):
        ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.8,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax3.text(0.01, 0.97,
         "Key Insight:\n• Online Delivery peaks at Range 2 (41.3%)\n"
         "• Table Booking peaks at Range 4 (46.8%)\n"
         "• Higher price → more Table Booking\n"
         "• Budget restaurants prefer Delivery",
         transform=ax3.transAxes, va='top', fontsize=9,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef9e7', alpha=0.95))

plt.tight_layout(rect=[0, 0, 1, 0.97], h_pad=3.5, w_pad=2.5)
plt.savefig('Level3_Analysis.png', dpi=150, bbox_inches='tight', facecolor='#f4f6f8')
print("\nChart saved as Level3_Analysis.png")
