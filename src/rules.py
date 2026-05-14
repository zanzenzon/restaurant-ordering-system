"""
rules.py — Propositional Logic & Order Validation Rules
========================================================
Each rule is a named propositional formula.  Rules are checked after
every add/remove operation and before order confirmation.

Rule schema
-----------
  name      : human-readable label
  condition : λ(order_set, subtotal) → bool   — antecedent P
  action    : λ(order_set)           → str    — consequent Q (message)
  blocking  : if True the rule PREVENTS confirmation when violated

Logical form of each rule is documented inline as:
  P → Q   (if P then Q)
  ¬P ∨ Q  (equivalent disjunction form)
"""

from menu import MENU_ITEMS, COMBOS, get_category_set


# ── Rule definitions ──────────────────────────────────────────────────

RULES = [
    {
        "name": "R1: Burger → suggest fries",
        "logic": "burger ∈ ORDER ∧ fries ∉ ORDER → recommend fries",
        "blocking": False,
        "check": lambda items, sub: "burger" in items and "fries" not in items
                                    and "burger_combo" not in items,
        "message": "💡 You have a burger but no fries! Consider adding fries ($1.99).",
    },
    {
        "name": "R2: Pizza → suggest coke",
        "logic": "pizza ∈ ORDER ∧ coke ∉ ORDER → recommend coke",
        "blocking": False,
        "check": lambda items, sub: "pizza" in items and "coke" not in items,
        "message": "💡 Pizza pairs great with a Coke ($1.49)!",
    },
    {
        "name": "R3: No drink warning",
        "logic": "ORDER ∩ DRINKS = ∅ → warn",
        "blocking": False,
        "check": lambda items, sub: len(items & get_category_set("drink")) == 0,
        "message": "⚠  Your order has no drink. Add a beverage?",
    },
    {
        "name": "R4: Combo + duplicate item",
        "logic": "burger_combo ∈ ORDER ∧ burger ∈ ORDER → conflict",
        "blocking": True,
        "check": lambda items, sub: "burger_combo" in items and "burger" in items,
        "message": "❌ Conflict: 'burger' is already included in 'burger_combo'.",
    },
    {
        "name": "R5: Discount eligibility",
        "logic": "subtotal > 20 → discount := 10%",
        "blocking": False,
        "check": lambda items, sub: sub > 20.0,
        "message": "🎉 Your order qualifies for a 10% discount!",
    },
    {
        "name": "R6: Large order → suggest shawarma_combo",
        "logic": "|ORDER| ≥ 4 ∧ shawarma_combo ∉ ORDER → recommend combo",
        "blocking": False,
        "check": lambda items, sub: len(items) >= 4 and "shawarma_combo" not in items,
        "message": "💡 Big order! The Shawarma Combo saves you money.",
    },
    {
        "name": "R7: Empty order block",
        "logic": "|ORDER| = 0 → block confirm",
        "blocking": True,
        "check": lambda items, sub: len(items) == 0,
        "message": "❌ Cannot confirm an empty order. Please add items first.",
    },
]


def evaluate_rules(ordered_items: set, subtotal: float,
                   blocking_only: bool = False) -> list[dict]:
    """
    Evaluate all rules against the current order state.

    Parameters
    ----------
    ordered_items : set of all item names in the order
    subtotal      : current order subtotal (for financial rules)
    blocking_only : if True, return only rules that block confirmation

    Returns
    -------
    List of triggered rule dicts (with 'name', 'message', 'blocking').
    """
    triggered = []
    for rule in RULES:
        if blocking_only and not rule["blocking"]:
            continue
        if rule["check"](ordered_items, subtotal):
            triggered.append({
                "name":     rule["name"],
                "logic":    rule["logic"],
                "message":  rule["message"],
                "blocking": rule["blocking"],
            })
    return triggered


def print_rule_check(ordered_items: set, subtotal: float):
    """Pretty-print all triggered rules."""
    triggered = evaluate_rules(ordered_items, subtotal)
    if not triggered:
        print("  ✅ All logic rules pass. No issues found.")
        return

    print("\n  Logic Rule Evaluation:")
    print("  " + "─" * 50)
    for r in triggered:
        kind = "BLOCK" if r["blocking"] else "INFO "
        print(f"  [{kind}] {r['name']}")
        print(f"         Formula: {r['logic']}")
        print(f"         {r['message']}")
    print()


def has_blocking_violation(ordered_items: set, subtotal: float) -> bool:
    """Return True if any blocking rule is triggered (prevents confirmation)."""
    blocking = evaluate_rules(ordered_items, subtotal, blocking_only=True)
    return len(blocking) > 0
