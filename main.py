"""
main.py — Entry Point
=====================
Run from the project root:
    python main.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ui import run

if __name__ == "__main__":
    run()
