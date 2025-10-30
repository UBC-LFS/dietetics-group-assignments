import tkinter as tk
from project_matching_gui import ProjectMatchingGUI 
from scripts.script import run_script
from tkinter import messagebox

def on_data_extracted(data, root):
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

    output_folder_name = data.get("output_folder_name")

    student_group_inclusions = data.get("student_group_inclusions", {})
    cleaned_student_group_inclusions = {}
    for key, val in student_group_inclusions.items():
        projects = [p.strip() for p in val.split(',')]
        cleaned_student_group_inclusions[key] = projects

    student_group_exclusions = data.get("student_group_exclusions", {})
    cleaned_student_group_exclusions = {}
    for key, val in student_group_exclusions.items():
        projects = [p.strip() for p in val.split(',')]
        cleaned_student_group_exclusions[key] = projects

    try: 
        run_script(csv_file_path, output_path, int(capacity), pref_range, capacity_exceptions, preassigned_students, cleaned_student_group_inclusions, cleaned_student_group_exclusions, output_folder_name) 
        messagebox.showinfo("Success", f"Matching completed successfully! Folder {output_folder_name} saved to: {output_path}")
    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectMatchingGUI(root, callback=lambda data: on_data_extracted(data, root))
    root.mainloop()
