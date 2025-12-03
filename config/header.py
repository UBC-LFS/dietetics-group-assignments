"""
This file defines the expected structure of the input CSV uploaded in the application.

Each configuration entry provides:
- header_values: A string representation of the expected CSV column names for users to choose
- indices: A mapping of identifiers to their corresponding column indices in the CSV. These indices 
            allow the application to correctly extract the student's information and their ranking of projects.

Column index details:
- project_column_index: The starting column index for all project preference 
  rankings. Each subsequent column represents a project and contains the 
  student’s numeric preference for that project.

- student_name: The column index where each student's FULL name (First + Last) is stored
OR
- student_first_name and student_last_name: Two separate columns for first and last name.
"""

HEADER_OPTIONS = {
    1: { 
        "header_values": '| Student Name | Student Number | Projects .. ', 
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