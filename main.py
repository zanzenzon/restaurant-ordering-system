"""
main.py — Entry Point
=====================
Run from the project root:
    python main.py
"""

from src.ui import run
import sys
import os

# Add src to sys.path so imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# pyrefly: ignore [missing-import]
from recommended_graph import RecommendationGraph
from ui import run

if __name__ == "__main__":
    run()
