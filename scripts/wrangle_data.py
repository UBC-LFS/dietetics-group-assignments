import csv
import re

# This script processes Will's dataset, where each student selects up to their top 3 project preferences.
# Projects not ranked by a student are automatically assigned the worst possible rank (TOTAL_NUM_PROJECTS).

# Update these constants depending on scenario
DATA_PATH = 'data/raw.csv'
OUTPUT_FILE = 'output/wrangled_data.csv'
PATH = './'
HEADER_NAMES = ['First Name', 'Last Name', 'Student Number', 'Is Dietetics']
TOTAL_NUM_PROJECTS = 12

def extract_project_name(name):
    if not name or name.strip() == '':
        return None
     
    return re.sub(r'^\d+\.\s*', '', str(name).strip())

# Extracts project number and returns index
def extract_proj_number(project_string):
    if not project_string:
        return None
    match = re.match(r'(\d+)\.', project_string.strip())
    return int(match.group(1))
    

def read_data_and_clean():
    students = []
    projects = [None] * TOTAL_NUM_PROJECTS

    student_data = []
    
    with open(PATH + DATA_PATH, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                continue
            if len(row) >= 7: # Assume we have 7 columns
                first_name = row[1]
                last_name = row[0]
                student_number = row[2]
                dietetics = row[6]
                project_choices = [row[3], row[4], row[5]]
                
                for proj in project_choices:
                    idx = extract_proj_number(proj)
                    if idx is not None and not projects[idx - 1]:
                        projects[idx - 1] = proj

                student_data.append((first_name, last_name, student_number, dietetics, project_choices))
    
    for student in student_data:
        first_name, last_name, student_number, dietetics, project_choices = student

        student_info = {
            HEADER_NAMES[0]: first_name,
            HEADER_NAMES[1]: last_name,
            HEADER_NAMES[2]: student_number,
            HEADER_NAMES[3]: dietetics,
        }

        choice_ranks = {proj: rank for rank, proj in enumerate(project_choices, start=1)}
        for proj in projects:
            student_info[proj] = choice_ranks.get(proj, TOTAL_NUM_PROJECTS)

        students.append(student_info)

    return students, projects


def write_to_csv(students, projects, output_file):
    HEADER = HEADER_NAMES + projects

    with open(output_file, 'w', newline='', encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)


if __name__ == '__main__':
    students, projects= read_data_and_clean()
    write_to_csv(students, projects, OUTPUT_FILE)

                    



