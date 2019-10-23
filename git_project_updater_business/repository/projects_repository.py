class ProjectsRepository:
    __instance = None

    @staticmethod
    def get_instance(settings_repository, project_scanner_factory):
        if ProjectsRepository.__instance is None:
            ProjectsRepository(settings_repository, project_scanner_factory)
        return ProjectsRepository.__instance

    def __init__(self, settings_repository, project_scanner_factory):
        """ Virtually private constructor. """
        if ProjectsRepository.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.settings_repository = settings_repository
            self.project_scanner_factory = project_scanner_factory
            self.__projects = None
            ProjectsRepository.__instance = self

    @property
    def projects(self):
        if not self.__projects:
            self.refresh_projects()
        return self.__projects

    def refresh_projects(self):
        self.__read_projects()

    def __read_projects(self):
        settings = self.settings_repository.get_settings()
        if not settings:
            print("Warning! Settings have not been set yet, projects will be empty")
        else:
            self.__projects = self.project_scanner_factory.compute_scanner(
                settings).scan_for_projects(settings)
