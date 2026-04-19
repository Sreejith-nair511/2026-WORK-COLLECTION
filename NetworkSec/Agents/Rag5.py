import matplotlib.pyplot as plt
import pandas as pd

# --- Data for comparison ---
data = {
    "Parameter": [
        "Complexity",
        "Latency",
        "Reasoning Ability",
        "Scalability",
        "Storage Backend",
        "Best Finance Use Case"
    ],
    "Basic RAG": [
        "Low",
        "Low",
        "Limited (single fact retrieval)",
        "High",
        "Vector DB",
        "Simple stock Q&A (e.g., 'Why did Tesla rise today?')"
    ],
    "Multi-step RAG": [
        "Medium",
        "Medium",
        "Moderate (multi-hop reasoning)",
        "Medium",
        "Vector DB",
        "Trend analysis across company + sector (e.g., Tesla + EV industry)"
    ]
}

df = pd.DataFrame(data)

# --- Create Matplotlib Table ---
fig, ax = plt.subplots(figsize=(12, 3))  # adjust size for paper
ax.axis("off")

# Add table
table = ax.table(cellText=df.values,
                 colLabels=df.columns,
                 cellLoc='center',
                 loc='center')

# Style
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5)  # (x, y) scaling for readability

# Bold headers
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#4a7ebB')  # dark blue header

plt.title("Basic vs Multi-step RAG Comparison (Stock Domain)", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.show()
