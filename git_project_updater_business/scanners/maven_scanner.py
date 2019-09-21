from git_project_updater_business.scanners.project_scanner import ProjectScanner
from git_project_updater_business.models.project import Project
from git_project_updater_business.models.maven.maven_project import MavenProject
from git_project_updater_business.utils.argument_utils import validate_settings
from git_project_updater_business.models.maven.maven_pom import MavenPom, MavenArtifact

from pathlib import Path

import os
import xmltodict

class MavenProjectsScanner(ProjectScanner):
    def __init__(self):
        pass

    def get_projects(self, settings):
        projects = {}

        project_root_directory_path = str(
            Path(settings.projects_root_directory))

        for root, dirs, files in os.walk(project_root_directory_path):
            for file in files:
                if file == "pom.xml":
                    pom_path = Path(root, file)
                    with open(str(pom_path), encoding="utf8") as pom_xml:
                        maven_pom = self.__build_maven_pom(pom_xml)
                        projects[maven_pom.artifact.artifact_id] = MavenProject(
                            maven_pom=maven_pom,
                            project_id=maven_pom.artifact.artifact_id,
                            project_parent_id=maven_pom.parent_artifact.artifact_id if maven_pom.parent_artifact else None,
                            project_type="maven",
                            path=pom_path
                        )

        return projects

    def __build_maven_pom(self, pom_xml):
        parsed_pom = xmltodict.parse(pom_xml.read())["project"]
        artifact = self.__parse_artifact(parsed_pom)
        parent_artifact = self.__parse_artifact(parsed_pom.get("parent", None))
        modules = self.__get_modules(parsed_pom)

        dependencies = self.__get_dependencies(
            parsed_pom.get("dependencies", None))

        dependencies_management = {}
        dependencies_management_node = parsed_pom.get(
            "dependencyManagement", None)

        if dependencies_management_node:
            dependencies_management = self.__get_dependencies(
                dependencies_management_node["dependencies"])

        return MavenPom(
            artifact=artifact,
            parent_artifact=parent_artifact,
            modules=modules,
            dependencies=dependencies,
            dependencies_management=dependencies_management
        )

    def __get_dependencies(self, xml_node):
        if not xml_node:
            return {}
        dependencies = xml_node.get("dependency", None)

        if not dependencies:
            return {}

        dependencies_artifacts = map(
            lambda d: self.__parse_artifact(d), dependencies)
        dependencies_artifacts = filter(None, dependencies_artifacts)
        return {a.artifact_id: a for a in dependencies_artifacts}

    def __get_modules(self, parsed_pom):
        modules_node = parsed_pom.get("modules", None)
        if modules_node:
            modules = modules_node.get("module", None)
            if modules:
                return modules.copy()
        return []

    def __parse_artifact(self, xml_node):

        if not xml_node or not isinstance(xml_node, dict):
            return None

        return MavenArtifact(
            artifact_id=xml_node.get("artifactId", None),
            group_id=xml_node.get("groupId", None),
            scope=xml_node.get("scope", None),
            packaging=xml_node.get("packaging", None),
            version=xml_node.get("version", None)
        )
