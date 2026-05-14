"""
ui.py — Command-Line Interface for the Restaurant Ordering System
=================================================================
Integrates FSM, OrderTree, RecommendationGraph, and Rules into a
clean interactive loop.
"""

import os
import sys

# Make sure src/ is on the path when running from project root
sys.path.insert(0, os.path.dirname(__file__))

from fsm             import FSM, State
from order_tree      import OrderTree
from recommend_graph import RecommendationGraph
from rules           import print_rule_check, has_blocking_violation, evaluate_rules
from menu            import display_menu, MENU_ITEMS, COMBOS


# ── Colour helpers (ANSI — degrade gracefully on Windows) ─────────────

def bold(s):   return f"\033[1m{s}\033[0m"
def green(s):  return f"\033[92m{s}\033[0m"
def yellow(s): return f"\033[93m{s}\033[0m"
def red(s):    return f"\033[91m{s}\033[0m"
def cyan(s):   return f"\033[96m{s}\033[0m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ── Main ordering loop ────────────────────────────────────────────────

def run():
    fsm   = FSM()
    tree  = OrderTree()
    graph = RecommendationGraph()

    print(bold("\n  Welcome to the Restaurant Ordering System"))
    print("  (Discrete Mathematics Project — FSM + Tree + Graph + Logic)")
    print()

    # ── Start the FSM ────────────────────────────────────────────────
    fsm.transition("start")

    while True:
        print()
        print(cyan(f"  ┌─ {fsm.describe()}"))

        # ── STATE: ORDERING ──────────────────────────────────────────
        if fsm.is_ordering():
            print("  │  Commands: [menu] [add <item>] [remove <item>] [order] [review] [cancel]")
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "menu":
                display_menu()

            elif cmd.startswith("add "):
                item = cmd[4:].strip()
                ok = tree.add_item(item)
                if ok:
                    fsm.transition("add_item")
                    # Show live rule hints after each add
                    triggered = evaluate_rules(tree.item_names(), tree.subtotal(), blocking_only=False)
                    info_rules = [r for r in triggered if not r["blocking"]]
                    if info_rules:
                        for r in info_rules:
                            print(f"  {r['message']}")
                    # Show quick recommendations
                    graph.print_recommendations(tree.item_names(), top_n=3)

            elif cmd.startswith("remove "):
                item = cmd[7:].strip()
                ok = tree.remove_item(item)
                if ok:
                    fsm.transition("remove_item")

            elif cmd == "order":
                tree.display()

            elif cmd == "review":
                if tree.is_empty():
                    print(red("  ⚠  Order is empty. Add items first."))
                else:
                    fsm.transition("review")

            elif cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Unknown command. Type 'menu' to see the menu."))

        # ── STATE: REVIEWING ─────────────────────────────────────────
        elif fsm.is_reviewing():
            tree.display()
            print_rule_check(tree.item_names(), tree.subtotal())
            print("  │  Commands: [confirm] [edit] [cancel]")
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "confirm":
                if has_blocking_violation(tree.item_names(), tree.subtotal()):
                    print(red("  ❌ Cannot confirm — resolve the issues above first."))
                else:
                    fsm.transition("confirm")

            elif cmd == "edit":
                fsm.transition("edit")

            elif cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Commands: confirm / edit / cancel"))

        # ── STATE: PAYMENT ────────────────────────────────────────────
        elif fsm.is_payment():
            total = tree.total()
            print(f"\n  Total due: {bold(f'${total:.2f}')}")
            print("  │  Commands: [pay] [cancel]")
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "pay":
                fsm.transition("pay")

            elif cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Commands: pay / cancel"))

        # ── STATE: COMPLETED ──────────────────────────────────────────
        elif fsm.is_completed():
            print(green("\n  🎉 Order completed! Thank you for dining with us.\n"))
            print("  Your order summary:")
            tree.display()
            print("  FSM Transition History:")
            fsm.print_history()
            print("  Commands: [new] [exit]")
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "new":
                tree  = OrderTree()
                graph = RecommendationGraph()
                fsm.transition("start")
            elif cmd == "exit":
                print("  Goodbye!\n")
                break

        # ── STATE: CANCELLED ──────────────────────────────────────────
        elif fsm.is_cancelled():
            print(red("\n  Order cancelled."))
            print("  Commands: [new] [exit]")
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "new":
                tree  = OrderTree()
                graph = RecommendationGraph()
                fsm.transition("start")
            elif cmd == "exit":
                print("  Goodbye!\n")
                break


if __name__ == "__main__":
    run()
