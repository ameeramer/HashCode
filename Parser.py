class Project:
    def __init__(self, name, number_of_days, score, best_before, roles):
        self.name = name
        self.number_of_days = number_of_days
        self.score = score
        self.best_before = best_before
        self.roles = roles
        
class Contributor:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        
        
def parse(path):
    data = open(path, 'r')
    Lines = data.readlines()
    
    splitted_lines = []
    for line in Lines:
        splitted_lines += [line.strip().split(' ')]
    number_of_contributors = int(splitted_lines[0][0])
    number_of_projects = int(splitted_lines[0][1])
    
    contributors = []
    curr_contributor_section = 0
    curr_line = 0
    while curr_contributor_section < number_of_contributors:
        curr_line += 1
        contributor_name = splitted_lines[curr_line][0]
        number_of_skills = int(splitted_lines[curr_line][1])
        skills = dict()
        for _ in range(number_of_skills):
            curr_line += 1
            skill_name = splitted_lines[curr_line][0]
            skill_level = int(splitted_lines[curr_line][1])
            skills[skill_name] = skill_level
        contributors += [Contributor(contributor_name, skills)]
        curr_contributor_section += 1
    projects = []
    curr_project_section = 0
    while curr_line < len(splitted_lines) - 1:
        curr_line += 1
        project_name = splitted_lines[curr_line][0]
        number_of_days = int(splitted_lines[curr_line][1])
        score = int(splitted_lines[curr_line][2])
        best_before = int(splitted_lines[curr_line][3])
        number_of_roles = int(splitted_lines[curr_line][4])
        roles = dict()
        for i in range(number_of_roles):
            curr_line += 1
            skill_name = splitted_lines[curr_line][0]
            skill_level = int(splitted_lines[curr_line][1])
            roles[skill_name] = skill_level
        projects += [Project(project_name, number_of_days, score, best_before, roles)]
        
    return contributors, projects