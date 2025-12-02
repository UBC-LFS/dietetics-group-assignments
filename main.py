from PySide6 import QtWidgets
from gui import ProjectMatchingGUI
from scripts.script import run_script
import sys

def on_data_extracted(data, window):
    """
    Callback function that receives data from the project_matching_gui.py
    and passes it to script.py for processing
    
    Args:
        data: The extracted data from the GUI
    """
    csv_file_path = data.get('csv_file_path')

    header_option = data.get('header_option')

    capacity = data.get("capacity")
    exceptions = data.get("capacity_exceptions")
    capacity_exceptions = {k: int(v) for k, v in exceptions.items()} if exceptions else {}

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
        run_script(csv_file_path, output_path, int(capacity), pref_range, capacity_exceptions, preassigned_students, cleaned_student_group_inclusions, cleaned_student_group_exclusions, output_folder_name, header_option)
        msg =  QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(
            f"Matching completed successfully!\n\nOutput folder '{output_folder_name}' "
            f"is saved to:\n{output_path}"
        )
        msg.exec() 
        window.close()
    except Exception as e:
        QtWidgets.QMessageBox.warning(
            window, "Error", f"An error occurred: {str(e)}"
        )    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    try:
        import pyi_splash
        if pyi_splash.is_alive():
            pyi_splash.close()
    except ImportError:
        pass

    window = ProjectMatchingGUI(app, callback=lambda data: on_data_extracted(data, window))
    window.show()

    sys.exit(app.exec())
