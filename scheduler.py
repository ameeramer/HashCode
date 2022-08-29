import  pandas as pd
class Scheduler:
    def __init__(self, projects, contributors):
        self.projects = projects
        self.contributors = contributors

    def get_doable_tasks(self, contributors=None):
        # Iterate over tasks and checks if some people can perform the task
        res = []
        for project in self.projects:
            if self.is_project_doable(project, contributors):
                res.append(res)
        return res

    def is_project_doable(self, project, contributors=None):
        if not contributors:
            free_conts = self.contributors
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



    def prioritize_projects(self,projects):
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
        projects_df["name"].tolist()
    def schedule(self):
        pass