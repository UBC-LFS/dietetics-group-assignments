import PySide6.QtWidgets as widget # pylint: disable=no-name-in-module
from PySide6.QtCore import Qt, QCoreApplication # pylint: disable=no-name-in-module
from PySide6.QtGui import QFont, QGuiApplication # pylint: disable=no-name-in-module
import sys
import os

MAIN_FONT = "PT Serif"
HEADER_FONT_SIZE = 18
SUBHEADER_FONT_SIZE = 15
REGULAR_FONT_SIZE = 12
BUTTON_BACKGROUND_COLOR = '#f0f0f0'
BUTTON_TEXT_COLOR = 'black'

class ProjectMatchingGUI(widget.QMainWindow):
    def __init__(self, callback = None):
        super().__init__()
        self.callback = callback
        
        # setup Window
        self.setWindowTitle("Student-Project Matching System")
        self.setGeometry(100, 100, 900, 700)

        # setup variables
        self.csv_file_path = ""
        self.csv_file_name = ""
        self.csv_data = None
        self.output_folder_path = ""
        self.user_inputs = {}
        self.folder_name = ""
        self.create_widgets()

    def create_widgets(self):
        central_widget = widget.QWidget()
        self.setCentralWidget(central_widget)

        main_layout = widget.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        central_widget.setLayout(main_layout)
        
        # Title label
        title_label = widget.QLabel("Welcome to Student-Project Matching System!")
        title_label.setFont(QFont(MAIN_FONT, HEADER_FONT_SIZE, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle label
        subtitle_label = widget.QLabel("Before you start, please read the README.txt file in the directory.")
        subtitle_label.setFont(QFont(MAIN_FONT, SUBHEADER_FONT_SIZE, QFont.Bold))
        subtitle_label.setWordWrap(True)
        subtitle_label.setContentsMargins(10, 10, 10, 10)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        self.create_upload_section(main_layout)
        self.configure_group(main_layout)

        main_layout.addStretch()

    def create_upload_section(self, parent_layout):
        upload_button = widget.QPushButton("Upload CSV File")
        upload_button.clicked.connect(self.upload_csv_file)
        upload_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
        }}
        """)
        upload_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        parent_layout.addWidget(upload_button, alignment=Qt.AlignLeft)

        # File display row
        file_display_layout = widget.QHBoxLayout()

        file_label = widget.QLabel("Selected file:")
        file_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        file_display_layout.addWidget(file_label)
        
        self.file_entry = widget.QLineEdit()
        self.file_entry.setReadOnly(True)
        self.file_entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.file_entry.setFixedWidth(400)
        file_display_layout.addWidget(self.file_entry, alignment=Qt.AlignLeft, stretch=1)
        
        parent_layout.addLayout(file_display_layout)

    
    def upload_csv_file(self):
        """Opens a file dialog to select CSV file"""
        file_path, _ = widget.QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV files (*.csv)"
        )
        if file_path:
            self.csv_file_path = file_path
            self.csv_file_name = os.path.basename(file_path)
            self.file_entry.setText(self.csv_file_name)

    def open_input_popup(self):
        if not self.csv_file_path:
            widget.QMessageBox.warning(
                self, "No File Selected", "Please upload a CSV file first."
            )
            return
        
        popup = widget.QDialog(self)  
        popup.setWindowTitle("Configure Matching Parameters")
        popup.resize(800, 750)     
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
        popup_subtitle.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE, QFont.Bold))
        popup_subtitle.setWordWrap(True)
        popup_subtitle.setAlignment(Qt.AlignCenter)

        scrollable_layout.addWidget(popup_title)
        scrollable_layout.addWidget(popup_subtitle)
        scrollable_layout.addSpacing(20)

        input_fields = [
            {
                "label": "Maximum Students per Project:",
                "key": "capacity",
                "type": "int",
                "default": "5",
                "tooltip": "Maximum number of students that can be assigned to one project"
            },
            {
                "label": "Exceptions for Maximum Students per Project:",
                "key": "capacity_exceptions",
                "type": "list",
                "item": {
                    "group": {"type": "string", "label": "Project/Group"},
                    "capacity": {"type": "int", "label": "Max Students"}
                },
                "tooltip": "Customize maximum number of students for specific projects (e.g. ProjectA : 2)"
            },
            {
                "label": "Preference Range:",
                "key": "preference_range",
                "type": "range",
                "item": {
                    "min": {"type": "int", "label": "Minimum Preferences", "default": 1},
                    "max": {"type": "int", "label": "Maximum Preferences", "default": 16}
                },
                "tooltip": "Minimum and maximum preference range of students to be matched to. The smallest value of max can be set to the highest minimum rank found among all projects."
            },
            {
                "label": "Preassigned Students:",
                "key": "student_group_inclusions",
                "type": "list",
                "item": {
                    "student": {"type": "string", "label": "Student ID"},
                    "projects": {"type": "string", "label": "Preassigned Groups"}
                },
                "tooltip": "Specify projects that the student can only be matched to by Student ID (e.g. 12345678: ProjectA, ProjectB)"
            },
            {
                "label": "Prohibited Projects:",
                "key": "student_group_exclusions",
                "type": "list",
                "item": {
                    "student": {"type": "string", "label": "Student ID"},
                    "projects": {"type": "string", "label": "Excluded Projects"}
                },
                "tooltip": "Specify projects that the student must not be assigned to by Student ID (e.g. 12345678: ProjectA, ProjectB)"
            },
        ]

        inputs_grid = widget.QGridLayout()
        inputs_grid.setColumnStretch(1, 1)

        row = 0
        for field in input_fields:
            label = widget.QLabel(field["label"])
            label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
            inputs_grid.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignTop)

            if field["type"] == "bool":
                checkbox = widget.QCheckBox()
                checkbox.setChecked(field["default"])
                inputs_grid.addWidget(checkbox, row, 1, Qt.AlignLeft)
                self.user_inputs[field["key"]] = checkbox
                
            elif field["type"] == "list":
                list_widget = widget.QWidget()
                list_layout = widget.QVBoxLayout(list_widget)
                list_layout.setContentsMargins(0, 0, 0, 0)
                
                self.user_inputs[field["key"]] = []
                
                def add_row(val1="", val2="", layout=list_layout, key=field["key"]):
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
                    
                    layout.addWidget(row_widget)
                    self.user_inputs[key].append((first_entry, second_entry, row_widget))
                
                def remove_row(key=field["key"]):
                    if self.user_inputs[key]:
                        print("deleting")
                        first_entry, second_entry, row_widget = self.user_inputs[key].pop()
                        row_widget.deleteLater()
                    print("outside")

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
                        border: none;
                        border-radius: 4px;
                    }}
                """)
                add_button.clicked.connect(lambda checked=False, f=add_row: f("", ""))
                button_layout.addWidget(add_button)
                
                remove_button = widget.QPushButton("-")
                remove_button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {BUTTON_BACKGROUND_COLOR};
                        color: {BUTTON_TEXT_COLOR};
                        padding: 4px 12px;
                        border: none;
                        border-radius: 4px;
                    }}
                """)
                remove_button.clicked.connect(remove_row)
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
            tooltip_label.setFont(QFont("Arial", 11))
            tooltip_label.setStyleSheet("color: gray; font-style: italic;")
            tooltip_label.setWordWrap(True)
            tooltip_label.setMaximumWidth(650)
            inputs_grid.addWidget(tooltip_label, row + 1, 0, 1, 2)
            
            row += 2
        
        scrollable_layout.addLayout(inputs_grid)
        scrollable_layout.addStretch()

        scroll_area.setWidget(scrollable_widget)

        main_layout.addWidget(scroll_area)

        popup.exec()
        

    def configure_group(self, parent_layout):
        configure_button = widget.QPushButton("Configure Groups")

        configure_button.clicked.connect(self.open_input_popup)
        configure_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {BUTTON_BACKGROUND_COLOR};
            color: {BUTTON_TEXT_COLOR};
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
        }}
        """)
        configure_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        parent_layout.addWidget(configure_button, alignment=Qt.AlignCenter)


if __name__ == "__main__":
    app = widget.QApplication(sys.argv)
    window = ProjectMatchingGUI()
    window.show()
    sys.exit(app.exec())