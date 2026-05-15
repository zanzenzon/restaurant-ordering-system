"""
tests/test_all.py — Unit Tests
================================
Run with:   python -m pytest tests/ -v
Or:         python tests/test_all.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from fsm             import FSM, State
from order_tree      import OrderTree, OrderNode
from recommended_graph import RecommendationGraph
from rules           import evaluate_rules, has_blocking_violation
from menu            import get_category_set, items_in_categories, get_item_price


class TestFSM(unittest.TestCase):

    def setUp(self):
        self.fsm = FSM()

    def test_initial_state(self):
        self.assertEqual(self.fsm.state, State.IDLE)

    def test_valid_transition_start(self):
        result = self.fsm.transition("start")
        self.assertTrue(result)
        self.assertEqual(self.fsm.state, State.ORDERING)

    def test_invalid_transition_blocked(self):
        # Cannot 'pay' from IDLE
        result = self.fsm.transition("pay")
        self.assertFalse(result)
        self.assertEqual(self.fsm.state, State.IDLE)

    def test_full_happy_path(self):
        self.fsm.transition("start")
        self.fsm.transition("add_item")
        self.fsm.transition("review")
        self.fsm.transition("confirm")
        self.fsm.transition("pay")
        self.assertEqual(self.fsm.state, State.COMPLETED)

    def test_cancel_from_ordering(self):
        self.fsm.transition("start")
        self.fsm.transition("cancel")
        self.assertEqual(self.fsm.state, State.CANCELLED)

    def test_history_records_transitions(self):
        self.fsm.transition("start")
        self.fsm.transition("add_item")
        self.assertEqual(len(self.fsm.history), 2)


class TestOrderTree(unittest.TestCase):

    def setUp(self):
        self.tree = OrderTree()

    def test_add_single_item(self):
        self.tree.add_item("fries")
        self.assertIn("fries", self.tree.item_names())

    def test_add_combo(self):
        self.tree.add_item("burger_combo")
        self.assertIn("burger_combo", self.tree.item_names())
        # children registered too
        self.assertIn("burger", self.tree.item_names())
        self.assertIn("fries",  self.tree.item_names())
        self.assertIn("coke",   self.tree.item_names())

    def test_remove_item(self):
        self.tree.add_item("pasta")
        self.tree.remove_item("pasta")
        self.assertNotIn("pasta", self.tree.item_names())

    def test_recursive_subtotal_leaf(self):
        node = OrderNode(name="test", effective_price=5.0)
        self.assertAlmostEqual(node.subtotal(), 5.0)

    def test_recursive_subtotal_tree(self):
        parent = OrderNode(name="combo", effective_price=8.49, is_combo=True)
        parent.children = [
            OrderNode(name="burger", effective_price=0.0),
            OrderNode(name="fries",  effective_price=0.0),
        ]
        # subtotal = 8.49 (children are 0)
        self.assertAlmostEqual(parent.subtotal(), 8.49)

    def test_discount_applied_over_threshold(self):
        self.tree.add_item("burger_combo")  # $8.49
        self.tree.add_item("pasta")         # $6.49
        self.tree.add_item("pizza")         # $7.99
        # subtotal = 22.97 > 20 → 10% discount
        self.assertGreater(self.tree.discount(), 0)

    def test_no_discount_under_threshold(self):
        self.tree.add_item("fries")   # $1.99
        self.assertEqual(self.tree.discount(), 0.0)

    def test_empty_tree(self):
        self.assertTrue(self.tree.is_empty())
        self.assertAlmostEqual(self.tree.subtotal(), 0.0)


class TestRecommendationGraph(unittest.TestCase):

    def setUp(self):
        self.graph = RecommendationGraph()

    def test_adjacency_list_populated(self):
        self.assertIn("burger", self.graph.adj)
        self.assertGreater(len(self.graph.adj["burger"]), 0)

    def test_bfs_recommends_unordered(self):
        ordered = {"burger"}
        recs = self.graph.recommend(ordered, top_n=3)
        names = [r["name"] for r in recs]
        self.assertNotIn("burger", names)   # never recommends what's already ordered

    def test_bfs_top_n_respected(self):
        ordered = {"burger", "pasta"}
        recs = self.graph.recommend(ordered, top_n=2)
        self.assertLessEqual(len(recs), 2)

    def test_empty_order_recommendations(self):
        recs = self.graph.recommend(set(), top_n=3)
        self.assertEqual(recs, [])


class TestRules(unittest.TestCase):

    def test_empty_order_blocks(self):
        self.assertTrue(has_blocking_violation(set(), 0.0))

    def test_no_drink_info_rule(self):
        triggered = evaluate_rules({"burger", "fries"}, 7.98)
        names = [r["name"] for r in triggered]
        self.assertTrue(any("No drink" in n for n in names))

    def test_discount_rule_triggers(self):
        triggered = evaluate_rules({"burger_combo", "pasta", "pizza"}, 22.97)
        names = [r["name"] for r in triggered]
        self.assertTrue(any("Discount" in n for n in names))

    def test_combo_duplicate_blocks(self):
        # burger_combo already includes burger → conflict
        triggered = evaluate_rules({"burger_combo", "burger"}, 8.49)
        blocking = [r for r in triggered if r["blocking"] and "Combo" in r["name"]]
        self.assertGreater(len(blocking), 0)


class TestMenuSets(unittest.TestCase):

    def test_category_set_main(self):
        mains = get_category_set("main")
        self.assertIn("burger", mains)
        self.assertIn("pasta",  mains)
        self.assertNotIn("coke", mains)

    def test_union_of_categories(self):
        union = items_in_categories(["main", "drink"])
        self.assertIn("burger", union)
        self.assertIn("coke",   union)

    def test_item_price(self):
        self.assertAlmostEqual(get_item_price("burger"), 5.99)
        self.assertAlmostEqual(get_item_price("burger_combo"), 8.49)


if __name__ == "__main__":
    unittest.main(verbosity=2)
