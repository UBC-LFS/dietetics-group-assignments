import os
from exceptions import FieldError
from styles import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget,
    QFileDialog, QComboBox, QPushButton, QLineEdit, QLabel 
)

# TODO: Remove and move to a separate file
HEADER_OPTIONS = {
    1: { 
        "header_values": '| Student Name | Student Number | Projects ... ', 
        "indices": {
            "student_number": 1,
            "student_name": 0,
            "project_column_index": 2
        }},
    2: { 
        "header_values": '| Student First Name | Student Last Name | Student Number | Projects ... ', 
        "indices": {
            "student_number": 2,
            "student_first_name": 0,
            "student_last_name": 1,
            "project_column_index": 3
        }},
    3: { 
        "header_values": '| Student First Name | Student Last Name | Student Email | Student Number | Projects ... ', 
        "indices": {
            "student_first_name": 0,
            "student_last_name": 1,
            "student_email": 2,
            "student_number": 3,
            "project_column_index": 4
        }}
}


class UploadCSVPage(QWidget):
    def __init__(self):
        super().__init__()

        self.header_options = HEADER_OPTIONS

        # widgets with state
        self.file_entry = None

        # needs to be accessed by the ProjectMatchingGUI object 
        self.csv_file_path = ""
        self.csv_file_name = "" 
        self.selected_header = None

        self.configure_button = None

        self._setup_gui()

    
    def extract_parameters(self):
        if self.csv_file_path == "" or self.csv_file_name == "":
            raise FieldError("No File Selected", "Please upload a csv file")

        if self.selected_header is None:
            raise FieldError("Select Header", "Please configure the parameters for the matching algorithm")

        index_info = self.header_options[self.selected_header]["indices"] 
        return self.csv_file_path, self.csv_file_name, index_info

    def _setup_gui(self):

        # Handle UI elements
        layout = QVBoxLayout()  
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)

        title_label = QLabel("Welcome to Student-Project Matching System!")
        title_label.setFont(QFont(MAIN_FONT, HEADER_FONT_SIZE, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Before you start, please read the README.txt file in the directory.")
        subtitle_label.setFont(QFont(MAIN_FONT, SUBHEADER_FONT_SIZE, QFont.Bold))
        subtitle_label.setWordWrap(True)
        subtitle_label.setContentsMargins(10, 10, 10, 10)
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)

        upload_button = QPushButton("Upload CSV File")
        upload_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 6px 12px;
            border-width: 2px; 
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        """)
        upload_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        layout.addWidget(upload_button, alignment=Qt.AlignLeft)

        file_display_layout = QHBoxLayout()
        file_label = QLabel("Selected File:")
        file_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.file_entry = QLineEdit()
        self.file_entry.setReadOnly(True)
        self.file_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.file_entry.setFixedWidth(400)
        layout.addLayout(file_display_layout)
        file_display_layout.addWidget(file_label)
        file_display_layout.addWidget(self.file_entry, alignment=Qt.AlignLeft, stretch=1)

        header_dropdown = QComboBox()
        header_dropdown.addItem("Select the header which corresponds to the CSV file uploaded.")
        index = header_dropdown.count() - 1
        header_dropdown.model().item(index).setEnabled(False)

        for key in self.header_options.keys():
            header_dropdown.addItem(self.header_options[key]["header_values"], key)

        layout.addWidget(header_dropdown, alignment=Qt.AlignLeft)

        side_note = QLabel("Note: The header values in the dropdown have to correspond to the correct columns.")
        side_note.setFont(QFont(MAIN_FONT, 12))
        side_note.setWordWrap(True)
        layout.addWidget(side_note)

        self.configure_button = QPushButton("Configure Groups")
        self.configure_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 6px 12px;
            border-width: 2px;
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        """)
        self.configure_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        layout.addWidget(self.configure_button, alignment=Qt.AlignLeft)

        layout.addStretch()

        # Setup signals
        upload_button.clicked.connect(self._upload_csv_file)
        header_dropdown.currentIndexChanged.connect(self._update_selected_header)
    

    @Slot()
    def _upload_csv_file(self):
        """Opens a file dialog to select CSV file"""
        start_dir = os.getcwd()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            start_dir,
            "CSV files (*.csv)"
        )

        if file_path:
            self.csv_file_path = file_path
            self.csv_file_name = os.path.basename(file_path)
            self.file_entry.setText(self.csv_file_name)
    

    @Slot(int)
    def _update_selected_header(self, dropdown_index):
        self.selected_header = dropdown_index
