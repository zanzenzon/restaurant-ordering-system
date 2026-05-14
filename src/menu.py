"""
menu.py — Restaurant Menu Data & Set Operations
================================================
Uses set theory: items grouped into named sets by category.
Supports membership queries, category intersection, and filtering.
"""

# ── Menu items: eachx entry is a dict with price, category, description ──
MENU_ITEMS = {
    # Main Course
    "burger":      {"price": 5.99,  "category": "main",    "desc": "Beef burger with lettuce & tomato"},
    "pasta":       {"price": 6.49,  "category": "main",    "desc": "Creamy Alfredo pasta"},
    "pizza":       {"price": 7.99,  "category": "main",    "desc": "Margherita pizza (6 slices)"},
    "sandwich":    {"price": 4.49,  "category": "main",    "desc": "Grilled chicken sandwich"},
    "shawarma":    {"price": 5.49,  "category": "main",    "desc": "Chicken shawarma wrap"},
    # Sides
    "fries":       {"price": 1.99,  "category": "side",    "desc": "Crispy golden fries"},
    "salad":       {"price": 2.49,  "category": "side",    "desc": "Fresh garden salad"},
    "onion_rings": {"price": 2.29,  "category": "side",    "desc": "Crunchy onion rings"},
    "coleslaw":    {"price": 1.79,  "category": "side",    "desc": "Creamy coleslaw"},
    # Beverages
    "coke":        {"price": 1.49,  "category": "drink",   "desc": "Coca-Cola (medium)"},
    "juice":       {"price": 1.99,  "category": "drink",   "desc": "Fresh orange juice"},
    "water":       {"price": 0.99,  "category": "drink",   "desc": "Bottled water"},
    "milkshake":   {"price": 2.99,  "category": "drink",   "desc": "Chocolate milkshake"},
    # Desserts
    "ice_cream":   {"price": 2.49,  "category": "dessert", "desc": "Vanilla ice cream scoop"},
    "brownie":     {"price": 2.99,  "category": "dessert", "desc": "Warm chocolate brownie"},
    "cheesecake":  {"price": 3.49,  "category": "dessert", "desc": "New York cheesecake slice"},
}

# ── Combo definitions: base item + included sub-items + combo price ──
COMBOS = {
    "burger_combo": {
        "base":     "burger",
        "includes": ["fries", "coke"],
        "price":    8.49,
        "desc":     "Burger + Fries + Coke",
    },
    "pasta_combo": {
        "base":     "pasta",
        "includes": ["salad", "juice"],
        "price":    9.49,
        "desc":     "Pasta + Salad + Juice",
    },
    "shawarma_combo": {
        "base":     "shawarma",
        "includes": ["fries", "coke"],
        "price":    7.99,
        "desc":     "Shawarma + Fries + Coke",
    },
}

# ── Set-theory helpers ─────────────────────────────────────────────────

def get_category_set(category: str) -> set:
    """Return the set of item names belonging to a given category."""
    return {name for name, info in MENU_ITEMS.items() if info["category"] == category}


def get_all_categories() -> set:
    """Return the set of all unique categories in the menu."""
    return {info["category"] for info in MENU_ITEMS.values()}


def items_in_categories(cats: list) -> set:
    """
    Return the union of items across multiple categories.
    Demonstrates set UNION operation.
    """
    result = set()
    for cat in cats:
        result = result | get_category_set(cat)
    return result


def item_exists(name: str) -> bool:
    return name in MENU_ITEMS or name in COMBOS


def get_item_price(name: str) -> float:
    if name in COMBOS:
        return COMBOS[name]["price"]
    if name in MENU_ITEMS:
        return MENU_ITEMS[name]["price"]
    raise KeyError(f"Item '{name}' not found in menu.")


def display_menu():
    """Pretty-print the full menu, grouped by category."""
    print("\n" + "═" * 55)
    print("           🍽️  RESTAURANT ORDERING SYSTEM")
    print("═" * 55)

    categories = {"main": "🍔 Main Course", "side": "🍟 Sides",
                  "drink": "🥤 Beverages",  "dessert": "🍰 Desserts"}

    for cat_key, cat_label in categories.items():
        items = {k: v for k, v in MENU_ITEMS.items() if v["category"] == cat_key}
        if items:
            print(f"\n  {cat_label}")
            print("  " + "─" * 50)
            for name, info in items.items():
                print(f"  {name:<14} ${info['price']:.2f}   {info['desc']}")

    print(f"\n  🎁 Combo Deals")
    print("  " + "─" * 50)
    for name, info in COMBOS.items():
        print(f"  {name:<20} ${info['price']:.2f}   {info['desc']}")

    print("\n" + "═" * 55)
