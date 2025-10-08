import tkinter as tk
from project_matching_gui import ProjectMatchingGUI 
from scripts.script import run_script
from tkinter import messagebox

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
    capacity_exceptions = {k: int(v) for k, v in exceptions.items()}

    pref_range_dict = data.get("preference_range")
    pref_range = (int(pref_range_dict['min']), int(pref_range_dict['max']))

    preassigned_students = data.get("preassigned_students", {})

    output_path = data.get("output_folder_path")
    try: 
        run_script(csv_file_path, output_path, int(capacity), pref_range, capacity_exceptions, preassigned_students)
        messagebox.showinfo("Success", f"Matching completed successfully!\nOutput saved to: {output_path}")
    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root, callback=on_data_extracted)
    root.mainloop()

# TODO Priorities:
# 1. match the variables from the popup to the matching algorithm
# 3. button to run the matching algorithm in scripts/script.py
# 4. figure out where to save the csv file -> we will have 2 different ones, one for canvas group matching and one for profs
# 5. (?) Optional for now: create another button to validate csv file before matching