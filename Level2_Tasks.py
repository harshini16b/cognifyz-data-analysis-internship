"""
Cognifyz Technologies – Data Analysis Internship
Level 2 – All Tasks (1 to 4)
Author  : [Your Name]
Dataset : Dataset_.csv  (9551 restaurants, 21 columns)
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from collections import Counter

# ──────────────────────────────────────────────
# Load dataset
# ──────────────────────────────────────────────
df    = pd.read_csv('Dataset_.csv')
total = len(df)
print(f"Dataset loaded: {total} rows, {df.shape[1]} columns\n")


# ══════════════════════════════════════════════
# LEVEL 2 – TASK 1: RESTAURANT RATINGS
# ══════════════════════════════════════════════
print("=" * 55)
print("TASK 1: RESTAURANT RATINGS")
print("=" * 55)

# Bin ratings into ranges
bins   = [0, 1, 2, 3, 4, 5]
labels = ['0–1', '1–2', '2–3', '3–4', '4–5']
df['Rating Range'] = pd.cut(df['Aggregate rating'], bins=bins,
                             labels=labels, include_lowest=True)
rating_dist = df['Rating Range'].value_counts().sort_index()

print("\nRating Distribution:")
for rng, cnt in rating_dist.items():
    bar = '█' * int(cnt / 50)
    print(f"  {rng}  | {bar} {cnt:,}  ({cnt/total*100:.2f}%)")

most_common_range = rating_dist.idxmax()
print(f"\n✔ Most common rating range : {most_common_range}")
print(f"✔ Average votes per restaurant : {df['Votes'].mean():.2f}")
print(f"✔ Median  votes per restaurant : {df['Votes'].median():.0f}")
print(f"✔ Maximum votes any restaurant : {df['Votes'].max():,}")


# ══════════════════════════════════════════════
# LEVEL 2 – TASK 2: CUISINE COMBINATIONS
# ══════════════════════════════════════════════
print("\n" + "=" * 55)
print("TASK 2: CUISINE COMBINATIONS")
print("=" * 55)

combo_counts  = Counter()
combo_ratings = {}

for entry, rating in zip(df['Cuisines'].fillna(''), df['Aggregate rating']):
    parts = [x.strip() for x in entry.split(',')]
    if len(parts) >= 2:
        combo = ', '.join(sorted(parts))          # normalise order
        combo_counts[combo] += 1
        combo_ratings.setdefault(combo, []).append(rating)

top10 = combo_counts.most_common(10)
print(f"\nRestaurants with multiple cuisines: {sum(1 for v in combo_counts.values() if v)}")
print("\nTop 10 Cuisine Combinations (by count) + Avg Rating:")
print(f"  {'Combination':<45} {'Count':>6}  {'Avg Rating':>10}")
print("  " + "-" * 65)
for combo, cnt in top10:
    avg_r = np.mean(combo_ratings[combo])
    note  = "⬆ Higher" if avg_r >= 3.0 else "⬇ Lower"
    print(f"  {combo:<45} {cnt:>6}   {avg_r:>6.2f}  {note}")


# ══════════════════════════════════════════════
# LEVEL 2 – TASK 3: GEOGRAPHIC ANALYSIS
# ══════════════════════════════════════════════
print("\n" + "=" * 55)
print("TASK 3: GEOGRAPHIC ANALYSIS")
print("=" * 55)

geo = df[(df['Longitude'] != 0) & (df['Latitude'] != 0)].copy()
print(f"\nRestaurants with valid coordinates : {len(geo):,}")
print(f"Longitude range : {geo['Longitude'].min():.4f}  →  {geo['Longitude'].max():.4f}")
print(f"Latitude  range : {geo['Latitude'].min():.4f}  →  {geo['Latitude'].max():.4f}")
print("\nCountry Code distribution (top 5):")
print(df['Country Code'].value_counts().head(5).to_string())
print("\nGeographic clusters observed:")
print("  • Dense cluster in India  (Lat 28–29, Lon 77–78) → New Delhi area")
print("  • Cluster in Philippines  (Lat 14–15, Lon 121)")
print("  • Scattered points in USA, UK, Brazil, South Africa, Australia")


# ══════════════════════════════════════════════
# LEVEL 2 – TASK 4: RESTAURANT CHAINS
# ══════════════════════════════════════════════
print("\n" + "=" * 55)
print("TASK 4: RESTAURANT CHAINS")
print("=" * 55)

name_counts = df['Restaurant Name'].value_counts()
chains      = name_counts[name_counts > 1]

print(f"\nTotal unique restaurant names : {df['Restaurant Name'].nunique():,}")
print(f"Names appearing > 1 time (chains): {len(chains):,}")

chain_df = df[df['Restaurant Name'].isin(chains.index)].groupby('Restaurant Name').agg(
    outlets     = ('Restaurant ID', 'count'),
    avg_rating  = ('Aggregate rating', 'mean'),
    total_votes = ('Votes', 'sum')
).sort_values('outlets', ascending=False).head(15)

print("\nTop 15 Restaurant Chains:")
print(f"  {'Chain Name':<25} {'Outlets':>8}  {'Avg Rating':>10}  {'Total Votes':>12}")
print("  " + "-" * 60)
for name, row in chain_df.iterrows():
    print(f"  {name:<25} {int(row['outlets']):>8}  {row['avg_rating']:>10.2f}  {int(row['total_votes']):>12,}")


# ══════════════════════════════════════════════
# COMBINED VISUALISATION  (10 sub-plots, 5 rows)
# ══════════════════════════════════════════════
COLORS = ['#3498db','#2ecc71','#e74c3c','#f39c12','#9b59b6',
          '#1abc9c','#e67e22','#34495e','#e91e63','#00bcd4',
          '#8bc34a','#ff5722']

# ── prepare data ──
top10_combos       = combo_counts.most_common(10)
combo_names        = [c[0] for c in top10_combos]
combo_cnts         = [c[1] for c in top10_combos]
combo_avgs         = [np.mean(combo_ratings[c[0]]) for c in top10_combos]
def shorten(n, m=30): return n if len(n) <= m else n[:m] + '…'
combo_names_short  = [shorten(n) for n in combo_names]

chain_plot = chain_df.head(12)
chain_names   = chain_plot.index.tolist()
chain_outlets = chain_plot['outlets'].tolist()
chain_ratings = chain_plot['avg_rating'].tolist()

rated = df[df['Aggregate rating'] > 0]['Aggregate rating']
avg_votes = df['Votes'].mean()

fig = plt.figure(figsize=(22, 28), facecolor='#f4f6f8')
fig.suptitle('Cognifyz Data Analysis Internship\nLevel 2 – Complete Task Results',
             fontsize=24, fontweight='bold', color='#2c3e50', y=0.99)

# ── Task 1A: Rating range bar ──
ax1a = fig.add_subplot(5, 2, 1)
bar_colors_t1 = ['#e74c3c','#e67e22','#f39c12','#3498db','#2ecc71']
bars1 = ax1a.bar(rating_dist.index, rating_dist.values,
                 color=bar_colors_t1, edgecolor='white', linewidth=0.8)
ax1a.set_title('Task 1A: Rating Range Distribution', fontsize=13, fontweight='bold', color='#2c3e50')
ax1a.set_xlabel('Rating Range', fontsize=10)
ax1a.set_ylabel('Number of Restaurants', fontsize=10)
ax1a.set_facecolor('#ffffff')
ax1a.spines[['top','right']].set_visible(False)
for bar, val in zip(bars1, rating_dist.values):
    pct = val / total * 100
    ax1a.text(bar.get_x()+bar.get_width()/2, bar.get_height()+20,
              f'{val:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=8, fontweight='bold')
ax1a.set_ylim(0, max(rating_dist.values)*1.25)
most_common_idx = list(rating_dist.index).index(rating_dist.idxmax())
bars1[most_common_idx].set_edgecolor('#2c3e50')
bars1[most_common_idx].set_linewidth(2.5)

# ── Task 1B: Rating histogram ──
ax1b = fig.add_subplot(5, 2, 2)
ax1b.hist(rated, bins=25, color='#3498db', edgecolor='white', linewidth=0.6, alpha=0.85)
ax1b.axvline(rated.mean(),   color='#e74c3c', linewidth=2, linestyle='--', label=f'Mean: {rated.mean():.2f}')
ax1b.axvline(rated.median(), color='#f39c12', linewidth=2, linestyle='--', label=f'Median: {rated.median():.2f}')
ax1b.set_title('Task 1B: Aggregate Rating Histogram\n(Rated restaurants only)', fontsize=13, fontweight='bold', color='#2c3e50')
ax1b.set_xlabel('Aggregate Rating', fontsize=10)
ax1b.set_ylabel('Frequency', fontsize=10)
ax1b.set_facecolor('#ffffff')
ax1b.spines[['top','right']].set_visible(False)
ax1b.legend(fontsize=9)
ax1b.text(0.98, 0.90, f'Avg Votes/\nRestaurant:\n{avg_votes:.0f}',
          transform=ax1b.transAxes, ha='right', va='top', fontsize=9,
          bbox=dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', alpha=0.9))

# ── Task 2A: Combo count ──
ax2a = fig.add_subplot(5, 2, (3, 4))
ax2a.barh(combo_names_short[::-1], combo_cnts[::-1],
          color=COLORS[:10][::-1], edgecolor='white', height=0.6)
ax2a.set_title('Task 2A: Top 10 Cuisine Combinations by Count',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax2a.set_xlabel('Number of Restaurants', fontsize=10)
ax2a.set_facecolor('#ffffff')
ax2a.spines[['top','right','left']].set_visible(False)
ax2a.tick_params(left=False)
for i, (cnt, name) in enumerate(zip(combo_cnts[::-1], combo_names_short[::-1])):
    ax2a.text(cnt+5, i, f'{cnt}', va='center', fontsize=9, fontweight='bold')
ax2a.set_xlim(0, max(combo_cnts)*1.15)
ax2a.set_yticks(range(len(combo_names_short)))
ax2a.set_yticklabels(combo_names_short[::-1], fontsize=8)

# ── Task 2B: Combo avg ratings ──
ax2b = fig.add_subplot(5, 2, (5, 6))
rating_colors = ['#2ecc71' if r >= 3.0 else '#e74c3c' for r in combo_avgs[::-1]]
ax2b.barh(combo_names_short[::-1], combo_avgs[::-1],
          color=rating_colors, edgecolor='white', height=0.6)
ax2b.axvline(3.0, color='#2c3e50', linewidth=1.5, linestyle='--', alpha=0.6)
ax2b.set_title('Task 2B: Average Rating per Cuisine Combination',
               fontsize=13, fontweight='bold', color='#2c3e50')
ax2b.set_xlabel('Average Rating', fontsize=10)
ax2b.set_xlim(0, 5)
ax2b.set_facecolor('#ffffff')
ax2b.spines[['top','right','left']].set_visible(False)
ax2b.tick_params(left=False)
for i, val in enumerate(combo_avgs[::-1]):
    ax2b.text(val+0.05, i, f'{val:.2f}', va='center', fontsize=9, fontweight='bold')
ax2b.set_yticks(range(len(combo_names_short)))
ax2b.set_yticklabels(combo_names_short[::-1], fontsize=8)
ax2b.legend(handles=[mpatches.Patch(color='#2ecc71', label='Rating ≥ 3.0'),
                      mpatches.Patch(color='#e74c3c', label='Rating < 3.0')],
            fontsize=9, loc='lower right')

# ── Task 3: Geographic scatter ──
ax3 = fig.add_subplot(5, 2, (7, 8))
sc = ax3.scatter(geo['Longitude'], geo['Latitude'],
                 c=geo['Aggregate rating'], cmap='RdYlGn',
                 s=2, alpha=0.5, vmin=0, vmax=5)
plt.colorbar(sc, ax=ax3, shrink=0.6, pad=0.02, label='Aggregate Rating')
ax3.set_title('Task 3: Geographic Distribution of Restaurants (Color = Rating)',
              fontsize=13, fontweight='bold', color='#2c3e50')
ax3.set_xlabel('Longitude', fontsize=10)
ax3.set_ylabel('Latitude', fontsize=10)
ax3.set_facecolor('#dce9f5')
ax3.spines[['top','right']].set_visible(False)
ax3.text(0.02, 0.97, f'Plotted: {len(geo):,} restaurants',
         transform=ax3.transAxes, va='top', fontsize=9,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# ── Task 4A: Chain outlets ──
ax4a = fig.add_subplot(5, 2, 9)
ax4a.barh(chain_names[::-1], chain_outlets[::-1],
          color=COLORS[:len(chain_names)][::-1], edgecolor='white', height=0.6)
ax4a.set_title('Task 4A: Top 12 Chains\nby Number of Outlets',
               fontsize=12, fontweight='bold', color='#2c3e50')
ax4a.set_xlabel('Number of Outlets', fontsize=10)
ax4a.set_facecolor('#ffffff')
ax4a.spines[['top','right','left']].set_visible(False)
ax4a.tick_params(left=False)
for i, cnt in enumerate(chain_outlets[::-1]):
    ax4a.text(cnt+0.4, i, f'{cnt}', va='center', fontsize=9, fontweight='bold')
ax4a.set_xlim(0, max(chain_outlets)*1.18)
ax4a.set_yticks(range(len(chain_names)))
ax4a.set_yticklabels(chain_names[::-1], fontsize=8)

# ── Task 4B: Chain avg ratings ──
ax4b = fig.add_subplot(5, 2, 10)
colors4b = ['#2ecc71' if r >= 3.5 else '#f39c12' if r >= 2.5 else '#e74c3c'
            for r in chain_ratings[::-1]]
ax4b.barh(chain_names[::-1], chain_ratings[::-1],
          color=colors4b, edgecolor='white', height=0.6)
ax4b.axvline(3.5, color='#2c3e50', linewidth=1.5, linestyle='--', alpha=0.6)
ax4b.set_title('Task 4B: Top 12 Chains\nby Average Rating',
               fontsize=12, fontweight='bold', color='#2c3e50')
ax4b.set_xlabel('Average Rating', fontsize=10)
ax4b.set_xlim(0, 5.5)
ax4b.set_facecolor('#ffffff')
ax4b.spines[['top','right','left']].set_visible(False)
ax4b.tick_params(left=False)
for i, val in enumerate(chain_ratings[::-1]):
    ax4b.text(val+0.05, i, f'{val:.2f}', va='center', fontsize=9, fontweight='bold')
ax4b.set_yticks(range(len(chain_names)))
ax4b.set_yticklabels(chain_names[::-1], fontsize=8)
ax4b.legend(handles=[mpatches.Patch(color='#2ecc71', label='≥ 3.5 Good'),
                      mpatches.Patch(color='#f39c12', label='2.5–3.5 Average'),
                      mpatches.Patch(color='#e74c3c', label='< 2.5 Below avg')],
            fontsize=8, loc='lower right')

plt.tight_layout(rect=[0, 0, 1, 0.97], h_pad=3.5, w_pad=2.5)
plt.savefig('Level2_Analysis.png', dpi=150, bbox_inches='tight', facecolor='#f4f6f8')
print("\nChart saved as Level2_Analysis.png")
