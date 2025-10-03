import tkinter as tk
from project_matching_gui import ProjectMatchingGUI 
from scripts.script import run_script

def on_data_extracted(data):
    """
    Callback function that receives data from the project_matching_gui.py
    and passes it to script.py for processing
    
    Args:
        data: The extracted data from the GUI
    """
    csv_file_path = data.get('csv_file_path')
    capacity = data.get("capacity")
    exceptions = data.get("capacity_exceptions")
    pref_range_dict = data.get("preference_range")
    pref_range = (int(pref_range_dict['min']), int(pref_range_dict['max']))
    preassigned_students = data.get("preassigned_students")
    output_path = data.get("output_folder_path")
    
    run_script(csv_file_path, output_path, int(capacity), pref_range, exceptions)


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root, callback=on_data_extracted)
    root.mainloop()

# TODO Priorities:
# 1. match the variables from the popup to the matching algorithm
# 3. button to run the matching algorithm in scripts/script.py
# 4. figure out where to save the csv file -> we will have 2 different ones, one for canvas group matching and one for profs
# 5. (?) Optional for now: create another button to validate csv file before matching