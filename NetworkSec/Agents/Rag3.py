import random
import matplotlib.pyplot as plt
import networkx as nx

# --- Stock knowledge base (dummy finance snippets) ---
stock_kb = {
    "AAPL": "Apple stock rose due to strong iPhone sales.",
    "MSFT": "Microsoft stock grew steadily with cloud revenue.",
    "TSLA": "Tesla stock jumped after new EV incentives.",
    "GOOGL": "Google stock declined after antitrust lawsuits.",
    "AMZN": "Amazon stock surged with strong AWS performance.",
    "SECTOR_TECH": "Tech sector performance is tied to AI adoption.",
    "SECTOR_AUTO": "Auto sector is influenced by EV demand and oil prices."
}

# --- Simple retriever ---
def basic_retriever(query):
    """Returns one relevant document (simulated)."""
    return random.choice(list(stock_kb.values()))

def multi_step_retriever(query):
    """Step 1: Retrieve company info. Step 2: Retrieve sector context."""
    company_info = random.choice(list(stock_kb.values())[:5])  # company-level
    if "Tesla" in company_info:
        sector_info = stock_kb["SECTOR_AUTO"]
    else:
        sector_info = stock_kb["SECTOR_TECH"]
    return [company_info, sector_info]

# --- Basic RAG ---
def basic_rag(query):
    retrieved = basic_retriever(query)
    return f"Q: {query}\nA: Based on info → {retrieved}"

# --- Multi-step RAG ---
def multi_step_rag(query):
    retrieved_docs = multi_step_retriever(query)
    return f"Q: {query}\nA: Step1 (Company) → {retrieved_docs[0]}\n   Step2 (Sector) → {retrieved_docs[1]}"

# --- Run example ---
query = "Why is Tesla stock moving today?"

basic_ans = basic_rag(query)
multi_ans = multi_step_rag(query)

print("\n--- BASIC RAG ---")
print(basic_ans)

print("\n--- MULTI-STEP RAG ---")
print(multi_ans)

# --- Graph Visualization ---
def draw_pipeline(method, nodes, edges):
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6,4))
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2000, edgecolors="black")
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color="gray", width=2)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    plt.title(f"{method} RAG Pipeline", fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.show()

# Basic RAG pipeline
draw_pipeline("Basic", ["Query", "Retriever", "LLM"], 
              [("Query", "Retriever"), ("Retriever", "LLM")])

# Multi-step RAG pipeline
draw_pipeline("Multi-step", ["Query", "Retriever Step 1", "Retriever Step 2", "LLM"], 
              [("Query", "Retriever Step 1"),
               ("Retriever Step 1", "Retriever Step 2"),
               ("Retriever Step 2", "LLM")])
