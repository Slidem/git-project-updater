from git_project_updater_business.settings.git_credentials import GitCredentials


class Settings:
    def __init__(self, git_credentials, projects_root_directory, projects_type):
        if not (git_credentials and projects_root_directory and projects_type):
            raise ValueError("Non null values expected")

        if not (isinstance(projects_root_directory, str) and isinstance(projects_type, str) and isinstance(git_credentials, GitCredentials)):
            raise ValueError("Invalid values")

        self.git_credentials = git_credentials
        self.projects_root_directory = projects_root_directory
        self.projects_type = projects_type

    def __str__(self):
        settings = ""
        settings += "{git_credentials}\n"
        settings += "Projects type: {projects_type}\n"
        settings += "Projects root directory {projects_root_directories}\n"

        return settings.format(
            git_credentials=self.git_credentials,
            projects_type=self.projects_type,
            projects_root_directories=self.projects_root_directory
        )

        self.git_credentials = git