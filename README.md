# 🍽️ Restaurant Ordering System

> A Discrete Mathematics project implementing a Restaurant Ordering System using
> **Finite-State Machines**, **N-ary Trees with Recursive Algorithms**, **Weighted Graphs (BFS)**, **Propositional Logic Rules**, and **Set Theory**.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Discrete Math Concepts](#discrete-math-concepts)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Module Descriptions](#module-descriptions)
- [Sample Output](#sample-output)
- [Team](#team)

---

## Overview

This system simulates a restaurant ordering workflow from a customer's perspective. It is built entirely around fundamental **Discrete Mathematics** structures, making each concept tangible and interactive.

**Key Features:**
- Interactive CLI ordering interface
- Full FSM order lifecycle (6 states, 12 transitions)
- Recursive bill computation on an n-ary tree (proved correct by induction)
- BFS-based item recommendations from a co-occurrence graph
- Propositional logic rule engine (7 rules)
- Set-theoretic menu organization

---

## Discrete Math Concepts

| Concept | Where Used | Module |
|---------|-----------|--------|
| **Finite-State Machine** | Order lifecycle: IDLE → ORDERING → REVIEWING → PAYMENT → COMPLETED / CANCELLED | `fsm.py` |
| **N-ary Tree** | Order structure (combos as parent nodes, items as leaves) | `order_tree.py` |
| **Recursion + Induction** | `total(node) = price + Σ total(child)` — proved correct by strong induction | `order_tree.py` |
| **Weighted Graph** | Co-occurrence graph of menu items | `recommend_graph.py` |
| **BFS** | Recommendation engine traversal O(V+E) | `recommend_graph.py` |
| **Set Theory** | Menu categories as sets; union/intersection operations | `menu.py` |
| **Propositional Logic** | Order validation rules (P → Q formulas) | `rules.py` |

---

## Project Structure

```
restaurant_ordering_system/
├── main.py                  # Entry point (interactive mode)
├── demo.py                  # Automated demo (for presentation)
├── README.md
├── src/
│   ├── menu.py              # Menu data + set theory helpers
│   ├── fsm.py               # Finite-State Machine
│   ├── order_tree.py        # N-ary tree + recursive total
│   ├── recommend_graph.py   # Co-occurrence graph + BFS
│   ├── rules.py             # Propositional logic rule engine
│   └── ui.py                # CLI interface + integration
├── tests/
│   └── test_all.py          # Unit tests (pytest or unittest)
└── docs/
    └── (report assets)
```

---

## How to Run

### Requirements
- Python 3.8 or higher
- No external packages required (standard library only)

### Interactive Mode
```bash
python main.py
```

### Automated Demo (Presentation Mode)
```bash
python demo.py
```

### Run Tests
```bash
python -m pytest tests/ -v
# or
python tests/test_all.py
```

---

## Module Descriptions

### `src/menu.py` — Set Theory
Defines the full menu as a Python dictionary and provides set-theoretic operations:
```python
get_category_set("main")          # → {"burger", "pasta", "pizza", ...}
items_in_categories(["main","drink"])  # → set union
```

### `src/fsm.py` — Finite-State Machine
```
States:  IDLE, ORDERING, REVIEWING, PAYMENT, COMPLETED, CANCELLED
Events:  start, add_item, remove_item, review, edit, confirm, pay, cancel
```
The FSM is encoded as a transition table `δ: State × Event → State`.

### `src/order_tree.py` — Recursive Tree
Each order is an n-ary tree. The recursive total algorithm is:
```
total(node):
    if leaf:  return node.price
    else:     return node.price + Σ total(child)
```
Complexity: **O(n)** where n = total nodes.

**Proof by Strong Induction:**
- *Base case* (height 0): `total(leaf) = leaf.price` ✓
- *Inductive step*: Assume correct for all children → correct for parent ✓

### `src/recommend_graph.py` — Graph + BFS
Vertices = menu items. Edges = co-occurrence frequency in past orders.
BFS from ordered items finds unordered neighbors ranked by weight.
Complexity: **O(V + E)**.

### `src/rules.py` — Propositional Logic
Seven rules encoded as propositional formulas:
```
R1: burger ∈ ORDER ∧ fries ∉ ORDER → recommend fries
R3: ORDER ∩ DRINKS = ∅ → warn
R4: burger_combo ∈ ORDER ∧ burger ∈ ORDER → BLOCK (conflict)
R5: subtotal > 20 → apply 10% discount
R7: |ORDER| = 0 → BLOCK confirmation
```

---

## Sample Output

```
  [FSM] IDLE ──(start)──▶ ORDERING
  [Tree] Added 'burger_combo' @ $8.49  (Burger + Fries + Coke)
  💡 You have a burger but no fries! Consider adding fries ($1.99).

  🌟 Customers who ordered this also ordered:
  ─────────────────────────────────────────────────
  1. onion_rings   $2.29   Crunchy onion rings
  2. milkshake     $2.99   Chocolate milkshake
  3. salad         $2.49   Fresh garden salad

  Order Tree:
  ─────────────────────────────────────────────────
    burger_combo [COMBO]  $8.49
      ├── burger    (included)
      ├── fries     (included)
      └── coke      (included)
    pasta           $6.49
  ─────────────────────────────────────────────────
  Subtotal:            $14.98
  Tax (14%):           $2.10
  TOTAL:               $17.08
```

---

## Team

| # | Name | Role |
|---|------|------|
| 1 | — | Team Leader |
| 2 | — | FSM Design |
| 3 | — | Logic & Rules |
| 4 | — | Graph & BFS |
| 5 | — | Tree & Recursion |
| 6 | — | UI Design |
| 7 | — | UI Design |
| 8 | — | Backend Integration |
| 9 | — | Backend Integration |
| 10 | — | Testing & Documentation |

---

## References

1. Rosen, K. H. (2019). *Discrete Mathematics and Its Applications* (8th ed.). McGraw-Hill.
2. Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
3. Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
4. Cormen, T. H., et al. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
