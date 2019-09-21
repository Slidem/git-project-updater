from git_project_updater_business.models.project import Project
from git_project_updater_business.models.maven.maven_pom import MavenPom
from abc import *


class MavenProject(Project):

    def __init__(self, **kwargs):
        self.maven_pom = kwargs["maven_pom"]
        self.__validate()
        super(MavenProject, self).__init__(**kwargs)

    def __validate(self):
        if not isinstance(self.maven_pom, MavenPom):
            raise ValueError("Expected valid MavenPom")

    def _get_details_str(self):
        return str(self.maven_pom.artifact)
