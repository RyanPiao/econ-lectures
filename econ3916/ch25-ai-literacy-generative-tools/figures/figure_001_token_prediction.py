"""Figure 1: LLM Next-Token Prediction — probability distribution over candidate tokens."""
import matplotlib.pyplot as plt
import numpy as np

# White Academia palette
CHARCOAL = '#2D2D2D'
DUSTY_BLUE = '#6B8BA4'
TERRACOTTA = '#C47B5A'
SAGE = '#6A8E6B'
LIGHT_BG = '#F8F6F3'
DECORATIVE = '#D5CEC7'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
})

fig, ax = plt.subplots(figsize=(6, 4.5))

# Token probabilities for the prompt "The Federal Reserve raised interest"
tokens = ['rates', 'rate', 'concerns', 'prices', 'levels', 'spending', 'risks', 'other']
probs = [0.42, 0.28, 0.08, 0.06, 0.05, 0.04, 0.03, 0.04]

colors = [TERRACOTTA if i == 0 else DUSTY_BLUE for i in range(len(tokens))]

bars = ax.barh(range(len(tokens)), probs, color=colors, edgecolor='white', height=0.65)

ax.set_yticks(range(len(tokens)))
ax.set_yticklabels(tokens, fontsize=12, color=CHARCOAL)
ax.set_xlabel('Probability', color=CHARCOAL)
ax.invert_yaxis()

# Add probability labels
for i, (bar, prob) in enumerate(zip(bars, probs)):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
            f'{prob:.0%}', va='center', fontsize=11, color=CHARCOAL)

# Context line
ax.text(0.0, -0.8, 'Prompt: "The Federal Reserve raised interest ___"',
        fontsize=11, style='italic', color=CHARCOAL, transform=ax.get_yaxis_transform())

ax.set_xlim(0, 0.55)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color(DECORATIVE)
ax.spines['left'].set_color(DECORATIVE)
ax.tick_params(colors=CHARCOAL)

plt.tight_layout()
plt.savefig(
    __file__.replace('.py', '.png'),
    dpi=150, bbox_inches='tight', facecolor='white'
)
plt.close()
print("OK: figure_001_token_prediction.png")
