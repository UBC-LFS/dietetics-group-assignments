"""
This file defines the input fields used in the application. 
Each field is represented as a dictionary with the following keys:
- label: The display name of the field shown to the user.
- key: The internal key used to reference the field in code.
- type: The data type of the field. It determines the kind of input widget created dynamically.
- default: Default value for field if it exists.
- tooltip: A short description shown to the user.
- callback: To be called when a field gets edited.
"""

INPUT_FIELDS = [
    {
        "label": "Maximum Students per Project:",
        "key": "capacity",
        "type": "int",
        "default": "5",
        "callback": "update_max_per_project"
    },
    {
        "label": "Exceptions for Maximum Students per Project:",
        "key": "capacity_exceptions",
        "type": "list",
        "item": {
            "group": {"type": "dropdown", "default": "projects", "label": "Project/Group"},
            "capacity": {"type": "int", "label": "Max Students"}
        },
        "tooltip": "Customize maximum number of students for specific projects (e.g. ProjectA : 2)",
        "callback": "update_max_per_project_exception"
    },
    {
        "label": "Preassigned Students:",
        "key": "student_group_inclusions",
        "type": "list",
        "item": {
            "student": {"type": "string", "label": "Student ID"},
            "projects": {"type": "multiselect", "default": "projects", "label": "Preassigned Groups"}
        },
        "tooltip": "Specify projects that the student must be assigned to by Student ID (e.g. 12345678: ProjectA, ProjectB)",
        "callback": "update_inclusions"
    },
    {
        "label": "Prohibited Projects:",
        "key": "student_group_exclusions",
        "type": "list",
        "item": {
            "student": {"type": "string", "label": "Student ID"},
            "projects": {"type": "multiselect", "default": "projects", "label": "Excluded Projects"}
        },
        "tooltip": "Specify projects that the student must not be assigned to by Student ID (e.g. 12345678: ProjectA, ProjectB)",
        "callback": "update_exclusions"
    },
]