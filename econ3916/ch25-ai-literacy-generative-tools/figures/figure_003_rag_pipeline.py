"""Figure 3: RAG Pipeline Flow — 4-stage architecture diagram."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# White Academia palette
CHARCOAL = '#2D2D2D'
DUSTY_BLUE = '#6B8BA4'
TERRACOTTA = '#C47B5A'
SAGE = '#6A8E6B'
LIGHT_BG = '#F8F6F3'
DECORATIVE = '#D5CEC7'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.size': 11,
})

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis('off')

# Helper function
def draw_box(ax, x, y, w, h, text, subtext, color, text_color='white'):
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                     boxstyle="round,pad=0.15",
                                     facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + 0.15, text,
            ha='center', va='center', fontsize=12, fontweight='bold', color=text_color)
    ax.text(x + w/2, y + h/2 - 0.25, subtext,
            ha='center', va='center', fontsize=8, color=text_color, alpha=0.85)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=CHARCOAL, lw=1.5))

# Stage boxes (horizontal flow)
box_w, box_h = 1.8, 1.2
y_main = 3.0

# Stage 1: Documents
draw_box(ax, 0.2, y_main, box_w, box_h, "1. Chunk", "Split into\n200-500 tokens", DUSTY_BLUE)

# Stage 2: Embed
draw_box(ax, 2.7, y_main, box_w, box_h, "2. Embed", "Text → dense\nvectors", TERRACOTTA)

# Stage 3: Retrieve
draw_box(ax, 5.2, y_main, box_w, box_h, "3. Retrieve", "Find top-k\nsimilar chunks", SAGE)

# Stage 4: Generate
draw_box(ax, 7.7, y_main, box_w, box_h, "4. Generate", "LLM answers\nfrom context", CHARCOAL)

# Arrows between stages
draw_arrow(ax, 2.0, y_main + box_h/2, 2.7, y_main + box_h/2)
draw_arrow(ax, 4.5, y_main + box_h/2, 5.2, y_main + box_h/2)
draw_arrow(ax, 7.0, y_main + box_h/2, 7.7, y_main + box_h/2)

# Input: Documents (top left)
doc_y = 5.3
draw_box(ax, 0.2, doc_y, box_w, 0.9, "Documents", "FOMC Minutes", DECORATIVE, CHARCOAL)
draw_arrow(ax, 1.1, doc_y, 1.1, y_main + box_h)

# Input: Query (top right, feeds into Retrieve)
draw_box(ax, 5.2, doc_y, box_w, 0.9, "Your Question", '"Fed on inflation?"', DECORATIVE, CHARCOAL)
draw_arrow(ax, 6.1, doc_y, 6.1, y_main + box_h)

# Vector DB (between Embed and Retrieve, below)
db_y = 1.2
draw_box(ax, 3.9, db_y, 2.0, 0.9, "Vector DB", "ChromaDB / FAISS", '#E8E4DF', CHARCOAL)
draw_arrow(ax, 3.6, y_main, 4.5, db_y + 0.9)
draw_arrow(ax, 5.4, db_y + 0.9, 6.1, y_main)

# Output: Grounded Answer
out_y = 1.2
draw_box(ax, 7.7, out_y, box_w, 0.9, "Answer", "Grounded in docs", DUSTY_BLUE)
draw_arrow(ax, 8.6, y_main, 8.6, out_y + 0.9)

plt.tight_layout()
plt.savefig(
    __file__.replace('.py', '.png'),
    dpi=150, bbox_inches='tight', facecolor='white'
)
plt.close()
print("OK: figure_003_rag_pipeline.png")
