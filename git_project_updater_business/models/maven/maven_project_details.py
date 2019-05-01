from git_project_updater_business.models.project_details import ProjectDetails


class MavenProjectDetails(ProjectDetails):
    def __init__(self, group_id, artifact_id, version, packaging):
        self.__group_id = group_id
        self.__artifact_id = artifact_id
        self.__version = version
        self.__packaging = packaging
        pass

    def _get_details_string(self):
        details = ""
        details += "artifactId: " + self.__artifact_id + "\n"
        details += "group_id: " + self.__group_id + "\n"
        details += "version: " + self.__version + "\n"
        details += "packaging: " + self.__packaging
        return details
