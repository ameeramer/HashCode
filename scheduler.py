import pandas as pd


class Scheduler:
    def __init__(self, projects, contributors):
        self.projects = projects
        self.contributors = contributors

    def get_doable_tasks(self, contributors=None):
        # Iterate over tasks and checks if some people can perform the task
        res = []
        for project in self.projects:
            if self.is_project_doable(project, contributors):
                res.append(project)
        return res

    def is_project_doable(self, project, contributors=None):
        if not contributors:
            free_conts = self.contributors.copy()
        else:
            free_conts = contributors

        for skill, level in project.roles.items():
            can_perform_skill = False
            for cont in free_conts:
                if cont.skills.get(skill, 0) >= level:
                    free_conts.remove(cont)
                    can_perform_skill = True
                    break
            if not can_perform_skill:
                return False
        return True

    def prioritize_projects(self, projects):
        projects_df = pd.DataFrame(columns=['name', 'days', 'score', 'best_before', 'roles'])
        for proj in projects:
            projects_df = projects_df.append({
                'name': proj.name,
                'days': proj.number_of_days,
                'score': proj.score,
                'best_before': proj.best_before,
                'roles': len(proj.roles)
            }, ignore_index=True)
        projects_df["score_rate"] = projects_df["score"] / projects_df["days"]
        projects_df["start_deadline"] = projects_df["best_before"] - projects_df["days"]
        projects_df = projects_df.sort_values(by=["start_deadline", "score_rate"], ascending=[True, False])
        return projects_df.index.to_list()

    def schedule(self):
        pass

    def allocate(self, project, contributors):
        if not self.is_project_doable(project, contributors):
            raise Exception('Project is not doable')

        allocated_contributors = []
        for skill, level in project.roles.items():
            contributors_for_skill_ids = []
            contributors_for_skill_levels = []
            contributors_for_skill_number_of_skills = []
            for cont_id, cont in enumerate(contributors):
                if cont.skills.get(skill, -1) >= level:
                    contributors_for_skill_ids += [cont_id]
                    contributors_for_skill_levels += [cont.skills.get(skill)]
                    contributors_for_skill_number_of_skills += [len(cont.skills)]

            conts_df = pd.DataFrame({'cont_id': contributors_for_skill_ids,
                                     'level': contributors_for_skill_levels,
                                     'number_of_skills': contributors_for_skill_number_of_skills})

            chosen_cont_id = conts_df.sort_values(by=['level', 'number_of_skills']).head(1)['cont_id'].item()
            allocated_contributors += [contributors[chosen_cont_id]]
            del contributors[chosen_cont_id]

        return allocated_contributors
