from git_project_updater_business.scanners.converter.project_processor_link import ProjectProcessorLink
import re


class MavenProjectVersionsProcessorLink(ProjectProcessorLink):

    property_regex = "\${(.+)}"

    def process(self, projects):

        for project_id, project in projects.items():
            self.__set_project_version(project, projects)
            self.__set_children_version(project, projects)

    def __set_project_version(self, project, projects):
        if project.version.upper() != "UNKOWN":
            # skip it, already done
            print("Project version already set")
            return

        project.version = project.maven_pom.artifact.version
        if project.version == "UNKOWN":
            # search in parent maybe
            parent_project = projects.get(project.parent_id, None)
            if parent_project:
                project.version = parent_project.maven_pom.artifact.version

        if project.version == "UNKOWN":
            raise ValueError(
                f"A project cannot have an unknown version. Check your maven pom for project id : {project.project_id}")

    def __set_children_version(self, project, projects):

        # Look in tree
        # For each children, see artifact in dependency_management and try extract version from there
        # If not in dependency management, try and extract it from actual dependencies
        # if not throw exception
        for child in project.children:
            child_version = None

            child_artifact = project.maven_pom.dependencies.get(
                child.project_id, None)

            if child_artifact:
                child_version = child_artifact.version

            if not child_version:
                child_artifact_dm = project.maven_pom.dependency_management.get(
                    child.project_id, None)

                if child_artifact_dm:
                    child_version = child_artifact.version

            if not child_version:
                parent_project = projects.get(project.parent_id, None)
                if parent_project:
                    child_artifact_dm = project.maven_pom.dependency_management.get(
                        child.project_id, None)
                    if child_artifact_dm:
                        child_version = child_artifact.version

            if self.__is_version_property(child_version):
                # method should raise exception if version property could not be found
                child_version = self.__extract_from_property(
                    child_version, project, projects)

            if not child_version:
                raise ValueError("No version specified")

            project.set_child_version(child.project_id, child_version)

    def __is_version_property(self, child_version):
        return bool(self.__version_property_match(child_version))

    def __extract_from_property(self, child_version, project, projects):
        version_property = self.__version_property_match(
            child_version).group(1)

        version_property_value = None
        # try getting from project properties
        version_property_value = project.maven_pom.properties.get(
            version_property, None)

        # try getting from parent project properties
        if not version_property_value:
            parent = projects.get(project.parent_id, None)
            if parent:
                version_property_value = parent.maven_pom.properties.get(
                    version_property, None)

        if not version_property_value:
            raise ValueError(f"Could not find version property value ({version_property}) in project {project.project_id}")
            
        return version_property_value
        

    def __version_property_match(self, str):
        """
        Returns a Match object if str matches the property_regex
        """
        return re.match(re.match(MavenProjectVersionsProcessorLink.property_regex, child_version))
