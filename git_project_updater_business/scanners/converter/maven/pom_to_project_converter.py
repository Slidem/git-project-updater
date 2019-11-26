import xmltodict

from git_project_updater_business.models.maven.maven_pom import MavenPom, MavenArtifact
from git_project_updater_business.models.maven.maven_project import MavenProject
from git_project_updater_business.scanners.converter.maven.maven_processor_chain_factory import \
    MavenProjectProcessorChainFactory


class PomToProjectConverter:

    def __init__(self):
        self.projects = {}

    def collect_and_convert(self, pom_path, pom_xml_content):
        """ Converts the pom_xml_content into a project
            This method does not return anything. To retrieve your converted
            project, call the compute_projects method.

            Args:pom_xml_content (TextIOWrapper) : pom content
        """

        # This method only gets the xml content and converts it
        # into a minimal MavenProject instance, and adds it into self.projects
        maven_pom = self.__build_maven_pom(pom_xml_content)
        project = self.__create_project_from_maven_pom(maven_pom, pom_path)
        self.projects[project.project_id] = project

    def compute_collected_projects(self):
        # before returning the projects
        # run each project through a chain of maven project processors
        # that will add additional data to the already existing projects
        # this is done now, as the processors now have access to all computed projects;
        return MavenProjectProcessorChainFactory().create_chain(self.projects).process_projects()

    #################################################################################
    # ---------------------------- PRIVATE METHODS ----------------------------------
    #################################################################################

    def __build_maven_pom(self, pom_xml):
        pom_dict = xmltodict.parse(pom_xml.read())["project"]
        artifact = self.__parse_artifact(pom_dict)
        parent_artifact = self.__parse_artifact(pom_dict.get("parent", None))
        modules = self.__get_modules(pom_dict)

        dependencies = self.__get_dependencies(
            pom_dict.get("dependencies", None))

        dependencies_management = {}
        dependencies_management_node = pom_dict.get(
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

    def __create_project_from_maven_pom(self, maven_pom, pom_path):
        project_id = maven_pom.artifact.artifact_id
        project_parent_id = maven_pom.parent_artifact.artifact_id if maven_pom.parent_artifact else None
        project_type = "maven"
        return MavenProject(
            maven_pom=maven_pom,
            project_id=project_id,
            project_parent_id=project_parent_id,
            project_type=project_type,
            path=pom_path
        )
