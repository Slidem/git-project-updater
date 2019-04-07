from git_project_updater_business.scanners.project_scanner import ProjectScanner
from git_project_updater_business.models.project import Project
from git_project_updater_business.models.maven.maven_project_details import MavenProjectDetails
from git_project_updater_business.utils.argument_utils import validate_settings

from pathlib import Path


class MavenProjectsScanner(ProjectScanner):
    def __init__(self):
        pass

    def get_projects(self, settings):
        # TODO implement real version; bellow is for dummy testing
        validate_settings(settings)
        projects = []
        projects_root_path = Path(settings.get_project_root_directory())

        project_details = MavenProjectDetails(
            group_id="com.ami",
            artifact_id="dummy-artifact",
            version="0.0.1-SNAPSHOT",
            packaging="pom"
        )
        dummy_project = Project(
            project_id="dummy",
            project_type=settings.get_projects_type(),
            path=projects_root_path,
            details=project_details,
            children=[])

        projects.append(dummy_project)

        return projects
