"""
This file defines the input fields used in the application. 
Each field is represented as a dictionary with the following keys:
- label: The display name of the field shown to the user
- key: The internal key used to reference the field in code.
- type: The data type of the field. It determines the kind of input widget created dynamically.
- default: Default value for field if it exists.
- tooltip: A short description shown to the user
"""

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
        "tooltip": "Minimum and maximum preference range of students to be assigned to. The smallest value of max can be set to the highest minimum rank of a project."
    },
    {
        "label": "Preassigned Students:",
        "key": "student_group_inclusions",
        "type": "list",
        "item": {
            "student": {"type": "string", "label": "Student ID"},
            "projects": {"type": "string", "label": "Preassigned Groups"}
        },
        "tooltip": "Specify projects that the student must be assigned to by Student ID (e.g. 12345678: ProjectA, ProjectB)"
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