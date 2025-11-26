Please read this file before using the program.

=========================
INSTALLATION INSTRUCTIONS
=========================

*** MACOS USERS ONLY *** 

You may see a warning message:
"ProjectMatching-macos can't be opened because it is from an unidentified developer."
Do not worry - this is macOS Gatekeeper protecting you from apps that are not notarized with Apple. You can still open the app safely by:
1. Right click the ProjectMatching-macos app icon
2. Choose Open from the menu

*Note*
This specific file is safe because it was distributed directly by our team. However, please be cautious
when using this method for other apps or files downloaded from the internet. Unknown or unverified software could harm your computer.

*** WINDOWS USERS ONLY *** 
You may see a warning message:
1. Click on Extract all
2. Click on More info
3. Click on Run Anyway


============================= 
CSV FILE FORMAT REQUIREMENTS
=============================

- The file must be saved as .csv (comma-separated values).
- The first row of the CSV file should contain column headers. All subsequent rows should be data values.
- No empty rows.
- The required columns must be in the specific order given by the dropdown list.
- Note: Dropdown headers need not match the CSV text exactly; however, ensure that they correspond to the correct columns.
    Examples:
    - "Student ID" in the dropdown can match CSV headers like "student_id", "Student ID", or "Student Number".
    - "Student Name" can match "student_name", "Name", or "Full Name".
    - "Projects ..." indicates project-related columns.

If your CSV file does not match these requirements, the program may not work correctly.


==============================
CONFIGURE MATCHING PARAMETERS
==============================

- Maximum Students per Project: This setting controls the maximum number of students that can be assigned to a project.
- Exceptions for Maximum Students per Project: This setting allows you to customize the capacity for specific projects.
    - First textbox: Enter the Project name exactly as it appears in your CSV file.
    - Second textbox: Enter the maximum number of students allowed for that project.
- Preference Range: This setting controls the minimum and maximum preference rank that the program will consider when assigning students to projects.
- Preassigned Projects: This setting allows you to specify projects that a student can only be assigned to.
    - First textbox: Enter the Student ID.
    - Second textbox: Enter the project names exactly as they appear in your CSV file, separated by commas.
- Prohibited Projects: This setting allows you to specify projects that a student must not be assigned to.
    - First textbox: Enter the Student ID.
    - Second textbox: Enter the project names exactly as they appear in your CSV file, separated by commas.


=================
ADDITIONAL NOTES
=================

1. The algorithm does not produce any unassigned students unless there are more students than projects.
2. If the maximum of preference range is too small, there will be an error: cost matrix is infeasible.
    - To avoid this: Set the maximum of preference range to be the maximum of the smallest rank across all projects.


=================
FILES GENERATED
=================

This section is to explain the three files generated and the purpose of each of the file.

1. 'student-project-allocations.csv'
    - This file contains the final allocations of students to their assigned projects. 
    - It shows which project each student has been matched with as well as their rankings for other projects
    - If a value is empty, it means that the corresponding field was already empty in the dataset provided by the user.

2. 'student_project_swaps.csv'
    - This file records any swaps that can be made between students while maintaining the same overall average ranking of the allocation.
    In other words, it identifies pairs of students who could exchange their assigned projects without decreasing the overall optimality of the matching.

3. 'canvas-group-allocations.csv'
    - This file is formatted specifically for uploading into Canvas to automatically create groups and assign students to them based on their project allocations.