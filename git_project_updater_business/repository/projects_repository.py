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
            self.__projects = project_scanner_factory.get_projects_scanner(
                settings).get_projects(settings)

        return self.__projects
