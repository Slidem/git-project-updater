from abc import ABC, abstractmethod
from xml.etree import ElementTree
from enum import enum, auto
from git_project_updater_business.models.project import Project


class ProjectVersionChanger(ABC):

    def __init__(self, project_service):
        self.project_service = project_service

    @abstractmethod
    def change(self, project: Project, version: str):
        pass


class MavenProjectVersionChanger(ProjectVersionChanger):

    def change(self, project: Project, version: str):
        if not version:
            raise ValueError("Version to change to cannot be empty")

        version_tag = self.get_version_tag(project)
        version_tag.text = version

    @abstractmethod
    def get_version_tag(self, project) -> ElementTree.SubElement:
        pass
