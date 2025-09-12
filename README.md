# dietetics-group-assignments

## Background
This project uses the Hungarian Algorithm to solve assignment problem of students to projects.

We start by creating a cost matrix where each cell represents the preference of projects listed by students. This cell can also be interpreted as how ‘expensive’ it is to assign a student to a particular project. We are trying to find the assignment that minimizes the total ‘cost’, with each student being assigned to exactly one project.

**What does the algorithm do?**

**Step 1: Normalize Data**  
- Perform row reduction and column reduction
- Intuition: This gives every student at least one "free" option and ensures every project can be taken by at least one student. 

**Step 2: Cover all zeros with the minimum number of lines**  
- If you can cover all zeros with `n` lines (where `n` = number of students/projects), an optimal assignment can be made.  
- Otherwise, adjust the matrix (shift uncovered values) and repeat until this condition is met.  
- Intuition: Can we assign every student to a project they want and fill every project with students who want it?

**Intuition**
- Zeros in the matrix represent "feasible" assignments.  
- Drawing a line through a student means they’ve been assigned a project; drawing a line through a project means it’s already filled.  
- The algorithm keeps adjusting until it’s possible to match every student to exactly one project in a way that minimizes total cost.

## How to run the project:

Install `scipy` to run project

## Troubleshooting:

1. ### "ValueError: cost matrix is infeasible"
    This error occurs when the Hungarian algorithm cannot find valid assignments. Common causes:
    - `PREFERENCE_RANGE` is too restrictive (upper bound y is too small)

    **Solution**: Increase the upper bound of `PREFERENCE_RANGE` to allow more preference values.

## Additional Notes:
- PREASSIGNED_STUDENTS = {'StudentIdentifier1': 'ProjectA', 'StudentIdentifier2': 'ProjectB'}
    - StudentIdentifier1 depends on how we set student values in read_data_and_clean function
- The only case where there are unassigned_students is #students > #project capacities
