"""
demo.py — Automated Demo Script (for presentation)
===================================================
Runs a complete scripted order without user input.
Shows all discrete math components in action:
  ✓ FSM transitions
  ✓ Order tree with recursive total
  ✓ Graph-based BFS recommendations
  ✓ Propositional logic rule evaluation
  ✓ Set theory operations on menu categories
"""

import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from fsm             import FSM
from order_tree      import OrderTree
from recommend_graph import RecommendationGraph
from rules           import print_rule_check
from menu            import display_menu, get_category_set, items_in_categories

DELAY = 0.6   # seconds between steps (set to 0 for instant)

def step(msg):
    print(f"\n{'═'*60}")
    print(f"  DEMO STEP: {msg}")
    print('═'*60)
    time.sleep(DELAY)


def run_demo():
    print("\n" + "█"*60)
    print("  RESTAURANT ORDERING SYSTEM — AUTOMATED DEMO")
    print("  Discrete Mathematics Project")
    print("█"*60)

    # ── 1. Set Theory ─────────────────────────────────────────────
    step("1. SET THEORY — Menu Category Sets")
    mains  = get_category_set("main")
    drinks = get_category_set("drink")
    sides  = get_category_set("side")

    print(f"\n  MAIN set   = {mains}")
    print(f"  DRINK set  = {drinks}")
    print(f"  SIDE set   = {sides}")
    print(f"  MAIN ∪ SIDE = {mains | sides}  (union)")
    print(f"  MAIN ∩ DRINK = {mains & drinks}  (intersection — expected empty)")
    print(f"  |MAIN| = {len(mains)},  |DRINK| = {len(drinks)},  |SIDE| = {len(sides)}")

    # ── 2. Display menu ────────────────────────────────────────────
    step("2. MENU DISPLAY")
    display_menu()

    # ── 3. FSM – Start ordering ────────────────────────────────────
    step("3. FSM — State Transitions")
    fsm = FSM()
    fsm.print_transition_table()

    print("  Starting order session …")
    fsm.transition("start")
    print(f"  {fsm.describe()}")

    # ── 4. Build order tree ────────────────────────────────────────
    step("4. ORDER TREE — Adding Items")
    tree = OrderTree()

    tree.add_item("burger_combo")
    fsm.transition("add_item")

    tree.add_item("pasta")
    fsm.transition("add_item")

    tree.add_item("ice_cream")
    fsm.transition("add_item")

    print("\n  Order tree after adding items:")
    tree.display()

    # ── 5. Recursive total demonstration ──────────────────────────
    step("5. RECURSIVE TOTAL — Proof of correctness by induction")
    print("""
  Claim: total(node) correctly computes the sum for any tree height h.

  BASE CASE (h = 0, leaf node):
    total(leaf) = leaf.effective_price   ✓ (directly returns price)

  INDUCTIVE STEP:
    Assume total(child) is correct ∀ children of node n  (I.H.)
    Then  total(n) = n.effective_price + Σ total(child)
                   = n.price + (correct subtotals by I.H.)   ✓

  ∴ By strong induction, total(n) is correct for all finite trees.
""")
    print(f"  Subtotal (recursive): ${tree.subtotal():.2f}")
    print(f"  Tax 14%:              ${tree.tax():.2f}")
    print(f"  Discount (if >$20):   -${tree.discount():.2f}")
    print(f"  TOTAL:                ${tree.total():.2f}")

    # ── 6. Logic rules ─────────────────────────────────────────────
    step("6. PROPOSITIONAL LOGIC — Rule Evaluation")
    print_rule_check(tree.item_names(), tree.subtotal())

    # ── 7. Graph BFS recommendations ──────────────────────────────
    step("7. GRAPH + BFS — Recommendation Engine")
    graph = RecommendationGraph()
    print("  Adjacency list (first 5 nodes):")
    for i, (node, nbrs) in enumerate(sorted(graph.adj.items())):
        if i >= 5: break
        nbr_str = ", ".join(f"{n}({w})" for n, w in sorted(nbrs, key=lambda x: -x[1]))
        print(f"  {node:<14} → {nbr_str}")

    print(f"\n  Current order items: {tree.item_names()}")
    graph.print_recommendations(tree.item_names(), top_n=3)

    # ── 8. FSM – Review → Confirm → Pay ───────────────────────────
    step("8. FSM — Completing the Order")
    fsm.transition("review")
    print(f"  {fsm.describe()}")
    fsm.transition("confirm")
    print(f"  {fsm.describe()}")
    fsm.transition("pay")
    print(f"  {fsm.describe()}")

    # ── 9. FSM History ────────────────────────────────────────────
    step("9. FULL FSM TRANSITION HISTORY")
    fsm.print_history()

    print("\n" + "█"*60)
    print("  DEMO COMPLETE ✓")
    print("  All discrete math components demonstrated:")
    print("  ✓ Sets & Set Operations")
    print("  ✓ Finite-State Machine (6 states, 12 transitions)")
    print("  ✓ N-ary Tree + Recursive Algorithm O(n)")
    print("  ✓ Propositional Logic Rules (7 rules)")
    print("  ✓ Weighted Graph + BFS Recommendations O(V+E)")
    print("  ✓ Proof by Mathematical Induction")
    print("█"*60 + "\n")


if __name__ == "__main__":
    run_demo()
