import sys
from exceptions import MissingFieldError
from styles import *
from algorithm import *
from upload_csv import UploadCSVPage
from configure_parameters import ConfigureParametersPage
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, 
    QVBoxLayout, QWidget, 
    QMessageBox, QPushButton, QLabel
)
from pprint import pprint


class ProjectMatchingGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # fields for algorithm
        self.csv_data = None
        self.selected_header = None
        self.csv_file_path = ""
        self.output_folder_path = ""
        self.folder_name = ""
        self.file_entry = ""
        self.user_inputs = {}

        self.students = None
        self.projects = None
        self.preferences = None
        self.rankings = None

        # setup window
        self.setWindowTitle("Student-Project Matching System")
        self.setGeometry(100, 100, 900, 700)
        self.stacked_widget = QStackedWidget()
        self.upload_csv_page = UploadCSVPage()
        self.configure_parameters_page = ConfigureParametersPage()
        self.upload_csv_page.configure_button.clicked.connect(self._setup_configure_parameters_page)
        self.configure_parameters_page.cancel_button.clicked.connect(self._setup_csv_upload_page)
        self.configure_parameters_page.generate_button.clicked.connect(self._start_matching)
        self.stacked_widget.addWidget(self.upload_csv_page)
        self.stacked_widget.addWidget(self.configure_parameters_page)
        self.setCentralWidget(self.stacked_widget)


    def _setup_csv_upload_page(self):
        self.setWindowTitle("Student-Project Matching System")
        self.stacked_widget.setCurrentIndex(0)


    def _setup_configure_parameters_page(self):
        try:
            # Extract data gathered from upload csv page
            csv_file_path, csv_file_name, csv_indices_info = self.upload_csv_page.extract_parameters()

            self.student_fields = {
                header: idx for header, idx in csv_indices_info.items()
                if header != "project_column_index"
            }

            proj_col_index = csv_indices_info["project_column_index"]

            self.students, self.projects, self.preferences = read_data_and_clean2(csv_file_path, self.student_fields, proj_col_index)
            self.configure_parameters_page.init_student_project_information(self.students, self.projects)

            # Update window 
            self.setWindowTitle("Configure Matching Parameters")
            self.stacked_widget.setCurrentIndex(1)
        except MissingFieldError as err:
            QMessageBox.warning(self, err.title, err.text)


    def _start_matching(self):
        print("Collect inputs")
        collected_user_inputs = self.configure_parameters_page.collect_inputs()
        print(collected_user_inputs)
        print("Start hungarian algorithm")

        max_per_projects = collected_user_inputs["max_per_project"]
        pref_range = collected_user_inputs["pref_range"]
        inclusions = collected_user_inputs["inclusions"]
        exclusions = collected_user_inputs["exclusions"]
        output_path = collected_user_inputs["output_folder_path"]
        output_folder_name = collected_user_inputs["folder_name"]

        run_script2(self.students, self.student_fields, self.projects, max_per_projects, self.preferences, pref_range, inclusions, exclusions, output_path, output_folder_name)



def main():
    app = QApplication(sys.argv)
    main_window = ProjectMatchingGUI()
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()