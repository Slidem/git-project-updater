from git_project_updater_business.scanners.project_scanner import ProjectScanner
from git_project_updater_business.models.project import Project
from git_project_updater_business.models.maven.maven_project_details import MavenProjectDetails
from git_project_updater_business.utils.argument_utils import validate_settings

from pathlib import Path

import os
import xmltodict


class MavenProjectsScanner(ProjectScanner):
    def __init__(self):
        pass

    def get_projects(self, settings):
        pom_paths = self.__get_poms(settings)
        project_map = {}
        parent_project_map = {}
        project_pom_dependencies_map = {}

        for pom_path in pom_paths:
            with open(str(pom_path), encoding="utf8") as xml_file:
                self.__convert_pom_to_project(
                    project_map, parent_project_map, project_pom_dependencies_map, xml_file)

        self.__resolve_dependenices(project_map, project_pom_dependencies_map)
        return list(project_map.values())

    def __get_poms(self, settings):
        pom_paths = []
        project_root_directory_path = str(
            Path(settings.get_project_root_directory()))

        for root, dirs, files in os.walk(project_root_directory_path):
            for file in files:
                if file == "pom.xml":
                    pom_paths.append(Path(root, file))
        return pom_paths

    def __convert_pom_to_project(self, project_map, parent_project_map, project_pom_dependencies_map, xml_file):
        pom = xmltodict.parse(xml_file.read())

        project_node = pom['project']

        artifact_id = project_node.get("artifactId", "")
        group_id = project_node.get("groupId", "")
        version = project_node.get("version", "")
        packaging = project_node.get("packaging", "jar")

        parent_node = project_node.get("parent", None)
        parent_artifact_id = artifact_id
        if parent_node:
            parent_artifact_id = parent_node.get("artifactId", "")

        project_pom_dependencies_map[artifact_id] = self.__get_project_pom_dependencies(
            project_node)

        project_details = MavenProjectDetails(
            group_id=group_id,
            artifact_id=artifact_id,
            version=version,
            packaging=packaging
        )

        project = Project(
            project_id=artifact_id,
            project_parent_id=parent_artifact_id,
            project_type="maven",
            path=Path(os.path.dirname(xml_file.name)),
            details=project_details,
            children=[],
            dependencies=[])

        if packaging == "pom":
            project_map[artifact_id] = project
            for child in parent_project_map.get(artifact_id, []):
                del project_map[child.get_project_id()]
                project.add_child(child)

        else:
            parent_project = project_map.get(parent_artifact_id, None)

            if parent_project:
                parent_project.add_child(project)

            else:
                parent_children = parent_project_map.get(
                    parent_artifact_id, None)
                if not parent_children:
                    parent_children = []
                    parent_project_map[parent_artifact_id] = parent_children
                parent_children.append(project)
                project_map[artifact_id] = project

    def __get_project_pom_dependencies(self, project_node):
        dependencies = []
        dependencies_node = project_node["dependencies"]
        for dependency_node in dependencies_node["dependency"]:
            dependencies.append(dependency_node['artifactId'])
        return dependencies

    def __resolve_dependenices(self, project_map, project_pom_dependencies_map):
        # TODO resolve dependencies based on projects and projects dependencies
