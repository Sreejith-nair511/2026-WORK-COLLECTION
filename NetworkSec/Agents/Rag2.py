import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# ---------- GRAPH DRAWING FUNCTION ----------
def draw_pipeline(method, nodes, edges, ax):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1500, edgecolors="black", ax=ax)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color="gray", width=2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)
    ax.set_title(f"{method} RAG", fontsize=12, fontweight="bold")
    ax.axis("off")

# ---------- PIPELINE DEFINITIONS ----------
pipelines = {
    "Basic": {
        "nodes": ["Query", "Retriever", "LLM"],
        "edges": [("Query", "Retriever"), ("Retriever", "LLM")]
    },
    "Multi-step": {
        "nodes": ["Query", "Retriever Step 1", "Retriever Step 2", "LLM"],
        "edges": [("Query", "Retriever Step 1"),
                  ("Retriever Step 1", "Retriever Step 2"),
                  ("Retriever Step 2", "LLM")]
    },
    "Agentic": {
        "nodes": ["Query", "Agent", "Retriever", "Tool", "LLM"],
        "edges": [("Query", "Agent"),
                  ("Agent", "Retriever"),
                  ("Agent", "Tool"),
                  ("Retriever", "LLM"),
                  ("Tool", "LLM")]
    },
    "Hybrid": {
        "nodes": ["Query", "Vector DB", "Graph DB", "Fusion Layer", "LLM"],
        "edges": [("Query", "Vector DB"),
                  ("Query", "Graph DB"),
                  ("Vector DB", "Fusion Layer"),
                  ("Graph DB", "Fusion Layer"),
                  ("Fusion Layer", "LLM")]
    }
}

# ---------- DRAW PIPELINE GRAPHS ----------
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

for i, (method, config) in enumerate(pipelines.items()):
    draw_pipeline(method, config["nodes"], config["edges"], axes[i])

plt.tight_layout()
plt.show()

# ---------- PARAMETER COMPARISON ----------
data = {
    "Pipeline": ["Basic RAG", "Multi-step RAG", "Agentic RAG", "Hybrid RAG"],
    "Complexity": ["Low", "Medium", "High", "High"],
    "Latency": ["Low", "Medium", "High", "Medium-High"],
    "Reasoning Ability": ["Limited", "Moderate (multi-hop)", "Strong (agent reasoning)", "Moderate (structural + semantic)"],
    "Scalability": ["High", "Medium", "Medium", "Medium"],
    "Storage Backend": ["Vector DB", "Vector DB", "Vector DB + Tools", "Vector DB + Graph DB"],
    "Best Use Case": [
        "Simple stock Q&A",
        "Analyzing trends across multiple sources",
        "Autonomous portfolio insights & compliance checks",
        "Risk management with relational + semantic data"
    ]
}

df = pd.DataFrame(data)

# ---------- PRINT TABLE ----------
print("\n--- RAG Pipeline Parameter Comparison ---\n")
print(df.to_string(index=False))

# ---------- VISUAL COMPARISON (Bar Chart: Complexity & Latency) ----------
fig, ax = plt.subplots(figsize=(8, 5))
categories = ["Complexity", "Latency"]
colors = ["#4daf4a", "#377eb8"]

for idx, cat in enumerate(categories):
    ax.bar([x + idx*0.2 for x in range(len(df))],
           df[cat].map({"Low":1, "Medium":2, "Medium-High":2.5, "High":3}),
           width=0.2, label=cat, color=colors[idx])

ax.set_xticks([x+0.2 for x in range(len(df))])
ax.set_xticklabels(df["Pipeline"], rotation=15, ha="right")
ax.set_ylabel("Scale: 1 (Low) → 3 (High)")
ax.set_title("Comparison of RAG Pipelines by Complexity & Latency")
ax.legend()
plt.tight_layout()
plt.show()
