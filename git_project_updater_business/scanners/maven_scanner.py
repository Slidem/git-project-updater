from git_project_updater_business.scanners.project_scanner import ProjectScanner
from git_project_updater_business.models.project import Project
from git_project_updater_business.models.maven.maven_project import MavenProject
from git_project_updater_business.utils.argument_utils import validate_settings
from git_project_updater_business.models.maven.maven_pom import MavenPom, MavenArtifact
from git_project_updater_business.scanners.converter.maven.pom_to_project_converter import PomToProjectConverter

from pathlib import Path

import os
import xmltodict


class MavenProjectsScanner(ProjectScanner):
    def __init__(self):
        pass

    def scan_for_projects(self, settings):

        project_root_directory_path = self.__get_normalized_root_path(settings)
        pom_to_project_converter = PomToProjectConverter()

        # recursively walk the projects root, and parse each pom.xml file into a valid Project instance
        for root, dirs, files_in_root in os.walk(project_root_directory_path):
            for file in files_in_root:
                # skip non pom.xml files
                if file != "pom.xml":
                    continue

                pom_path = Path(root, file)

                # open pom file, and parse it into a MavenPom instance
                with open(str(pom_path), encoding="utf8") as pom_xml:
                    pom_to_project_converter.convert_to_project(pom_path, pom_xml)

        return pom_to_project_converter.compute_projects()

    def __get_normalized_root_path(self, settings):
        return str(Path(settings.projects_root_directory))

    
