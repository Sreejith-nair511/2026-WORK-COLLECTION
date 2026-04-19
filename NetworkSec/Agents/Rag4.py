import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ------------------- PARAMETER COMPARISON -------------------
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

# ------------------- PRINT COMPARISON TABLE -------------------
print("\n--- Basic vs Multi-step RAG Comparison ---\n")
print(df.to_string(index=False))

# ------------------- NUMERIC ENCODING FOR GRAPH -------------------
# Mapping qualitative values to numeric for plotting
mapping = {"Low": 1, "Medium": 2, "High": 3}
numeric_df = pd.DataFrame({
    "Parameter": ["Complexity", "Latency", "Reasoning Ability*", "Scalability"],
    "Basic RAG": [mapping["Low"], mapping["Low"], mapping["Low"], mapping["High"]],
    "Multi-step RAG": [mapping["Medium"], mapping["Medium"], mapping["Medium"], mapping["Medium"]]
})

# ------------------- BAR CHART VISUALIZATION -------------------
labels = numeric_df["Parameter"]
x = np.arange(len(labels))  # label locations
width = 0.35

fig, ax = plt.subplots(figsize=(8,5))
rects1 = ax.bar(x - width/2, numeric_df["Basic RAG"], width, label="Basic RAG", color="#4daf4a")
rects2 = ax.bar(x + width/2, numeric_df["Multi-step RAG"], width, label="Multi-step RAG", color="#377eb8")

# Add labels
ax.set_ylabel("Scale: 1=Low, 2=Medium, 3=High")
ax.set_title("Basic RAG vs Multi-step RAG (Stock Domain)")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=15, ha="right")
ax.legend()

# Annotate bars
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.annotate(f"{height}",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # offset
                textcoords="offset points",
                ha="center", va="bottom")

plt.tight_layout()
plt.show()
