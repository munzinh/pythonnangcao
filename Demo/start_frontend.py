#!/usr/bin/env python3
"""
Frontend startup script.

This script sets up the Python path and starts the Tkinter GUI.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the GUI
from frontend.gui import main

if __name__ == '__main__':
    main()
