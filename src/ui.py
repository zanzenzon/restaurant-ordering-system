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
from recommended_graph import RecommendationGraph
from rules           import print_rule_check, has_blocking_violation, evaluate_rules
from menu            import display_menu, MENU_ITEMS, COMBOS, get_item_name


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
            print("  │  " + cyan("1. Menu") + "  " + cyan("2. Add Item") + "  " + cyan("3. Remove Item") + "  " + cyan("4. View Order") + "  " + cyan("5. Review") + "  " + cyan("6. Cancel"))
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "1" or cmd == "menu":
                display_menu()

            elif cmd == "2" or cmd.startswith("2 ") or cmd.startswith("add "):
                if cmd == "2" or cmd == "add":
                    item_input = input("  │  Enter item name or number: ").strip().lower()
                elif cmd.startswith("2 "):
                    item_input = cmd[2:].strip()
                else:
                    item_input = cmd[4:].strip()
                
                if not item_input:
                    print(yellow("  ⚠  No item specified."))
                    continue

                item = get_item_name(item_input)

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

            elif cmd == "3" or cmd.startswith("3 ") or cmd.startswith("remove "):
                if cmd == "3" or cmd == "remove":
                    item_input = input("  │  Enter item name or number to remove: ").strip().lower()
                elif cmd.startswith("3 "):
                    item_input = cmd[2:].strip()
                else:
                    item_input = cmd[7:].strip()

                if not item_input:
                    print(yellow("  ⚠  No item specified."))
                    continue

                item = get_item_name(item_input)

                ok = tree.remove_item(item)
                if ok:
                    fsm.transition("remove_item")

            elif cmd == "4" or cmd == "order":
                tree.display()

            elif cmd == "5" or cmd == "review":
                if tree.is_empty():
                    print(red("  ⚠  Order is empty. Add items first."))
                else:
                    fsm.transition("review")

            elif cmd == "6" or cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Unknown command. Use numbers 1-6 or type the command."))

        # ── STATE: REVIEWING ─────────────────────────────────────────
        elif fsm.is_reviewing():
            tree.display()
            print_rule_check(tree.item_names(), tree.subtotal())
            print("  │  " + cyan("1. Confirm") + "  " + cyan("2. Edit") + "  " + cyan("3. Cancel"))
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "1" or cmd == "confirm":
                if has_blocking_violation(tree.item_names(), tree.subtotal()):
                    print(red("  ❌ Cannot confirm — resolve the issues above first."))
                else:
                    fsm.transition("confirm")

            elif cmd == "2" or cmd == "edit":
                fsm.transition("edit")

            elif cmd == "3" or cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Unknown command. Use numbers 1-3 or type confirm/edit/cancel."))

        # ── STATE: PAYMENT ────────────────────────────────────────────
        elif fsm.is_payment():
            total = tree.total()
            print(f"\n  Total due: {bold(f'${total:.2f}')}")
            print("  │  " + cyan("1. Pay") + "  " + cyan("2. Cancel"))
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "1" or cmd == "pay":
                fsm.transition("pay")

            elif cmd == "2" or cmd == "cancel":
                fsm.transition("cancel")

            else:
                print(yellow("  Unknown command. Use numbers 1-2 or type pay/cancel."))

        # ── STATE: COMPLETED ──────────────────────────────────────────
        elif fsm.is_completed():
            print(green("\n  🎉 Order completed! Thank you for dining with us.\n"))
            print("  Your order summary:")
            tree.display()
            print("  FSM Transition History:")
            fsm.print_history()
            print("  " + cyan("1. New Order") + "  " + cyan("2. Exit"))
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "1" or cmd == "new":
                tree  = OrderTree()
                graph = RecommendationGraph()
                fsm.transition("start")
            elif cmd == "2" or cmd == "exit":
                print("  Goodbye!\n")
                break
            else:
                print(yellow("  Unknown command. Use numbers 1-2 or type new/exit."))

        # ── STATE: CANCELLED ──────────────────────────────────────────
        elif fsm.is_cancelled():
            print(red("\n  Order cancelled."))
            print("  " + cyan("1. New Order") + "  " + cyan("2. Exit"))
            cmd = input("  └─▶ ").strip().lower()

            if cmd == "1" or cmd == "new":
                tree  = OrderTree()
                graph = RecommendationGraph()
                fsm.transition("start")
            elif cmd == "2" or cmd == "exit":
                print("  Goodbye!\n")
                break
            else:
                print(yellow("  Unknown command. Use numbers 1-2 or type new/exit."))


if __name__ == "__main__":
    run()
