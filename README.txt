Please read this file before using the program.

=========================
INSTALLATION INSTRUCTIONS
=========================
*** LINUX USERS ONLY ***

You must extract the zip file before running.
Steps:
1. Right-click the zip file
2. Select "Extract here"
3. Click on the extracted folder
4. Click on ProjectMatching-linux

Windows / macOS users: EXtract and double click the executable as normal.

=============================
CSV FILE FORMAT REQUIREMENTS
=============================

- The file must be saved as .csv (comma-separated values).
- The first row should contain column headers.
- No empty rows.
- The required columns must be in this specific order: StudentID, FirstName, LastName, Project(s) Ranking.

| Student Id | First Name | Last Name | Project A | Project B | Project C |
|------------|------------|-----------|-----------|-----------|-----------|
| 1234567    | John       | Smith     |     1     |     2     |     3     |
| 1234568    | Jane       | Doe       |     2     |     1     |     3     |
| 1234569    | Bob        | Johnson   |     3     |     2     |     1     |

If your CSV file does not match these requirements, the program may not work correctly.

==============================
CONFIGURE MATCHING PARAMETERS
==============================

- Maximum Students per Project: This setting controls the maximum number of students that can be assigned to a project.
- Exceptions for Maximum Students per Project: This setting allows you to customize the capacity for specific projects.
    - First textbox: Enter the Project name exactly as it appears in your CSV file.
    - Second textbox: Enter the maximum number of students allowed for that project.
- Preference Range: This setting controls the minimum and maximum preference rank that the program will consider when assigning students to projects.
- Preassigned Students: This setting allows you to preassign students to specific projects.
    - First textbox: Enter the Student ID.
    - Second textbox:  Enter the Project name exactly as it appears in your CSV file.


=================
ADDITIONAL NOTES
=================

1. The algorithm does not produce any unassigned students unless there are more students than projects.
2. If the maximum of preference range is too small, there will be an error: cost matrix is infeasible.
    - To avoid this: Set the maximum of preference range to be the maximum of the smallest rank across all projects.




