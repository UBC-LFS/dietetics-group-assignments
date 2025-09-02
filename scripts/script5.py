import csv
import numpy as np

PATH = './'

MAX_PER_PROJECT = 1
MIN_PROPOSAL_VALUE = 6
MIN_SATISFACTION_VALUE = 5


def read_data_and_clean():
    students = []
    projects = []
    preferences = {}
    rankings = {}
    count_map = {}

    with open(PATH + 'data5/year5.csv', 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == 0:
                projects = row[2:]
                rankings = {project: [] for project in projects}
                count_map = {project: {str(i): 0 for i in range(1, 100)} for project in projects}
            else:
                student = f'{row[0]} ({row[1]})'
                if student:
                    if student in students:
                        print('Found duplicate student:', student)
                    else:
                        students.append(student)
                        preferences[student] = {}
                        for j, col in enumerate(row[2:]):
                            if not col:
                                col = str(len(row[2:]))
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
        max_per_projects[p] = MAX_PER_PROJECT


    return students, projects, max_per_projects, preferences, rankings, ranking_map


def get_averages_of_preferences(projects, preferences):
    totals = [0] * len(projects)
    counts = [0] * len(projects)
    averages = [0] * len(projects)

    for st, prefs in preferences.items():
        i = 0
        for project_name, pref in prefs.items():
            counts[i] += 1
            totals[i] += int(pref)
            i += 1

    for i in range(len(totals)):
        averages[i] = totals[i] / counts[i]

    indexes = sorted(range(len(averages)), key=lambda i: averages[i], reverse=True)
    
    return indexes


def matching_first_round(students, projects, max_per_projects, preferences, rankings, ranking_map):
    indexes = get_averages_of_preferences(projects, preferences)

    allocations = {project: [] for project in projects}
    proposals = {student: '' for student in students}
    ranking_allocations = {student: '' for student in students}

    for i in indexes:
        if i == 7:
            print(projects[i])
            continue

        project = projects[i]
        proejct_rankings = rankings[project]

        for j, item in enumerate(proejct_rankings):
            student = item[0]
            pref = item[1]
            if not proposals[student] and pref in [str(k) for k in range(1,17)]:
                allocations[project].append(student)
                proposals[student] = pref
                ranking_allocations[student] = ranking_map[project][student]

                allocations[project].sort(key=lambda s: int(preferences[s][project]))

                if len(allocations[project]) > max_per_projects[project]:
                    rejected_student = allocations[project].pop()
                    proposals[rejected_student] = ''
                    ranking_allocations[rejected_student] = ''


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
    with open(PATH + '/output5/' + filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for item in items:
            writer.writerow(item)


def checking(projects, max_per_projects, preferences, allocations, proposals, ranking_allocations, unassigned_students):
    for student in unassigned_students:
        this_group = ''
        this_proposal = proposals[student]
        this_prefs = dict(sorted(preferences[student].items(), key=lambda a: int(a[1])))

        for project, members in allocations.items():
            if student in members:
                this_group = project
                break

        possible_projects = []
        i = 0
        for pro, pref in this_prefs.items():
            if i < 9:
                possible_projects.append(pro)
            i += 1

        for pro in possible_projects:
            assigned_memnbers = allocations[pro]
            for member in assigned_memnbers:
                their_prefs = dict(sorted(preferences[member].items(), key=lambda a: int(a[1])))
                if member not in students:
                    print(member, list(their_prefs.keys()))


if __name__ == '__main__':
    students, projects, max_per_projects, preferences, rankings, ranking_map = read_data_and_clean()

    allocations, proposals, ranking_allocations, unassigned_students = matching_first_round(students, projects, max_per_projects, preferences, rankings, ranking_map)

    # checking(projects, max_per_projects, preferences, allocations, proposals, ranking_allocations, unassigned_students)
    write_csv(allocations, proposals, ranking_allocations)