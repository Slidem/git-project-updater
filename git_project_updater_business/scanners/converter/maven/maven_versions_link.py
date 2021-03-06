from git_project_updater_business.scanners.converter.project_processor_link import ProjectProcessorLink
from git_project_updater_business.version.models.version import ChildVersion, MavenChildVersion, ChildVersionType
from git_project_updater_business.errors.maven_errors import MavenError
from abc import ABC, abstractmethod
import re


class MavenProjectVersionsProcessorLink(ProjectProcessorLink):

    property_regex = "\${(.+)}"

    def process(self, projects):
        for project_id, project in projects.items():
            self.__set_project_version(project, projects)
            self.__set_children_version(project, projects)
        return projects

    def __set_project_version(self, project, projects):

        if project.version.upper() != "UNKOWN":
            # skip it, already done
            print("Project version already set")
            return

        project.version = project.maven_pom.artifact.version
        if project.version == "UNKOWN":
            # search in parent maybe
            parent_project = projects.get(project.project_parent_id, None)
            if parent_project:
                project.version = parent_project.maven_pom.artifact.version

        if project.version == "UNKOWN":
            raise ValueError(
                f"A project cannot have an unknown version. Check your maven pom for project id : {project.project_id}")

    def __set_children_version(self, project, projects):

        for child in project.dependency_tree.children:

            child_version = self.__try_to_resolve_child_version(
                child, project, projects)

            if not child_version:
                raise ValueError(
                    f"No version specified for child : {child.project_id} in project {project.project_id}")

            # set in project
            project.dependency_tree.set_child_version(
                child.project_id, child_version)

            # set in parent also
            parent_project = projects.get(project.project_parent_id, None)
            if parent_project:
                parent_project.dependency_tree.set_child_version(
                    child.project_id, child_version)

    def __try_to_resolve_child_version(self, child, project, projects):
        parent = projects.get(project.project_parent_id, None)

        property_placeholder_resolvers = [
            ProjectVersionPlaceholderResolver(project, parent),
            ParentProjectVersionPlaceholderResolver(project, parent),
            ProjectPropertiesPlaceholderResolver(project, parent),
            ParentPropertiesPlaceholderResolver(project, parent)
        ]

        version_resolvers = [
            ArtifactVersionResolver(
                child, project, parent, property_placeholder_resolvers),
            DependencyManagementVersionResolver(
                child, project, parent, property_placeholder_resolvers),
            ParentDependencyManagementVersionResolver(
                child, project, parent, property_placeholder_resolvers)
        ]

        child_version = None

        for r in version_resolvers:
            child_version = r.resolve()
            if child_version:
                break

        return child_version


# Version resolvers --------------------------------------------------------------------
# --------------------------------------------------------------------------------------

class VersionResolver(ABC):

    def __init__(self, child, project, parent_project, property_placeholder_resolvers):
        self.child = child
        self.project = project
        self.parent_project = parent_project
        self.property_placeholder_resolvers = property_placeholder_resolvers

    def resolve(self) -> ChildVersion:
        child_version = self.resolve_child_version()

        if not child_version:
            return None

        if is_version_property(child_version.value):
            property_name = version_property_match(
                child_version.value).group(1)

            for r in self.property_placeholder_resolvers:
                if r.accept(property_name):
                    return r.resolve(property_name)

            raise MavenError(
                f"Could nor resolve version property \"{property_name}\" for project id {self.project.project_id}")

        return child_version

    @abstractmethod
    def resolve_child_version(self) -> ChildVersion:
        pass


class ArtifactVersionResolver(VersionResolver):

    def resolve_child_version(self):
        child_artifact = self.project.maven_pom.dependencies.get(
            self.child.project_id, None)

        if not child_artifact or not child_artifact.version:
            return None

        return ChildVersion(child_artifact.version, ChildVersionType.ARTIFACT_VERSION)


class DependencyManagementVersionResolver(VersionResolver):

    def resolve_child_version(self):

        child_artifact_dm = self.project.maven_pom.dependencies_management.get(
            self.child.project_id, None)

        if not child_artifact_dm or not child_artifact_dm.version:
            return None

        return ChildVersion(child_artifact_dm.version,
                            ChildVersionType.ARTIFACT_VERSION)


class ParentDependencyManagementVersionResolver(VersionResolver):

    def resolve_child_version(self):
        if not self.parent_project:
            return None

        parent_child_artifact_dm = self.parent_project.maven_pom.dependencies_management.get(
            self.child.project_id, None)

        if not parent_child_artifact_dm or not parent_child_artifact_dm.version:
            return None

        return ChildVersion(parent_child_artifact_dm.version,
                            ChildVersionType.PARENT_DEPENDECY_MANAGEMENT_ARTIFACT_VERSION)

# Property placeholder resolvers--------------------------------------------------------
# --------------------------------------------------------------------------------------


class PropertyPlaceholderResolver(ABC):

    def __init__(self, project, parent_project):
        self.project = project
        self.parent_project = parent_project

    @abstractmethod
    def accept(self, property_name) -> bool:
        pass

    @abstractmethod
    def resolve(self, property_name) -> ChildVersion:
        pass


class ProjectPropertiesPlaceholderResolver(PropertyPlaceholderResolver):

    def accept(self, property_name):
        return self.project.maven_pom.properties.get(property_name, None) != None

    def resolve(self, property_name):
        return MavenChildVersion(self.project.maven_pom.properties[property_name], ChildVersionType.PROJECT_PROPERTY_VERSION, property_name)


class ParentPropertiesPlaceholderResolver(PropertyPlaceholderResolver):

    def accept(self, property_name):
        return self.parent_project and self.parent_project.maven_pom.properties.get(property_name, None) != None

    def resolve(self, property_name):
        return MavenChildVersion(self.parent_project.maven_pom.properties[property_name], ChildVersionType.PARENT_PROJECT_PROPERTY_VERSION, property_name)


class ProjectVersionPlaceholderResolver(PropertyPlaceholderResolver):

    def accept(self, property_name):
        return property_name == "project.version" and self.project.version

    def resolve(self, property_name):
        return ChildVersion(self.project.version, ChildVersionType.PROJECT_VERSION)


class ParentProjectVersionPlaceholderResolver(PropertyPlaceholderResolver):

    def accept(self, property_name):
        return self.parent_project and property_name == "project.version" and not self.project.version and self.parent_project.version

    def resolve(self, property_name):
        return ChildVersion(self.parent_project.version, ChildVersionType.PARENT_PROJECT_VERSION)

# --------------------------------------------------------------------------------------


def is_version_property(child_version):
    return bool(version_property_match(child_version))


def version_property_match(version):
    """
    Returns a Match object if str matches the property_regex
    """
    if not version:
        return None

    return re.match(MavenProjectVersionsProcessorLink.property_regex, version)
