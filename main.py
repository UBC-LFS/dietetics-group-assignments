import tkinter as tk

from project_matching_gui import ProjectMatchingGUI 
from scripts.script import run_script

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root)
    root.mainloop()

# TODO Priorities:
# 1. match the variables from the popup to the matching algorithm
# 3. button to run the matching algorithm in scripts/script.py
# 4. figure out where to save the csv file -> we will have 2 different ones, one for canvas group matching and one for profs
# 5. (?) Optional for now: create another button to validate csv file before matching