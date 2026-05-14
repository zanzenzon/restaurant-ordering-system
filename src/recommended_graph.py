"""
recommended_graph.py — Graph-Based Menu Recommendation Engine
============================================================
Models co-occurrence of menu items as an undirected weighted graph.

  V = set of menu items
  E = {(u, v, w) | items u & v were ordered together w times}

BFS from a seed node finds items within a given "hop distance",
ranked by edge weight (frequency).

Complexity:  O(V + E)  for BFS traversal.
"""

from collections import deque, defaultdict
from menu import MENU_ITEMS


# ── Static co-occurrence data (mock past-order history) ──────────────
# Represents: how many times two items appeared in the same past order.
# In a production system this would be computed from a real orders DB.

CO_OCCURRENCE: list[tuple[str, str, int]] = [
    ("burger",      "fries",       42),
    ("burger",      "coke",        38),
    ("burger",      "onion_rings", 21),
    ("burger",      "milkshake",   15),
    ("pasta",       "salad",       30),
    ("pasta",       "juice",       25),
    ("pasta",       "cheesecake",  18),
    ("pizza",       "coke",        35),
    ("pizza",       "fries",       20),
    ("pizza",       "ice_cream",   12),
    ("sandwich",    "fries",       28),
    ("sandwich",    "coke",        26),
    ("sandwich",    "coleslaw",    14),
    ("shawarma",    "fries",       33),
    ("shawarma",    "coke",        29),
    ("fries",       "coke",        55),
    ("fries",       "milkshake",   19),
    ("ice_cream",   "brownie",     22),
    ("brownie",     "milkshake",   17),
    ("cheesecake",  "juice",       11),
    ("salad",       "water",       20),
]


class RecommendationGraph:
    """
    Undirected weighted graph for item co-occurrence.

    Internally stored as an adjacency list:
      adj[u] = [(v, weight), ...]
    """

    def __init__(self):
        # adjacency list: item → list of (neighbor, weight)
        self.adj: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self._build()

    def _build(self):
        """Populate adjacency list from CO_OCCURRENCE data."""
        for u, v, w in CO_OCCURRENCE:
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))   # undirected

    # ── BFS recommendation ────────────────────────────────────────────

    def recommend(self, ordered_items: set, top_n: int = 3) -> list[dict]:
        """
        BFS from every item in the current order.
        Returns the top_n items NOT already ordered, ranked by total
        accumulated edge-weight (popularity score).

        Parameters
        ----------
        ordered_items : set of item names currently in the order
        top_n         : how many recommendations to return

        Algorithm
        ---------
        1. For each seed in ordered_items, run BFS to depth 1.
        2. Accumulate weight(seed, neighbor) for each unordered neighbor.
        3. Sort candidates by score descending.
        4. Return top_n.
        """
        scores: dict[str, int] = defaultdict(int)
        visited_seeds = set()

        queue = deque()
        for seed in ordered_items:
            if seed in self.adj and seed not in visited_seeds:
                visited_seeds.add(seed)
                queue.append(seed)

        # BFS (depth-1 neighbours only — keeps recommendations tight)
        while queue:
            node = queue.popleft()
            for neighbor, weight in self.adj.get(node, []):
                if neighbor not in ordered_items:
                    scores[neighbor] += weight

        if not scores:
            return []

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for name, score in ranked[:top_n]:
            info = MENU_ITEMS.get(name, {})
            results.append({
                "name":  name,
                "price": info.get("price", 0.0),
                "desc":  info.get("desc", ""),
                "score": score,
            })
        return results

    # ── Display helpers ───────────────────────────────────────────────

    def print_recommendations(self, ordered_items: set, top_n: int = 3):
        recs = self.recommend(ordered_items, top_n=top_n)
        if not recs:
            print("  No recommendations available.")
            return
        print("\n  🌟 Customers who ordered this also ordered:")
        print("  " + "─" * 48)
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r['name']:<14} ${r['price']:.2f}   {r['desc']}")
        print()

    def print_adjacency_summary(self):
        """Print graph adjacency list (for report/demo)."""
        print("\n  Graph Adjacency List (co-occurrence weights):")
        print("  " + "─" * 50)
        for node, neighbors in sorted(self.adj.items()):
            nbr_str = ", ".join(f"{n}({w})" for n, w in sorted(neighbors, key=lambda x: -x[1]))
            print(f"  {node:<14} → {nbr_str}")
        print()
