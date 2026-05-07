"""Generate TF-IDF vs Embeddings comparison visual for Ch 23 lecture slides."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'sans-serif'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4.5))

# Left panel: TF-IDF (sparse, high-dimensional)
ax1.set_title('TF-IDF', fontsize=12, fontweight='bold', color='#2C6FA0')
criteria = ['Interpretability', 'Cost', 'Synonyms', 'Negation', 'Auditability']
scores_tfidf = [5, 5, 1, 1, 5]
colors_tfidf = ['#2ecc71', '#2ecc71', '#e74c3c', '#e74c3c', '#2ecc71']
bars1 = ax1.barh(criteria, scores_tfidf, color=colors_tfidf, alpha=0.8, edgecolor='white')
ax1.set_xlim(0, 6)
ax1.set_xticks([])
for bar, score in zip(bars1, scores_tfidf):
    label = 'High' if score >= 4 else 'Low'
    ax1.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
             label, va='center', fontsize=8, fontweight='bold',
             color='#2ecc71' if score >= 4 else '#e74c3c')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['bottom'].set_visible(False)

# Right panel: Embeddings (dense, semantic)
ax2.set_title('Embeddings', fontsize=12, fontweight='bold', color='#8E44AD')
scores_emb = [1, 3, 5, 4, 1]
colors_emb = ['#e74c3c', '#f39c12', '#2ecc71', '#2ecc71', '#e74c3c']
bars2 = ax2.barh(criteria, scores_emb, color=colors_emb, alpha=0.8, edgecolor='white')
ax2.set_xlim(0, 6)
ax2.set_xticks([])
ax2.set_yticklabels([])
for bar, score in zip(bars2, scores_emb):
    label = 'High' if score >= 4 else ('Med' if score == 3 else 'Low')
    color = '#2ecc71' if score >= 4 else ('#f39c12' if score == 3 else '#e74c3c')
    ax2.text(bar.get_width() + 0.15, bar.get_y() + bar.get_height()/2,
             label, va='center', fontsize=8, fontweight='bold', color=color)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)

# Bottom annotation
fig.text(0.5, 0.02, 'Research papers → TF-IDF  |  Production/similarity → Embeddings',
         ha='center', fontsize=8, style='italic', color='#555')

plt.tight_layout(rect=[0, 0.06, 1, 1])
plt.savefig('figures/ch23-tfidf-vs-embeddings.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: ch23-tfidf-vs-embeddings.png')
