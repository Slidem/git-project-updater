from git_project_updater_business.settings.git_credentials import GitCredentials


class Settings:
    def __init__(self, git_credentials, project_root_directories, projects_type):
        if not (git_credentials and project_root_directories and projects_type):
            raise ValueError("Non null values expected")

        if not (isinstance(project_root_directories, (list, str)) and isinstance(projects_type, str) and isinstance(git_credentials, GitCredentials)):
            raise ValueError("Invalid values")

        self.__git_credentials = git_credentials
        self.__project_root_directories = project_root_directories
        self.__projects_type = projects_type

    def get_git_credentials(self):
        return self.__git_credentials

    def get_project_root_directories(self):
        return self.__project_root_directories

    def get_projects_type(self):
        return self.__projects_type

    def __str__(self):
        settings = ""
        settings += "{git_credentials}\n"
        settings += "Projects type: {projects_type}\n"
        settings += "Projects root directories {projects_root_directories}\n"

        return settings.format(
            git_credentials=self.__git_credentials,
            projects_type=self.__projects_type,
            projects_root_directories=self.__project_root_directories
        )
