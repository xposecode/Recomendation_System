import sys
import os

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Test imports
try:
    import tkinter
    print("✓ tkinter imported successfully")
except ImportError as e:
    print(f"✗ tkinter import failed: {e}")

try:
    from load_dataset_module import DataLoader
    print("✓ DataLoader imported successfully")
except ImportError as e:
    print(f"✗ DataLoader import failed: {e}")

try:
    from similarity_module import SimilarityCalculator
    print("✓ SimilarityCalculator imported successfully")
except ImportError as e:
    print(f"✗ SimilarityCalculator import failed: {e}")

try:
    from user_interface_module import MusicAppGUI
    print("✓ MusicAppGUI imported successfully")
except ImportError as e:
    print(f"✗ MusicAppGUI import failed: {e}")

# Run a simple test
import tkinter as tk
print("\nTesting basic tkinter window...")
root = tk.Tk()
root.withdraw()  # Don't show it
print("✓ Basic tkinter window created")
root.destroy()