from git_project_updater_business.scanners.project_scanner import ProjectScanner


class EmptyProjectScanner:
    def __init__(self):
        pass

    def get_projects(self, settings):
        return []
