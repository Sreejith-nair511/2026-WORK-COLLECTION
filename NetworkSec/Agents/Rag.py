import random
import matplotlib.pyplot as plt
import networkx as nx

# Dummy stock knowledge base
knowledge_base = {
    "AAPL": "Apple stock rose due to strong iPhone sales.",
    "GOOGL": "Google stock declined after antitrust news.",
    "TSLA": "Tesla stock jumped following new EV incentives.",
    "MSFT": "Microsoft stock remained stable amid cloud growth.",
    "AMZN": "Amazon stock rose due to strong AWS performance."
}

# --- Simple retriever function (simulating embeddings) ---
def retrieve(query, method="basic"):
    # Just random retrieval for demonstration
    if method == "basic":
        return random.choice(list(knowledge_base.values()))
    elif method == "multi-step":
        return [random.choice(list(knowledge_base.values())) for _ in range(2)]
    elif method == "agentic":
        domain = "tech stocks" if "cloud" in query or "AI" in query else "general"
        return f"Agent picked {domain} domain -> {random.choice(list(knowledge_base.values()))}"
    elif method == "hybrid":
        vec_result = random.choice(list(knowledge_base.values()))
        graph_relation = "Linked to NASDAQ performance"
        return f"{vec_result} | {graph_relation}"
    else:
        return "No retrieval method"

# --- Generation step ---
def generate_answer(query, retrieved):
    return f"Q: {query}\nA: Based on retrieval -> {retrieved}"

# --- Run all RAG types ---
query = "What is affecting stock performance today?"

methods = ["basic", "multi-step", "agentic", "hybrid"]
results = {}
for m in methods:
    retrieved = retrieve(query, method=m)
    results[m] = generate_answer(query, retrieved)

# --- Print results ---
for m, ans in results.items():
    print(f"\n--- {m.upper()} RAG ---")
    print(ans)

# --- Visualization with Matplotlib ---
def plot_rag_graph(method):
    G = nx.DiGraph()
    G.add_node("Query", color="skyblue")
    if method == "basic":
        G.add_nodes_from(["Retriever", "LLM"])
        G.add_edges_from([("Query", "Retriever"), ("Retriever", "LLM")])
    elif method == "multi-step":
        G.add_nodes_from(["Retriever Step 1", "Retriever Step 2", "LLM"])
        G.add_edges_from([("Query", "Retriever Step 1"),
                          ("Retriever Step 1", "Retriever Step 2"),
                          ("Retriever Step 2", "LLM")])
    elif method == "agentic":
        G.add_nodes_from(["Agent", "Retriever", "Tool", "LLM"])
        G.add_edges_from([("Query", "Agent"), ("Agent", "Retriever"),
                          ("Retriever", "Tool"), ("Tool", "LLM")])
    elif method == "hybrid":
        G.add_nodes_from(["Vector DB", "Graph DB", "Fusion Layer", "LLM"])
        G.add_edges_from([("Query", "Vector DB"), ("Query", "Graph DB"),
                          ("Vector DB", "Fusion Layer"), ("Graph DB", "Fusion Layer"),
                          ("Fusion Layer", "LLM")])

    pos = nx.spring_layout(G)
    colors = [G.nodes[n].get("color", "lightgreen") for n in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, font_size=10, arrowsize=20)
    plt.title(f"{method.upper()} RAG Pipeline")
    plt.show()

# Plot all methods
for m in methods:
    plot_rag_graph(m)
