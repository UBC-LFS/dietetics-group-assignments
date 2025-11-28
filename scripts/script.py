from scipy.optimize import linear_sum_assignment
import PySide6.QtWidgets as widget
import csv
import os

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
            "student_first_number": 0,
            "student_last_name": 1,
            "student_email": 2,
            "student_number": 3,
            "project_column_index": 4
        }}
}

def retrieve_student_field_and_proj(header_option_val):
    header_option = HEADER_OPTIONS[header_option_val]["indices"]

    student_fields = {
        header: idx for header, idx in header_option.items()
        if header != "project_column_index"
    }

    proj_col_index = HEADER_OPTIONS[header_option_val]["indices"]["project_column_index"]

    return student_fields, proj_col_index

def read_data_and_clean(data_path, student_fields, proj_col_index, max_per_project, exceptions, inclusions, exclusions):
    students = {}
    projects = []
    original_preferences = {}
    preferences = {}
    rankings = {}
    count_map = {}

    with open(data_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                projects = row[proj_col_index:]
                rankings = {project: [] for project in projects}
                count_map = {project: {str(i): 0 for i in range(1, 100)} for project in projects}
            else:
                if not row:
                    continue
                student = { header: row[idx] for header, idx in student_fields.items() }
                student_id = student['student_number']
                if student_id:
                    if student_id in students:
                        raise ValueError(f"Duplicate student found: {student}")
                    
                    students[student_id] = student
                    preferences[student_id] = {}
                    original_preferences[student_id] = {}
                    for j, col in enumerate(row[proj_col_index:]):
                        project = projects[j]
                        original_preferences[student_id][project] = col # keeps the original data in the final csv file generated
                        if col.strip() != "" and not col.strip().isdigit():
                            raise ValueError(f"Invalid value '{col}' as project ranking. Expected a number or empty cell.")
                        
                        if not col:
                            col = str(len(row[proj_col_index:]))
                        
                        if student_id in inclusions and project not in inclusions[student_id]:  
                            preferences[student_id][project] = float('inf')
                            rankings[project].append((student_id, float('inf')))
                        elif student_id in exclusions and project in exclusions[student_id]:
                            preferences[student_id][project] = float('inf')
                            rankings[project].append((student_id, float('inf')))
                        else:
                            preferences[student_id][project] = col
                            rankings[project].append((student_id, col))
                        count_map[project][str(col)] += 1

    c = 0
    temp = {project: '' for project in projects}
    for project, dict in count_map.items():
        s = dict['1'] + dict['2']
        temp[project] = s
        c += 1

    for ranking, items in rankings.items():
        items.sort(key=lambda x: float(x[1]))

    ranking_map = {project: {} for project in projects}
    for project, items in rankings.items():
        maxx = -1
        rank = 1
        for item in items:
            student_id = item[0]
            pref = float(item[1])

            if maxx == -1:
                maxx = pref
            elif pref > maxx:
                maxx = pref
                rank += 1

            ranking_map[project][student_id] = str(rank)

    invalid_projects = [p for p in exceptions if p not in projects]
    if invalid_projects:
        raise ValueError("Project(s) not found in the dataset: " + ", ".join(invalid_projects))

    max_per_projects = {}
    for p in projects:
        if p in exceptions:
            max_per_projects[p] = exceptions[p]
        else:
            max_per_projects[p] = max_per_project

    return students, projects, max_per_projects, preferences, ranking_map, original_preferences


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

# Find all pairs of students who can swap projects without changing total cost
def find_equal_cost_swaps(students, student_allocated_project, preassigned_students, preferences):

    available_students_ids = [sid for sid in students.keys() if sid not in preassigned_students]
    n = len(available_students_ids)

    swap_pairs = []
  
    for i in range(n):
        for j in range(i+1, n):
            student_id1 = available_students_ids[i]
            student_id2 = available_students_ids[j]

            if "student_name" in students[student_id1]:
                student_id1_name = f"{students[student_id1]['student_name']}"
                student_id2_name = f"{students[student_id2]['student_name']}"
            else:
                student_id1_name = f"{students[student_id1]['student_first_name']} {students[student_id1]['student_last_name']}"
                student_id2_name = f"{students[student_id2]['student_first_name']} {students[student_id2]['student_last_name']}"

            project_i = student_allocated_project[student_id1]
            project_j = student_allocated_project[student_id2]
            current_cost_i= preferences[student_id1][project_i]
            current_cost_j = preferences[student_id2][project_j]
            swapped_cost_i = preferences[student_id1][project_j]
            swapped_cost_j = preferences[student_id2][project_i]

            # If the students are allocated to the same project
            if project_i == project_j:
                continue
            
            if current_cost_i == float('inf') or current_cost_j == float('inf') or swapped_cost_i == float('inf') or swapped_cost_j == float('inf'):
                continue

            current_cost = int(current_cost_i) + int(current_cost_j)
            swap_cost = int(swapped_cost_i) + int(swapped_cost_j)

            if swap_cost == current_cost:
                swap_pairs.append({
                    's1_number': student_id1,
                    's2_number': student_id2,
                    's1_name': student_id1_name,
                    's2_name': student_id2_name,
                    'proj1': project_i,
                    'proj2': project_j,
                    's1_cur_rank': current_cost_i,
                    's2_cur_rank': current_cost_j,
                    's1_swap_rank': swapped_cost_i,
                    's2_swap_rank': swapped_cost_j
                })
    return swap_pairs

# Assigns students their projects based on preference using Hungarian Algorithm with filtering
def match_students_to_projects(students, projects, max_per_projects, preferences, ranking_map, pref_range, preassigned_students):
    allocations = {project: [] for project in projects}
    proposals = {sid: '' for sid in students.keys()}
    ranking_allocations = {sid: '' for sid in students.keys()}

    adjusted_max_per_projects = max_per_projects.copy()
    
    if preassigned_students:
        for student_id, project in preassigned_students.items():
            if student_id not in students:
                raise ValueError(f"Preassigned student '{student_id}' not found in dataset.")
            if project not in projects:
                raise ValueError(f"Preassigned project '{project}' not found in dataset.")
     
            allocations[project].append(student_id)
            proposals[student_id] = str(preferences[student_id][project])
            ranking_allocations[student_id] = ranking_map[project][student_id]
            adjusted_max_per_projects[project] -= 1
           
    # Retrieve all students who are not preassigned in preassigned_students
    available_students = [sid for sid in students.keys() if sid not in preassigned_students]
    
    # Hungarian Algorithm matches one student to one project, and since the capacity of each project differs
    # we have to duplicate projects based on capacity
    # Eg: project with their space = [A: 3, B: 2]
    # project_copies = [A, A, A, B, B]
    project_copies = []
    for i, project in enumerate(projects):
        capacity = adjusted_max_per_projects[project]
        for _ in range(capacity):
            project_copies.append(project)

    # row = students (exclude students who are in preassigned_students)
    # col = projects (include duplicates due to multiple capacity in a group)
    # value in matrix = student's preference of that project
    rows = len(available_students)
    cols = len(project_copies)
    student_proj_pref_matrix = [[0] * cols for _ in range(rows)]

    for i, student_id in enumerate(available_students):
        for j, project_copy in enumerate(project_copies):
            pref_rank = preferences[student_id][project_copy]
            if pref_rank == float('inf'):
                student_proj_pref_matrix[i][j] = float('inf')
            else:
                if pref_range[0] <= int(pref_rank) <= pref_range[1]:
                    student_proj_pref_matrix[i][j] = int(pref_rank)
                else:
                    student_proj_pref_matrix[i][j] = float('inf')

    # Solves linear sum assignment problem
    # Return: array of row indices and one of corresponding col indices to provide optimal assignment
    row_ind, col_ind = linear_sum_assignment(student_proj_pref_matrix)

    for student_idx, project_copy_idx in zip(row_ind, col_ind):
        student_id = available_students[student_idx]
        project = project_copies[project_copy_idx]  
        pref_rank = preferences[student_id][project]

        allocations[project].append(student_id)
        proposals[student_id] = str(pref_rank)
        ranking_allocations[student_id] = ranking_map[project][student_id]

    unassigned_students = []
    for sid, pref in proposals.items():
        if not pref:
            unassigned_students.append(sid)

    if len(unassigned_students) > 0:
        raise ValueError("There are unassigned student(s) due to insufficient capacity. Fix the capacity of projects before proceeding.")
    return allocations

def map_students_to_projects(allocations):
    student_allocated_project = {}
    for project, student_list in allocations.items():
        for student_id in student_list:
            student_allocated_project[student_id] = project

    return student_allocated_project

def check_folder_existence(output_path, output_folder_name):
    existing_folders = os.listdir(output_path)
    if any(folder.lower() == output_folder_name.lower() for folder in existing_folders):
        msg_box = widget.QMessageBox()
        msg_box.setIcon(widget.QMessageBox.Question)
        msg_box.setWindowTitle("Overwrite Folder?")
        msg_box.setText(f"The folder '{output_folder_name}' already exists.\nDo you want to overwrite its contents?")
        msg_box.setStandardButtons(widget.QMessageBox.Yes | widget.QMessageBox.No)
        msg_box.setDefaultButton(widget.QMessageBox.No)
        
        overwrite = msg_box.exec() == widget.QMessageBox.Yes
        if not overwrite:
            raise FileExistsError(f"The folder '{output_folder_name}' already exists and overwrite was cancelled.")

def write_csv_for_canvas_group(output_path, allocations, preferences, output_folder_name):
    header = ['user_id', 'group_name', 'ranking']
    rows = [header]

    for allocated_proj, students in allocations.items():
        for student_id in students:
            ranking = preferences.get(student_id, {}).get(allocated_proj, "")
            rows.append([student_id, allocated_proj, ranking])

    save(output_path, "canvas-group-allocations.csv", rows, output_folder_name)

def write_csv_for_swap(output_path, swap_pairs, output_folder_name):
    header = ['Pair', 'Student Pair Name', 'Student Pair Number', 'Current Assigned Group', 'Current Rank', 'Swapped Group', 'Swapped Rank']
    rows = [header]
    
    for i, pair in enumerate(swap_pairs):
        student1_num, student2_num = pair['s1_number'], pair['s2_number']
        student1_name, student2_name = pair['s1_name'], pair['s2_name']
        project1, project2 = pair['proj1'], pair['proj2']
        s1_cur_rank, s2_cur_rank = pair['s1_cur_rank'], pair['s2_cur_rank']
        s1_swap_rank, s2_swap_rank = pair['s1_swap_rank'], pair['s2_swap_rank']

        student_1 = [
            f'{i + 1}',
            f'{student1_name}',
            f'{student1_num}',
            f'{project1}',
            f'{s1_cur_rank}',
            f'{project2}',
            f'{s1_swap_rank}'
        ]
        rows.append(student_1)

        student_2 = [
            f'{i + 1}',
            f'{student2_name}',
            f'{student2_num}',
            f'{project2}',
            f'{s2_cur_rank}',
            f'{project1}',
            f'{s2_swap_rank}'
        ]
        rows.append(student_2)
        rows.append([])

    save(output_path, "student-project-swaps.csv", rows, output_folder_name)

def write_csv_for_allocations(output_path, student_fields, student_allocated_project, students, preferences, projects, output_folder_name):
    
    ordered_student_fields = [
        field for field, _ in sorted(student_fields.items(), key=lambda x: x[1])
    ]
    
    header = ordered_student_fields + ["allocated_project", "ranking_for_allocated_project"]
    for project in projects:
        header.append(f"{project}")

    rows = [header]

    for student_id, student_info in students.items():
        row_dict = {}

        for field in ordered_student_fields:
            row_dict[field] = student_info.get(field, "")

        allocated_project = student_allocated_project.get(student_id, "")
        allocated_ranking = preferences.get(student_id, {}).get(allocated_project, "")
        row_dict["allocated_project"] = allocated_project
        row_dict["ranking_for_allocated_project"] = allocated_ranking

        for project in projects:
            row_dict[project] = preferences.get(student_id, {}).get(project, "")
        
        row = [row_dict[h] for h in header]
        rows.append(row)

    save(output_path, "student-project-allocations.csv", rows, output_folder_name)


def save(output_path, filename, items, output_folder_name): 
    results_folder = os.path.join(output_path, output_folder_name)
    os.makedirs(results_folder, exist_ok=True)

    file_path = os.path.join(results_folder, filename)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in items:
            writer.writerow(item)  


def run_script(data_path, output_path, max_per_project, pref_range, capacity_exceptions, preassigned_students, inclusions, exclusions, output_folder_name, header_option):
    student_fields, proj_col_index = retrieve_student_field_and_proj(header_option)
    students, projects, max_per_projects, preferences, ranking_map, original_preferences = read_data_and_clean(data_path, student_fields, proj_col_index, max_per_project, capacity_exceptions, inclusions, exclusions)

    check_folder_existence(output_path, output_folder_name)

    allocations = match_students_to_projects(students, projects, max_per_projects, preferences, ranking_map, pref_range, preassigned_students)
    student_allocated_project = map_students_to_projects(allocations)
    swap_pairs = find_equal_cost_swaps(students, student_allocated_project, preassigned_students, preferences)

    write_csv_for_allocations(output_path, student_fields, student_allocated_project, students, original_preferences, projects, output_folder_name)
    write_csv_for_canvas_group(output_path, allocations, preferences, output_folder_name)
    write_csv_for_swap(output_path, swap_pairs, output_folder_name)


   