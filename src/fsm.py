"""
fsm.py — Finite-State Machine for Order Processing
====================================================
States and transitions model the full lifecycle of a restaurant order.

States
------
  S0  IDLE        System is waiting; no active order.
  S1  ORDERING    Customer is adding / removing items.
  S2  REVIEWING   Customer is reviewing the order before confirming.
  S3  PAYMENT     Order confirmed; awaiting payment.
  S4  COMPLETED   Payment received; order done.
  S5  CANCELLED   Order was cancelled at any point before payment.

Transition Table
----------------
  Current State  │  Event          │  Next State
  ───────────────┼─────────────────┼─────────────
  IDLE           │  start          │  ORDERING
  ORDERING       │  add_item       │  ORDERING
  ORDERING       │  remove_item    │  ORDERING
  ORDERING       │  review         │  REVIEWING
  ORDERING       │  cancel         │  CANCELLED
  REVIEWING      │  confirm        │  PAYMENT
  REVIEWING      │  edit           │  ORDERING
  REVIEWING      │  cancel         │  CANCELLED
  PAYMENT        │  pay            │  COMPLETED
  PAYMENT        │  cancel         │  CANCELLED
  COMPLETED      │  start          │  ORDERING   (new order)
  CANCELLED      │  start          │  ORDERING   (retry)
"""

from enum import Enum, auto


class State(Enum):
    IDLE       = "IDLE"
    ORDERING   = "ORDERING"
    REVIEWING  = "REVIEWING"
    PAYMENT    = "PAYMENT"
    COMPLETED  = "COMPLETED"
    CANCELLED  = "CANCELLED"


# Transition table: (current_state, event) → next_state
TRANSITIONS = {
    (State.IDLE,      "start"):       State.ORDERING,
    (State.ORDERING,  "add_item"):    State.ORDERING,
    (State.ORDERING,  "remove_item"): State.ORDERING,
    (State.ORDERING,  "review"):      State.REVIEWING,
    (State.ORDERING,  "cancel"):      State.CANCELLED,
    (State.REVIEWING, "confirm"):     State.PAYMENT,
    (State.REVIEWING, "edit"):        State.ORDERING,
    (State.REVIEWING, "cancel"):      State.CANCELLED,
    (State.PAYMENT,   "pay"):         State.COMPLETED,
    (State.PAYMENT,   "cancel"):      State.CANCELLED,
    (State.COMPLETED, "start"):       State.ORDERING,
    (State.CANCELLED, "start"):       State.ORDERING,
}

# Human-readable descriptions for each state
STATE_DESCRIPTIONS = {
    State.IDLE:      "System is idle. Ready to take a new order.",
    State.ORDERING:  "Order in progress. Add or remove items.",
    State.REVIEWING: "Reviewing order. Confirm or go back to edit.",
    State.PAYMENT:   "Awaiting payment.",
    State.COMPLETED: "Order complete. Thank you!",
    State.CANCELLED: "Order cancelled.",
}


class FSM:
    """
    Finite-State Machine controlling the restaurant order workflow.

    Attributes
    ----------
    state        : current State
    history      : list of (event, from_state, to_state) tuples for the report log
    """

    def __init__(self):
        self.state: State = State.IDLE
        self.history: list[tuple] = []

    # ── Core transition ────────────────────────────────────────────────

    def transition(self, event: str) -> bool:
        """
        Attempt to transition on 'event'.
        Returns True on success, False if the event is invalid for the
        current state (FSM stays in the same state).
        """
        key = (self.state, event)
        if key not in TRANSITIONS:
            print(f"  [FSM] ⚠  Event '{event}' is invalid in state '{self.state.value}'.")
            return False

        from_state = self.state
        self.state = TRANSITIONS[key]
        self.history.append((event, from_state, self.state))
        print(f"  [FSM] {from_state.value} ──({event})──▶ {self.state.value}")
        return True

    # ── Convenience queries ────────────────────────────────────────────

    def is_ordering(self) -> bool:
        return self.state == State.ORDERING

    def is_reviewing(self) -> bool:
        return self.state == State.REVIEWING

    def is_payment(self) -> bool:
        return self.state == State.PAYMENT

    def is_completed(self) -> bool:
        return self.state == State.COMPLETED

    def is_cancelled(self) -> bool:
        return self.state == State.CANCELLED

    def describe(self) -> str:
        return f"State: {self.state.value} — {STATE_DESCRIPTIONS[self.state]}"

    # ── History / report ──────────────────────────────────────────────

    def print_history(self):
        print("\n  FSM Transition Log:")
        print("  " + "─" * 50)
        for i, (event, frm, to) in enumerate(self.history, 1):
            print(f"  {i:>2}. {frm.value:<12} ──({event})──▶ {to.value}")
        print()

    def print_transition_table(self):
        """Print the full FSM transition table — useful for the report."""
        print("\n  Transition Table (δ : State × Event → State)")
        print("  " + "─" * 55)
        print(f"  {'Current State':<14} {'Event':<16} {'Next State'}")
        print("  " + "─" * 55)
        for (state, event), next_state in TRANSITIONS.items():
            print(f"  {state.value:<14} {event:<16} {next_state.value}")
        print()
