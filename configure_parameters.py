import os
from exceptions import FieldError
from styles import *
from config.input_fields import INPUT_FIELDS 
from widgets.range_field import RangeField
from widgets.list_field import ListField
from widgets.checkable_combo_box import CheckableComboBox
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QFileDialog, QComboBox, QLineEdit, QPushButton, QScrollArea, QCheckBox, QWidget, QLabel 


class ConfigureParametersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.input_fields = INPUT_FIELDS
        self.user_inputs = {}

        # widgets with state
        self.selected_file = None
        self.num_students = None
        self.num_projects = None
        self.num_slots = None
        self.output_folder_path = None

        # Needed by ProjectMatchingGUI object
        self.students = []
        self.projects = []
        self.max_per_project = {}
        self.pref_range = {"min": 1, "max": 9999}
        self.inclusions = {}
        self.exclusions = {}
        self.cancel_button = None
        self.generate_button = None

        self._setup_gui()


    def init_student_project_information(self, students, projects, filename):
        self.students = students
        self.projects = projects 

        # place any code that changes based on reuploaded csv here
        self._init_input_fields()

        self.max_per_project = {}
        for p in self.projects:
            self.max_per_project[p] = round(len(self.students) / len(self.projects))

        self.selected_file.setText(f"File: {filename}")
        self.num_students.setText(f"Total students: {len(self.students)}")
        self.num_projects.setText(f"Total projects: {len(self.projects)}")
        self.num_slots.setText(f"Total Project Spots: {sum(self.max_per_project.values())}")

    # Do input checking here
    def collect_inputs(self):
        if len(self.students) != sum(self.max_per_project.values()):
            raise FieldError("Mismatched Number of Students and Project Spots", "Number of available project spots does not match number of students")

        seen = set()
        for project_field, capacity_field in self.user_inputs["capacity_exceptions"].values():
            project = project_field.currentIndex()
            if project in seen:
                raise FieldError("Duplicate Projects", "Duplicate projects found in capacity exceptions fields.")
            seen.add(project)

        if not self.output_folder_path.text():
            raise FieldError("No Directory", "No output directory Selected. Please select a directory.")
        
        collected_user_inputs = {
            "max_per_project": self.max_per_project,
            "pref_range": self.pref_range,
            "inclusions": self.inclusions,
            "exclusions": self.exclusions,
            "output_folder_path": self.output_folder_path.text(),
        }

        return collected_user_inputs


    def _init_input_fields(self):
        for field in self.input_fields:
            if field["key"] == "capacity":
                widget = self.user_inputs[field["key"]]
                widget.setText(str(round(len(self.students) / len(self.projects))))
            elif field["type"] == "range":
                widget = self.user_inputs[field["key"]]
                widget.reset()
            elif field["type"] == "list":
                widget = self.user_inputs[field["key"]]
                widget.clear()
                items = field["item"]
                for item in items.values():
                    # update dropdowns or multiselects
                    if item["type"] == "dropdown" or item["type"] == "multiselect" and "default" in item:
                        dropdown_options = self._get_dropdown_options(item["default"])
                        item["dropdown_options"] = dropdown_options
                
                widget.row_template = items


    def _setup_gui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        self.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scrollable_widget = QWidget()
        scrollable_layout = QVBoxLayout(scrollable_widget)
        scrollable_layout.setContentsMargins(20, 20, 20, 20)
        scrollable_layout.addSpacing(20)

        title = QLabel("Assignment Settings")
        title.setFont(QFont(MAIN_FONT, HEADER_FONT_SIZE, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        scrollable_layout.addWidget(title)

        self.selected_file = QLabel("File: N/A")
        self.selected_file.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        self.selected_file.setWordWrap(True)
        self.selected_file.setAlignment(Qt.AlignCenter)
        scrollable_layout.addWidget(self.selected_file)

        # Data extracted from the csv
        information_row = QHBoxLayout()
        information_row.setContentsMargins(20, 20, 20, 20)

        self.num_students = QLabel("Total students: n/a")
        self.num_students.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        information_row.addWidget(self.num_students)

        self.num_projects = QLabel("Total projects: n/a")
        self.num_projects.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        information_row.addWidget(self.num_projects)
        
        self.num_slots = QLabel("Total Project Spots: n/a")
        self.num_slots.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        information_row.addWidget(self.num_slots)
        scrollable_layout.addLayout(information_row)

        inputs_grid = QGridLayout()
        inputs_grid.setColumnStretch(1, 1)

        row = 0
        for field in self.input_fields:
            self._create_field_widget(inputs_grid, row, field)
            row += 3

        scrollable_layout.addLayout(inputs_grid)

        folder_path_display_layout = QHBoxLayout()
        folder_path_label = QLabel("Output Directory:")
        folder_path_label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        self.output_folder_path = QLineEdit()
        self.output_folder_path.setReadOnly(True)
        self.output_folder_path.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))

        folder_path_btn = QPushButton("Browse")
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
        folder_path_btn.clicked.connect(self._select_folder_path)

        folder_path_display_layout.addWidget(folder_path_label)
        folder_path_display_layout.addWidget(self.output_folder_path, alignment=Qt.AlignLeft, stretch=1)
        folder_path_display_layout.addWidget(folder_path_btn, alignment=Qt.AlignLeft, stretch=1)
        scrollable_layout.addLayout(folder_path_display_layout)

        button_final_widget = QWidget()
        button_layout = QHBoxLayout(button_final_widget)
        button_layout.setContentsMargins(0, 10, 0, 2)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(f"""
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
        self.cancel_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        button_layout.addWidget(self.cancel_button)

        self.generate_button = QPushButton("Generate Groups")
        self.generate_button.setStyleSheet(f"""
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
        self.generate_button.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        button_layout.addWidget(self.generate_button)

        scrollable_layout.addWidget(button_final_widget, alignment=Qt.AlignLeft)
        scrollable_layout.addStretch()
        scroll_area.setWidget(scrollable_widget)

        layout.addWidget(scroll_area)


    def _create_field_widget(self, inputs_grid, row, field):
        label = QLabel(field["label"])
        label.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
        inputs_grid.addWidget(label, row, 0, Qt.AlignLeft | Qt.AlignTop)

        if "tooltip" in field:
            tooltip_label = QLabel(field["tooltip"])
            tooltip_label.setFont(QFont("Arial", 13))
            tooltip_label.setStyleSheet("color: gray; font-style: italic;")
            tooltip_label.setWordWrap(True)
            inputs_grid.addWidget(tooltip_label, row + 1, 0, 1, 2)
            row += 1

        if field["type"] == "bool":
            checkbox = QCheckBox()
            checkbox.setChecked(field["default"])
            inputs_grid.addWidget(checkbox, row, 1, Qt.AlignLeft)

            current_key = field["key"]
            self.user_inputs[current_key] = checkbox
            
        elif field["type"] == "list":
            row_template = field["item"]
            list_widget = ListField(row_template)

            if "callback" in field:
                callback = self._get_callback_function(field["callback"])
                list_widget.changed.connect(callback)
                # list_widget._signal_change()

            self.user_inputs[field["key"]] = list_widget
            inputs_grid.addWidget(list_widget, row + 1, 0, 1, 2)

        elif field["type"] == "range":
            default_min = field["item"]["min"]["default"]
            default_max = field["item"]["max"]["default"]
            range_widget = RangeField(default_min=default_min, default_max=default_max)

            if "callback" in field:
                callback = self._get_callback_function(field["callback"])
                range_widget.changed.connect(callback)
                # range_widget._signal_change()

            self.user_inputs[field["key"]] = range_widget
            inputs_grid.addWidget(range_widget, row + 1, 0, 1, 2)

        elif field["type"] == "dropdown":
            dropdown_widget = QComboBox()
            inputs_grid.addWidget(dropdown_widget)
            self.user_inputs[field["key"]] = dropdown_widget

        elif field["type"] == "multiselect":
            multiselect_widget = CheckableComboBox()
            inputs_grid.addWidget(multiselect_widget)
            self.user_inputs[field["key"]] = multiselect_widget

        else:
            entry = QLineEdit(field["default"])
            entry.setMaximumWidth(80)
            entry.setFont(QFont(MAIN_FONT, REGULAR_FONT_SIZE))
            inputs_grid.addWidget(entry, row, 1, Qt.AlignLeft)
            self.user_inputs[field["key"]] = entry

            if "callback" in field:
                callback = self._get_callback_function(field["callback"])
                entry.textEdited.connect(callback)
        
        row += 2


    def _get_dropdown_options(self, source):
        match source:
            case "courses":
                return self.course
            case "students":
                return self.students
            case "projects":
                return self.projects


    def _get_callback_function(self, callback_id):
        match callback_id:
            case "update_max_per_project":
                return self._update_max_per_project
            case "update_max_per_project_exception":
                return self._update_max_per_project_exception
            case "update_pref_range":
                return self._update_pref_range
            case "update_inclusions":
                return self._update_inclusions
            case "update_exclusions":
                return self._update_exclusions

    # Callbacks
    @Slot()
    def _select_folder_path(self):
        start_dir = os.getcwd()

        folder = QFileDialog.getExistingDirectory(
            self,  
            "Select folder to save CSV files",  
            start_dir,  
            QFileDialog.Option.ShowDirsOnly  
        )
        if folder:
            self.output_folder_path.setText(folder)
    

    @Slot(str)
    def _update_max_per_project(self, max_students):
        if not max_students.isdigit():
            self.num_slots.setText(f"Total Project Spots: N/A")
        else:
            max_students = int(max_students)

            for proj in self.projects:
                self.max_per_project[proj] = max_students

            list_fields = self.user_inputs["capacity_exceptions"]
            for dropdown, textbox in list_fields.selected_fields:
                project = dropdown.currentText()
                capacity = textbox.text()

                if not capacity.isdigit():
                    self.max_per_project[project] = 0
                else:
                    self.max_per_project[project] = int(capacity)
                
            self.num_slots.setText(f"Total Project Spots: {sum(self.max_per_project.values())}")


    @Slot()
    def _update_max_per_project_exception(self):
        max_students = int(self.user_inputs["capacity"].text())
        list_fields = self.user_inputs["capacity_exceptions"]

        for proj in self.projects:
            self.max_per_project[proj] = max_students

        for dropdown, textbox in list_fields.selected_fields:
            project = dropdown.currentText()
            capacity = textbox.text()

            if not capacity.isdigit():
                self.max_per_project[project] = 0
            else:
                self.max_per_project[project] = int(capacity)
            
        self.num_slots.setText(f"Total Project Spots: {sum(self.max_per_project.values())}")


    @Slot()
    def _update_pref_range(self, pref_range):
        self.pref_range = pref_range


    @Slot()
    def _update_inclusions(self, inclusions):
        self.inclusions = {}
        for student_number, projects in inclusions:
            self.inclusions[student_number.text().strip()] = projects.currentData()
        

    @Slot()
    def _update_exclusions(self, exclusions):
        self.exclusions = {}
        for student_number, projects in exclusions:
            self.exclusions[student_number.text().strip()] = projects.currentData()
