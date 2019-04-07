from git_project_updater_business.models.project_details import ProjectDetails


class MavenProjectDetails(ProjectDetails):
    def __init__(self, group_id, artifact_id, version, packaging):
        pass

    def _get_details_string(self):
        return "maven details... to be implemnted"
