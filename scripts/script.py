from scipy.optimize import linear_sum_assignment
import csv
import numpy as np

# Update these constants depending on scenario
MAX_PER_PROJECT = 4
MIN_PROPOSAL_VALUE = 6
MIN_SATISFACTION_VALUE = 5
COL_PROJ_INDEX = 4 # the column index which projects start from (depending on dataset)
EXCLUDE_PROJ_INDEXES = [] # list of project indexes to exclude from matching
EXCEPTIONS = {} # dict of exceptions with capacity of projects
DATA_PATH = 'output/wrangled_data.csv'
OUTPUT_PATH = '/output/'
PATH = './'
PREASSIGNED_STUDENTS = {} # dict of students we want to pre-assigned to projects
PREFERENCE_RANGE = (1, 12) # Range of preferences to accept (x, y) x <= pref <= y
DATA_START_ROW_INDEX = 1

def read_data_and_clean():
    students = []
    projects = []
    preferences = {}
    rankings = {}
    count_map = {}

    with open(PATH + DATA_PATH, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                projects = row[COL_PROJ_INDEX:]
                rankings = {project: [] for project in projects}
                count_map = {project: {str(i): 0 for i in range(1, 100)} for project in projects}
            elif i >= DATA_START_ROW_INDEX:
                if not row:
                    continue
                student = f'{row[0]} {row[1]} ({row[2]})' # Note: replace this student identifier as provided in dataset
                if student:
                    if student in students:
                        print('Found duplicate student:', student)
                    else:
                        students.append(student)
                        preferences[student] = {}
                        for j, col in enumerate(row[COL_PROJ_INDEX:]):
                            if not col:
                                col = str(len(row[COL_PROJ_INDEX:]))
                            project = projects[j]
                            preferences[student][project] = col
                            rankings[project].append((student, col))
                            count_map[project][str(col)] += 1

    c = 0
    temp = {project: '' for project in projects}
    for project, dict in count_map.items():
        s = dict['1'] + dict['2']
        temp[project] = s
        c += 1

    for ranking, items in rankings.items():
        items.sort(key=lambda x: int(x[1]))

    ranking_map = {project: {} for project in projects}
    for project, items in rankings.items():
        maxx = -1
        rank = 1
        for item in items:
            student = item[0]
            pref = item[1]

            if maxx == -1:
                maxx = int(pref)
            elif int(pref) > maxx:
                maxx = int(pref)
                rank += 1

            ranking_map[project][student] = str(rank)

    max_per_projects = {}
    for p in projects:
        if p in EXCEPTIONS:
            max_per_projects[p] = EXCEPTIONS[p]
        else:
            max_per_projects[p] = MAX_PER_PROJECT

    return students, projects, max_per_projects, preferences, ranking_map


def calculate_averages_of_proposals(projects, allocations, proposals):
    averages_dict = {project: 0.0 for project in projects}

    for project, students in allocations.items():
        if len(students) > 0:
            total = 0
            for student in students:
                total += int(proposals[student])
               
            averages_dict[project] = total / len(students)
        else:
             averages_dict[project] = 0.0

    averages = [avg for p, avg in averages_dict.items()]
    indexes = sorted(range(len(averages)), key=lambda i: averages[i])
    
    averages_out = {}
    for i in range(len(averages)):
        averages_out[projects[i]] = averages[i]

    # Minor Addition: Only include projects with allocations when calculating overall average
    allocated_projects = {p: avg for p, avg in averages_out.items() if avg > 0.0}
    overall_average = sum(allocated_projects.values()) / len(allocated_projects) if allocated_projects else 0.0

    return averages_out, indexes, overall_average

# Assigns students their projects based on preference using Hungarian Algorithm with filtering
def match_students_to_projects(students, projects, max_per_projects, preferences, ranking_map):
    allocations = {project: [] for project in projects}
    proposals = {student: '' for student in students}
    ranking_allocations = {student: '' for student in students}

    adjusted_max_per_projects = max_per_projects.copy()
    
    if PREASSIGNED_STUDENTS:
        for student, project in PREASSIGNED_STUDENTS.items():
            if student in students and project in projects:
                allocations[project].append(student)
                proposals[student] = str(preferences[student][project])
                ranking_allocations[student] = ranking_map[project][student]
                adjusted_max_per_projects[project] -= 1
            else:
                print(f"Warning: Preassigned student ({student}) or project ({project}) not found in current dataset")

    # Retrieve all students who are not preassigned in PREASSIGNED_STUDENTS
    available_students = [s for s in students if s not in PREASSIGNED_STUDENTS]
    
    # Hungarian Algorithm matches one student to one project, and since the capacity of each project differs
    # we have to duplicate projects based on capacity
    # Eg: project with their space = [A: 3, B: 2]
    # project_copies = [A, A, A, B, B]
    project_copies = []
    for i, project in enumerate(projects):
        if i not in EXCLUDE_PROJ_INDEXES:
            capacity = adjusted_max_per_projects[project]
            for _ in range(capacity):
                project_copies.append(project)

    # row = students (exclude students who are in PREASSIGNED_STUDENTS)
    # col = projects (include duplicates due to multiple capacity in a group)
    # value in matrix = student's preference of that project
    rows = len(available_students)
    cols = len(project_copies)
    student_proj_pref_matrix = [[0] * cols for _ in range(rows)]

    for i, student in enumerate(available_students):
        for j, project_copy in enumerate(project_copies):
            pref_rank = preferences[student][project_copy]

            if PREFERENCE_RANGE[0] <= int(pref_rank) <= PREFERENCE_RANGE[1]:
                student_proj_pref_matrix[i][j] = preferences[student][project_copy]
            else:
                student_proj_pref_matrix[i][j] = float('inf') 

    # Solves linear sum assignment problem
    # Return: array of row indices and one of corresponding col indices to provide optimal assignment
    row_ind, col_ind = linear_sum_assignment(student_proj_pref_matrix)

    for student_idx, project_copy_idx in zip(row_ind, col_ind):
        student = available_students[student_idx]
        project = project_copies[project_copy_idx]  
        pref_rank = preferences[student][project]

        allocations[project].append(student)
        proposals[student] = str(pref_rank)
        ranking_allocations[student] = ranking_map[project][student]

    unassigned_students = []
    for sid, pref in proposals.items():
        if not pref:
            unassigned_students.append(sid)

    return allocations, proposals, ranking_allocations, unassigned_students


def write_csv(allocations, proposals, ranking_allocations):
    allocations_items = []
    for project, students in allocations.items():
        temp = []
        temp.append(project)
        for student in students:
            temp.append(student)
        allocations_items.append(temp)

    save('allocations.csv', allocations_items)


    proposals_items = []
    for project, students in allocations.items():
        temp = []
        temp.append(project)
        for student in students:
            proposal = proposals[student]
            temp.append(str(proposal))
        proposals_items.append(temp)

    save('proposals.csv', proposals_items)

    ranking_allocations_items = []
    for project, students in allocations.items():
        temp = []
        temp.append(project)
        for student in students:
            ranking_allocation = ranking_allocations[student]
            temp.append(str(ranking_allocation))
        ranking_allocations_items.append(temp)

    save('ranking_allocations.csv', ranking_allocations_items)


def save(filename, items):
    with open(PATH + OUTPUT_PATH + filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in items:
            writer.writerow(item)  

            

if __name__ == '__main__':
    students, projects, max_per_projects, preferences, ranking_map = read_data_and_clean()

    allocations, proposals, ranking_allocations, unassigned_students = match_students_to_projects(students, projects, max_per_projects, preferences, ranking_map)
    print("Unassigned students: ", unassigned_students)
    write_csv(allocations, proposals, ranking_allocations)

    averages_out, indexes, overall_average = calculate_averages_of_proposals(projects, allocations, proposals)
    print("Overall Average: ", overall_average)

   