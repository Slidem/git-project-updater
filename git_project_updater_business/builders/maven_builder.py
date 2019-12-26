from nxpy import maven
from git_project_updater_business.models.project import Project
from git_project_updater_business.builders.maven_wrapper import MvnWrapper


class MavenBuilder:

    mvn_wrapper = MvnWrapper(False)

    def build(self, project: Project, *commands):
        if not project:
            return

        project_path = str(project.path.joinpath("pom.xml"))
        print(f"Building maven project for path {project_path}")

        path_as_list = [project_path]

        if not commands or not all(commands):
            self.__run_default_commands(path_as_list)
        else:
            MavenBuilder.mvn_wrapper.run_maven_commands(path_as_list, commands)

    def __run_default_commands(self, path_as_list):
        MavenBuilder.mvn_wrapper.clean(path_as_list)
        MavenBuilder.mvn_wrapper.install(path_as_list)
