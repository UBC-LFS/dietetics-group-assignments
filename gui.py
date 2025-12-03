import PySide6.QtWidgets as widget # pylint: disable=no-name-in-module
from PySide6.QtCore import Qt # pylint: disable=no-name-in-module
from PySide6.QtGui import QFont # pylint: disable=no-name-in-module
from pathlib import Path
from config.header import HEADER_OPTIONS
from config.input_fields import INPUT_FIELDS
import os

MAIN_FONT = "PT Serif"
HEADER_FONT_SIZE = 20
SUBHEADER_FONT_SIZE = 18
REGULAR_FONT_SIZE = 16
SMALLER_FONT_SIZE = 12
BUTTON_BACKGROUND_COLOR = '#f0f0f0'
BUTTON_TEXT_COLOR = 'black'
BUTTON_BORDER_COLOR = '#a9a9a9'

class ProjectMatchingGUI(widget.QMainWindow):
    def __init__(self, root, callback = None):
        super().__init__()
        self.callback = callback
        
        self.setWindowTitle("Student-Project Matching System")
        self.setGeometry(100, 100, 900, 700)

        self.csv_data = None
        self.selected_header = None
        self.csv_file_path = ""
        self.output_folder_path = ""
        self.folder_name = ""
        self.file_entry = ""
        self.user_inputs = {}
        self.create_widgets()

    def create_widgets(self):
        central_widget = widget.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = widget.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)
        
        title_label = widget.QLabel("Welcome to Student-Project Matching System!")
        title_label.setFont(QFont(MAIN_FONT, HEADER_FONT_SIZE, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        subtitle_label = widget.QLabel("Before you start, please read the README.txt file in the directory.")
        subtitle_label.setFont(QFont(MAIN_FONT, SUBHEADER_FONT_SIZE, QFont.Bold))
        subtitle_label.setWordWrap(True)
        subtitle_label.setContentsMargins(10, 10, 10, 10)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        self.create_upload_section(main_layout)
        self.validate_configure_button(main_layout)

        main_layout.addStretch()

    def create_upload_section(self, parent_layout):
        upload_button = widget.QPushButton("Upload CSV File")
        upload_button.clicked.connect(self.upload_csv_file)
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
        parent_layout.addWidget(upload_button, alignment=Qt.AlignLeft)

        # File display row
        file_display_layout = widget.QHBoxLayout()

        file_label = widget.QLabel("Selected File:")
        file_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        file_display_layout.addWidget(file_label)
        
        self.file_entry = widget.QLineEdit()
        self.file_entry.setReadOnly(True)
        self.file_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.file_entry.setFixedWidth(400)
        file_display_layout.addWidget(self.file_entry, alignment=Qt.AlignLeft, stretch=1)

        def update_selected_header(dropdown):
            self.selected_header = dropdown.currentData()
       
        # Dropdown for header
        header_dropdown = widget.QComboBox()
        header_dropdown.addItem("Select the header which corresponds to the CSV file uploaded.")
        index = header_dropdown.count() - 1
        header_dropdown.model().item(index).setEnabled(False)

        for key in HEADER_OPTIONS.keys():
            header_dropdown.addItem(HEADER_OPTIONS[key]["header_values"], key)
        
        header_dropdown.currentIndexChanged.connect(lambda: update_selected_header(header_dropdown))

        side_note = widget.QLabel(
            "Note: The header values in the dropdown have to correspond to the correct columns."
        )
        side_note.setFont(QFont(MAIN_FONT, 12))
        side_note.setWordWrap(True)

        parent_layout.addLayout(file_display_layout)
        parent_layout.addWidget(header_dropdown, alignment = Qt.AlignLeft)
        parent_layout.addWidget(side_note)
   
    def upload_csv_file(self):
        """Opens a file dialog to select CSV file"""
        start_dir = os.getcwd()

        file_path, _ = widget.QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            start_dir,
            "CSV files (*.csv)"
        )
        if file_path:
            self.csv_file_path = file_path
            self.csv_file_name = os.path.basename(file_path)
            self.file_entry.setText(self.csv_file_name)

    def select_folder_path(self):
        start_dir = os.getcwd()

        folder = widget.QFileDialog.getExistingDirectory(
            self,  
            "Select folder to save CSV files",  
            start_dir,  
            widget.QFileDialog.Option.ShowDirsOnly  
        )
        if folder:
            self.output_folder_path.setText(folder)

    def open_input_popup(self):
        if not self.csv_file_path:
            widget.QMessageBox.warning(
                self, "No File Selected", "Please upload a CSV file."
            )
            return
        
        if self.selected_header is None:
            widget.QMessageBox.warning(
                self, "Select Header", "Please select the header which corresponds to your CSV file"
            )
            return
        
        popup = widget.QDialog(self)  
        popup.setWindowTitle("Configure Matching Parameters")
        popup.resize(900, 850)     
        popup.setModal(True)       

        main_layout = widget.QVBoxLayout(popup)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = widget.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scrollable_widget = widget.QWidget()
        scrollable_layout = widget.QVBoxLayout(scrollable_widget)
        scrollable_layout.setContentsMargins(20, 20, 20, 20)

        popup_title = widget.QLabel("Matching Parameters")
        popup_title.setFont(QFont(MAIN_FONT, HEADER_FONT_SIZE, QFont.Bold))
        popup_title.setAlignment(Qt.AlignCenter)

        popup_subtitle = widget.QLabel("Please configure the parameters for the matching algorithm")
        popup_subtitle.setFont(QFont(MAIN_FONT, SUBHEADER_FONT_SIZE, QFont.Bold))
        popup_subtitle.setWordWrap(True)
        popup_subtitle.setAlignment(Qt.AlignCenter)

        scrollable_layout.addWidget(popup_title)
        scrollable_layout.addWidget(popup_subtitle)
        scrollable_layout.addSpacing(20)

        inputs_grid = widget.QGridLayout()
        inputs_grid.setColumnStretch(1, 1)

        row = 0
        for field in INPUT_FIELDS:
            label = widget.QLabel(field["label"])
            label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
            inputs_grid.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignTop)

            if field["type"] == "bool":
                checkbox = widget.QCheckBox()
                checkbox.setChecked(field["default"])
                inputs_grid.addWidget(checkbox, row, 1, Qt.AlignLeft)

                current_key = field["key"]
                self.user_inputs[current_key] = checkbox
                
            elif field["type"] == "list":
                list_widget = widget.QWidget()
                list_layout = widget.QVBoxLayout(list_widget)
                list_layout.setContentsMargins(0, 0, 0, 0)
                
                current_key = field["key"]
                current_layout = list_layout
                self.user_inputs[current_key] = []
                
                def add_row(val1="", val2="", layout=list_layout, key=current_key):
                    row_widget = widget.QWidget()
                    row_layout = widget.QHBoxLayout(row_widget)
                    row_layout.setContentsMargins(0, 2, 0, 2)
                    
                    first_entry = widget.QLineEdit(val1)
                    first_entry.setMaximumWidth(200)
                    row_layout.addWidget(first_entry)
                    
                    colon_label = widget.QLabel(":")
                    colon_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                    row_layout.addWidget(colon_label)
                    
                    second_entry = widget.QLineEdit(val2)
                    second_entry.setMaximumWidth(200)
                    row_layout.addWidget(second_entry)
                    
                    row_layout.addStretch()
                    layout.insertWidget(layout.count() - 1, row_widget)
                    self.user_inputs[key].append((first_entry, second_entry))
                
                def remove_row(key):
                    if self.user_inputs[key]:
                        first_entry, second_entry = self.user_inputs[key].pop()
                        row_widget = first_entry.parent()
                        row_widget.deleteLater()

                # Button frame
                button_widget = widget.QWidget()
                button_layout = widget.QHBoxLayout(button_widget)
                button_layout.setContentsMargins(0, 2, 0, 2)
                
                add_button = widget.QPushButton("+")
                add_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {BUTTON_BACKGROUND_COLOR};
                        color: {BUTTON_TEXT_COLOR};
                        padding: 4px 12px;
                        border-width: 2px;
                        border-color: {BUTTON_BORDER_COLOR};
                        border-style: solid;
                        border-radius: 4px;
                    }}
                """)
                add_button.clicked.connect(lambda checked=False, k=current_key, lf=current_layout: add_row("", "", lf, key=k))
                button_layout.addWidget(add_button)
                
                remove_button = widget.QPushButton("-")
                remove_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {BUTTON_BACKGROUND_COLOR};
                        color: {BUTTON_TEXT_COLOR};
                        padding: 4px 12px;
                        border-width: 2px;
                        border-color: {BUTTON_BORDER_COLOR};
                        border-style: solid;
                        border-radius: 4px;
                    }}
                """)
                remove_button.clicked.connect(lambda checked=False, k=current_key, lf=current_layout: remove_row(key=k))
                button_layout.addWidget(remove_button)
                
                button_layout.addStretch()
                
                list_layout.addWidget(button_widget)
                
                inputs_grid.addWidget(list_widget, row + 1, 0, 1, 2)
                
            elif field["type"] == "range":
                range_widget = widget.QWidget()
                range_layout = widget.QHBoxLayout(range_widget)
                range_layout.setContentsMargins(0, 0, 0, 0)
                
                min_label = widget.QLabel("Min:")
                min_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                range_layout.addWidget(min_label)
                
                min_entry = widget.QLineEdit(str(field["item"]["min"]["default"]))
                min_entry.setMaximumWidth(80)
                min_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                range_layout.addWidget(min_entry)
                
                range_layout.addSpacing(15)
                
                max_label = widget.QLabel("Max:")
                max_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                range_layout.addWidget(max_label)
                
                max_entry = widget.QLineEdit(str(field["item"]["max"]["default"]))
                max_entry.setMaximumWidth(80)
                max_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                range_layout.addWidget(max_entry)
                
                range_layout.addStretch()
                
                self.user_inputs[field["key"]] = {"min": min_entry, "max": max_entry}
                
                inputs_grid.addWidget(range_widget, row + 1, 0, 1, 2)
                
            else:
                entry = widget.QLineEdit(field["default"])
                entry.setMaximumWidth(80)
                entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
                inputs_grid.addWidget(entry, row, 1, Qt.AlignLeft)
                self.user_inputs[field["key"]] = entry
            
            row += 1
            
            # Tooltip
            tooltip_label = widget.QLabel(field["tooltip"])
            tooltip_label.setFont(QFont("Arial", 13))
            tooltip_label.setStyleSheet("color: gray; font-style: italic;")
            tooltip_label.setWordWrap(True)
            inputs_grid.addWidget(tooltip_label, row + 1, 0, 1, 2)
            
            row += 2
        
        # Folder display row
        folder_path_display_layout = widget.QHBoxLayout()

        folder_path_label = widget.QLabel("Selected Directory:")
        folder_path_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        self.output_folder_path = widget.QLineEdit()
        self.output_folder_path.setReadOnly(True)
        self.output_folder_path.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.output_folder_path.setFixedWidth(520)

        folder_path_btn = widget.QPushButton("Browse")
        folder_path_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 4px 12px;
            border-width: 1px;
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        """)
        folder_path_btn.setFont(QFont(MAIN_FONT, SMALLER_FONT_SIZE))
        folder_path_btn.clicked.connect(self.select_folder_path)

        folder_path_display_layout.addWidget(folder_path_label)
        folder_path_display_layout.addWidget(self.output_folder_path, alignment=Qt.AlignLeft, stretch = 1)
        folder_path_display_layout.addWidget(folder_path_btn, alignment=Qt.AlignLeft, stretch = 1)

        folder_name_display_layout = widget.QHBoxLayout()
        folder_name_label = widget.QLabel("Save as (folder name):")
        folder_name_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        folder_name_display_layout.addWidget(folder_name_label)

        self.folder_name = widget.QLineEdit()
        self.folder_name.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.folder_name.setFixedWidth(500)
        folder_name_display_layout.addWidget(self.folder_name, alignment=Qt.AlignLeft, stretch=1)

        button_final_widget = widget.QWidget()
        button_layout = widget.QHBoxLayout(button_final_widget)
        button_layout.setContentsMargins(0, 10, 0, 2)

        cancel_button = widget.QPushButton("Cancel")
        cancel_button.clicked.connect(popup.close)
        cancel_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 8px 15px;
            border-width: 2px;
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        """)
        cancel_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        generate_button = widget.QPushButton("Generate Groups")
        generate_button.clicked.connect(lambda: self.validate_inputs_and_run(popup))
        generate_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 8px 15px;
            border-width: 2px;
            border-color: {BUTTON_BORDER_COLOR};
            border-style: solid;
            border-radius: 4px;
        }}
        """)
        generate_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(generate_button)

        scrollable_layout.addLayout(inputs_grid)
        scrollable_layout.addLayout(folder_path_display_layout)
        scrollable_layout.addLayout(folder_name_display_layout)
        scrollable_layout.addWidget(button_final_widget, alignment=Qt.AlignLeft)
        scrollable_layout.addStretch()

        scroll_area.setWidget(scrollable_widget)

        main_layout.addWidget(scroll_area)

        popup.exec()


    def collect_inputs_and_run(self, popup=None):
        if not self.output_folder_path.text():
            raise ValueError("No Directory Selected. Please select a directory.")
        
        if not self.folder_name.text():
            raise ValueError("No Folder Name entered. Please enter a folder name.")
        
        collected_user_inputs = {}
        for key, val in self.user_inputs.items():
            if isinstance(val, list) and key == 'capacity_exceptions':
                if val:
                    results = {}
                    for a, b in val:
                        v1, v2 = a.text().strip(), b.text().strip()
                        if v1 and v2:
                            try:
                                capacity = int(v2)
                            except ValueError as exc:
                                raise ValueError(f"Invalid maximum capacity '{v2}'. Expected an integer.") from exc
                            
                            results[v1] = capacity

                    collected_user_inputs[key] = results
            elif isinstance(val, list) and key != 'capacity_exceptions': # student_group_inclusions || student_group_exclusions
                if val:
                    results = {}
                    for a, b in val:
                        v1, v2 = a.text().strip(), b.text().strip()
                        if v1 and v2:
                            results[v1] = v2

                    collected_user_inputs[key] = results
                    
            elif isinstance(val, dict):
                min_val = val["min"].text().strip()
                max_val = val["max"].text().strip()
                
                if not min_val:
                    raise ValueError("Minimum value for preference range cannot be empty.")

                try:
                    min_val_int = int(min_val)
                except ValueError as exc:
                    raise ValueError(f"Invalid minimum value of {min_val} for preference range. Expected to be an integer.") from exc
            
                if not max_val:
                    raise ValueError("Maximum value for preference range cannot be empty.")
                try:
                    max_val_int = int(max_val)
                except ValueError as exc:
                    raise ValueError(f"Invalid maximum value of {max_val} for preference range. Expected to be an integer.") from exc

                collected_user_inputs[key] = {
                    "min": min_val_int,
                    "max": max_val_int
                }
            else: 
                collected_user_inputs[key] = val.text()

        collected_user_inputs["csv_file_path"] = self.csv_file_path
        collected_user_inputs['csv_file_name'] = self.csv_file_name
        collected_user_inputs['output_folder_path'] = self.output_folder_path.text()
        collected_user_inputs['output_folder_name'] = self.folder_name.text()

        collected_user_inputs["header_option"] = self.selected_header

        if self.callback:
            self.callback(collected_user_inputs)

    def validate_inputs_and_run(self, popup):
        try:
            self.collect_inputs_and_run(popup)
        except ValueError as err:
            widget.QMessageBox.warning(
                self, "Invalid", str(err)
            )
        

    def validate_configure_button(self, parent_layout):
    
        configure_button = widget.QPushButton("Configure Groups")
        configure_button.clicked.connect(self.open_input_popup)
        configure_button.setStyleSheet(f"""
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
        configure_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        parent_layout.addWidget(configure_button, alignment=Qt.AlignLeft)

