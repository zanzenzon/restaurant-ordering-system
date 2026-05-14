"""
order_tree.py — Tree Data Structure & Recursive Bill Computation
================================================================
Each order is represented as an n-ary tree:

    Order (root)
    ├── burger_combo  ($8.49)
    │   ├── burger    ($5.99)  ← included, price = 0 inside combo
    │   ├── fries     ($1.99)  ← included
    │   └── coke      ($1.49)  ← included
    └── ice_cream     ($2.49)

Recursive algorithm
-------------------
  total(node):
      if node is a LEAF:
          return node.effective_price
      else:
          return node.effective_price + Σ total(child) for child in node.children

  Correctness proved by strong induction on tree height (see report).

Complexity: O(n)  where n = total number of nodes in the tree.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from menu import MENU_ITEMS, COMBOS, get_item_price


@dataclass
class OrderNode:
    """
    A single node in the order tree.

    Parameters
    ----------
    name            : item / combo name
    effective_price : price charged for THIS node only.
                      For combo children it is 0 (already covered by parent).
    is_combo        : True if this node represents a combo deal.
    children        : sub-items (populated for combos).
    """
    name:            str
    effective_price: float
    is_combo:        bool               = False
    children:        list[OrderNode]    = field(default_factory=list)
    quantity:        int                = 1   # reserved for future multi-quantity support

    # ── Recursive total ─────────────────────────────────────────────

    def subtotal(self) -> float:
        """
        Recursively compute the subtotal rooted at this node.
        BASE CASE:  leaf node (no children)  → effective_price
        INDUCTIVE:  internal node            → effective_price + Σ child.subtotal()
        """
        if not self.children:                           # base case
            return self.effective_price * self.quantity
        return self.effective_price * self.quantity + sum(child.subtotal() for child in self.children)

    # ── Display helpers ──────────────────────────────────────────────

    def display(self, indent: int = 0, prefix: str = ""):
        tag = " [COMBO]" if self.is_combo else ""
        price_str = f"${self.effective_price:.2f}" if self.effective_price > 0 else "(included)"
        print(f"{'  ' * indent}{prefix}{self.name}{tag}  {price_str}")
        for child in self.children:
            self.display_child(child, indent + 1)

    def display_child(self, node: OrderNode, indent: int):
        tag = " [COMBO]" if node.is_combo else ""
        price_str = f"${node.effective_price:.2f}" if node.effective_price > 0 else "(included)"
        print(f"{'  ' * indent}├── {node.name}{tag}  {price_str}")
        for child in node.children:
            node.display_child(child, indent + 1)


class OrderTree:
    """
    Manages the full order as an n-ary tree rooted at a virtual 'root' node.
    Provides add / remove operations and delegates total computation to
    the recursive OrderNode.subtotal() method.
    """

    def __init__(self):
        self.root = OrderNode(name="ORDER", effective_price=0.0)
        self._item_nodes: dict[str, OrderNode] = {}   # quick lookup by name

    # ── Mutation ────────────────────────────────────────────────────

    def add_item(self, name: str) -> bool:
        """
        Add an item or combo to the order tree.
        Returns False if name not found in menu.
        """
        if name in self._item_nodes:
            print(f"  [Tree] '{name}' is already in the order. Use quantity update if needed.")
            return False

        if name in COMBOS:
            return self._add_combo(name)
        elif name in MENU_ITEMS:
            return self._add_single(name)
        else:
            print(f"  [Tree] ⚠  '{name}' not found in the menu.")
            return False

    def _add_single(self, name: str) -> bool:
        price = MENU_ITEMS[name]["price"]
        node = OrderNode(name=name, effective_price=price)
        self.root.children.append(node)
        self._item_nodes[name] = node
        print(f"  [Tree] Added '{name}' @ ${price:.2f}")
        return True

    def _add_combo(self, name: str) -> bool:
        combo = COMBOS[name]
        combo_node = OrderNode(name=name, effective_price=combo["price"], is_combo=True)

        # Add child nodes with effective_price = 0 (already covered by combo price)
        for item_name in [combo["base"]] + combo["includes"]:
            child = OrderNode(name=item_name, effective_price=0.0)
            combo_node.children.append(child)
            self._item_nodes[item_name] = child   # register children for membership check

        self.root.children.append(combo_node)
        self._item_nodes[name] = combo_node
        print(f"  [Tree] Added combo '{name}' @ ${combo['price']:.2f}  ({combo['desc']})")
        return True

    def remove_item(self, name: str) -> bool:
        """Remove a top-level item/combo node from the tree."""
        # Find and remove from root's children
        original_len = len(self.root.children)
        to_remove = None
        for node in self.root.children:
            if node.name == name:
                to_remove = node
                break

        if to_remove is None:
            print(f"  [Tree] ⚠  '{name}' is not a top-level order item.")
            return False

        self.root.children.remove(to_remove)
        # Un-register the node and its children
        self._item_nodes.pop(name, None)
        for child in to_remove.children:
            self._item_nodes.pop(child.name, None)
        print(f"  [Tree] Removed '{name}' from the order.")
        return True

    def contains(self, name: str) -> bool:
        return name in self._item_nodes

    def is_empty(self) -> bool:
        return len(self.root.children) == 0

    def item_names(self) -> set:
        """Return the set of all item names in the order (including combo children)."""
        return set(self._item_nodes.keys())

    # ── Totals ──────────────────────────────────────────────────────

    def subtotal(self) -> float:
        """Recursive subtotal via root node (O(n) traversal)."""
        return sum(child.subtotal() for child in self.root.children)

    def tax(self, rate: float = 0.14) -> float:
        """Compute tax at given rate (default 14%)."""
        return round(self.subtotal() * rate, 2)

    def discount(self, threshold: float = 20.0, pct: float = 0.10) -> float:
        """
        Logic rule: IF subtotal > threshold THEN apply discount.
        Returns the discount amount (0 if rule not satisfied).
        """
        sub = self.subtotal()
        if sub > threshold:
            return round(sub * pct, 2)
        return 0.0

    def total(self, tax_rate: float = 0.14, discount_threshold: float = 20.0) -> float:
        sub  = self.subtotal()
        disc = self.discount(threshold=discount_threshold)
        tax  = self.tax(rate=tax_rate)
        return round(sub - disc + tax, 2)

    # ── Display ─────────────────────────────────────────────────────

    def display(self):
        if self.is_empty():
            print("  (Order is empty)")
            return

        print("\n  Order Tree:")
        print("  " + "─" * 45)
        for node in self.root.children:
            node.display(indent=2)

        sub  = self.subtotal()
        disc = self.discount()
        tax  = self.tax()
        tot  = self.total()

        print("  " + "─" * 45)
        print(f"  {'Subtotal:':<20} ${sub:.2f}")
        if disc > 0:
            print(f"  {'Discount (10%):':<20} -${disc:.2f}  ✓ [Rule: subtotal > $20]")
        print(f"  {'Tax (14%):':<20} ${tax:.2f}")
        print(f"  {'TOTAL:':<20} ${tot:.2f}")
        print()
