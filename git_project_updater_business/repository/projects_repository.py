class ProjectsRepository:
    __instance = None
    __projects = None

    @staticmethod
    def get_instance():
        if ProjectsRepository.__instance == None:
            ProjectsRepository()
        return ProjectsRepository.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ProjectsRepository.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ProjectsRepository.__instance = self

    def get_projects(self, settings, project_scanner_factory):
        if not self.__projects:
            self.__read_projects(settings, project_scanner_factory)
        return self.__projects

    def refresh_projects(self, settings, project_scanner_factory):
        self.__read_projects(settings, project_scanner_factory)

    def __read_projects(self, settings, project_scanner_factory):
        self.__projects = project_scanner_factory.get_projects_scanner(
            settings).get_projects(settings)
