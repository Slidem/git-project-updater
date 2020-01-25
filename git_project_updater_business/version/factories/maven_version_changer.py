from git_project_updater_business.version.factories.version_changer import VersionChanger
from abc import ABC, abstractmethod
from git_project_updater_business.errors.maven_errors import MavenError
import xml.etree.ElementTree as ET


class MavenVersionChanger(VersionChanger):

    def __init__(self, project, xml_path_finder, node_finder):
        super().__init__(project)
        self.xml_path_finder = xml_path_finder
        self.node_finder = node_finder

    def change_in(self, project_to_change_in, with_version):
        ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
        path = self.xml_path_finder.get_xml_path(project_to_change_in)
        child_version = project_to_change_in.dependency_tree.get_child_version(
            self.project.project_id)

        xml_tree = ET.parse(str(path))
        version_node = self.node_finder.get_node(
            xml_tree, self.project.project_id, child_version)

        version_node.text = with_version
        xml_tree.write(path)

class MavenVersionChangerXmlPathFinder(ABC):

    def __init__(self, projects_repository):
        self.projects_repository = projects_repository

    @abstractmethod
    def get_xml_path(self, project):
        pass


class ProjectMavenVersionChangerXmlPathFinder(MavenVersionChangerXmlPathFinder):

    def get_xml_path(self, project):
        return str(project.path.joinpath("pom.xml"))


class ParentMavenVersionChangerXmlPathFinder(MavenVersionChangerXmlPathFinder):

    def get_xml_path(self, project):
        parent = self.projects_repository.projects.get(
            project.project_parent_id, None)

        pj = parent

        if not pj:
            pj = project

        if not pj:
            raise MavenError(
                f"Could not get pom path for project_id {project.project_id}")

        return str(pj.path.joinpath("pom.xml"))


class MavenVersionChangerXmlElementFinder(ABC):

    @abstractmethod
    def get_node(self, xml_tree, child_project_id, child_version):
        pass


class DependencyArtifactXmlFinder(MavenVersionChangerXmlElementFinder):

    def get_node(self, xml_tree, child_project_id, child_version):

        root = xml_tree.getroot()
        dependencies = find(root, "dependencies")

        for d in find_all(dependencies, "dependency"):
            artifact_id = find(d, "artifactId")
            if artifact_id == child_project_id:
                return find(d, "version")

        raise MavenError(
            f"No dependency found for child_id {child_project_id}")


class DependencyManagementArtifactXmlFinder(MavenVersionChangerXmlElementFinder):

    def get_node(self, xml_tree, child_project_id, child_version):
        root = xml_tree.getroot()

        dependencies_management = find(root, "dependencies")

        for d in find_all(dependencies_management, "dependency"):
            artifact_id = find(d, "artifactId")
            if artifact_id == child_project_id:
                return find(d, "version")

        raise MavenError(
            f"No dependency_management found for child_id {child_project_id}")


class PropertiesArtifactXmlFinder(MavenVersionChangerXmlElementFinder):

    def get_node(self, xml_tree, child_project_id, child_version):
        root = xml_tree.getroot()
        properties = find(root, "properties")
        return find(properties, child_version.property_tag_value)


# ElementTree is dumb, and you have to specify the namespace in order to find your specific tag
ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}


def find(node, tag):
    return node.find(f"mvn:{tag}", ns)


def find_all(node, tag):
    return node.findall(f"mvn:{tag}", ns)
