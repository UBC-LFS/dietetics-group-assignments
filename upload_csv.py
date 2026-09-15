import os
from exceptions import FieldError
from config.header import HEADER_OPTIONS
from styles import *
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget,
    QFileDialog, QComboBox, QPushButton, QLineEdit, QLabel 
)
import pandas as pd
from enum import Enum
import re

class responseField(Enum):
    NAME = 'student_name'
    FIRST_NAME = 'student_first_name'
    LAST_NAME = 'student_last_name'
    EMAIL = 'student_email'
    STUDENT_NUMBER = 'student_number'
    PROJECT = 'project_column_index'
    
    
class UploadCSVPage(QWidget):
    def __init__(self):
        super().__init__()

        self.header_options = HEADER_OPTIONS

        # widgets with state
        self.file_entry = None

        # accessed by the ProjectMatchingGUI object 
        self.csv_file_path = ""
        self.csv_file_name = "" 
        self.selected_header = None
        self.configure_button = None

        self._setup_gui()

    
    # output a dictionary of 'student_first_name': idx, etc.
    def extract_parameters(self):
        if self.csv_file_path == "" or self.csv_file_name == "":
            raise FieldError("No File Selected", "Please upload a csv file")
        # for filtereing QX_Y to QX for later grouping
        def get_q_number(col): 
            match = re.match(r"^(Q\d+)(?:_\d+)?$", str(col))
            return match.group(1) if match else None
        # for removing the common question header from qualtrix
        def common_prefix(strings): 
            strings = [str(s) for s in strings]
            if not strings:
                return ""
            if len(strings) == 1:
                return ""
            prefix = strings[0]
            for s in strings[1:]:
                while not s.startswith(prefix):
                    prefix = prefix[:-1]
                    if not prefix:
                        return ""
            return prefix
        df = pd.read_csv(self.csv_file_path)
        filtered = df.loc[:, df.columns.astype(str).str.match(r"^Q\d+(?:_\d+)?$")] # keeping only the actual question
        for q, cols in filtered.T.groupby(filtered.columns.map(get_q_number)):
            prefix = common_prefix(cols[0])
            selected_col_name = cols.T.columns
            filtered.loc[filtered.index[0], selected_col_name] = (
                filtered.loc[filtered.index[0], selected_col_name]
                .astype(str)
                .str.removeprefix(prefix)
            )
        only_q_num = filtered.columns.map(get_q_number)
        most_common = only_q_num.value_counts().idxmax()
        first_index = only_q_num.get_loc(most_common).start

        filtered.columns = filtered.iloc[0]
        filtered = filtered.iloc[2:].reset_index(drop=True)
        col_names = filtered.columns
                
        current_id = 0
        index_info = {}
        student_id_index = None
        for current_id in range(first_index):
            if 'first' in col_names[current_id].lower():
                index_info[responseField.FIRST_NAME] = current_id
            elif 'last' in col_names[current_id].lower():
                index_info[responseField.LAST_NAME] = current_id
            elif 'name' in col_names[current_id].lower():
                index_info[responseField.NAME] = current_id
            elif 'mail' in col_names[current_id].lower():
                index_info[responseField.EMAIL] = current_id
            elif 'student id' in col_names[current_id].lower():
                index_info[responseField.STUDENT_NUMBER] = current_id
                student_id_index = current_id
            elif 'student number' in col_names[current_id].lower():
                index_info[responseField.STUDENT_NUMBER] = current_id
                student_id_index = current_id
        index_info[responseField.PROJECT] = first_index
        if student_id_index is None:
            def is_student_number_column(series, threshold=0.7):
                values = series.dropna().astype(str).str.strip()
                if len(values) == 0:
                    return False
                valid = values.str.fullmatch(r"\d{8,}")
                return valid.mean() >= threshold
                
            for i, col in enumerate(filtered.columns):
                if is_student_number_column(filtered[col]):
                    student_id_index = i
                    break
        if student_id_index is None:
            raise ValueError(f"Unable to find student number column")
        filtered_index_info = {key.value: value for key, value in index_info.items()}
        filtered = filtered.drop_duplicates(subset=filtered.columns[student_id_index], keep='last')
        filtered.to_csv(self.csv_file_path.replace(".","_cleaned."), index=False)
        return self.csv_file_path.replace(".","_cleaned."), self.csv_file_name.replace(".","_cleaned."), filtered_index_info


    def _setup_gui(self):
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

        # header_dropdown = QComboBox()
        # header_dropdown.addItem("Select the header which corresponds to the CSV file uploaded.") # TODO!!
        # index = header_dropdown.count() - 1
        # header_dropdown.model().item(index).setEnabled(False)

        # for key in self.header_options.keys():
        #     header_dropdown.addItem(self.header_options[key]["header_values"], key)

        # layout.addWidget(header_dropdown, alignment=Qt.AlignLeft)

        # side_note = QLabel("Note: The header values in the dropdown have to correspond to the correct columns.")
        # side_note.setFont(QFont(MAIN_FONT, 12))
        # side_note.setWordWrap(True)
        # layout.addWidget(side_note)

        self.configure_button = QPushButton("Configure Groups")
        
        self.configure_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        layout.addWidget(self.configure_button, alignment=Qt.AlignLeft)
        
        
        self.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 6px 12px;
            border-width: 2px;
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {BUTTON_HOVER_COLOR};
        }}
        """)

        for button in self.findChildren(QPushButton):
            button.setCursor(QCursor(Qt.PointingHandCursor))

        layout.addStretch()

        # Setup signals
        upload_button.clicked.connect(self._upload_csv_file)
        # header_dropdown.currentIndexChanged.connect(self._update_selected_header)
    

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
