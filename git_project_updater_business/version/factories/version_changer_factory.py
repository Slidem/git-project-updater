from git_project_updater_business.version.models.version import ChildVersionType
from git_project_updater_business.version.factories.maven_version_changer import MavenVersionChanger, ProjectMavenVersionChangerXmlPathFinder, ParentMavenVersionChangerXmlPathFinder, DependencyArtifactXmlFinder, DependencyManagementArtifactXmlFinder, PropertiesArtifactXmlFinder
from git_project_updater_business.repository.projects_repository import ProjectsRepository, SettingsRepository, ProjectScannerFactory
from git_project_updater_business.errors.updater_errors import VersionChangerError


def create_maven_changer(project, project_to_change_in):
    version_used = project_to_change_in.dependency_tree.get_child_version(
        project.project_id)

    if project.project_type == "maven":
        return get_for_maven(project, version_used)
    
    raise VersionChangerError(f"project type {project.project_type} not supported yet")


def get_for_maven(project, version_used):
    pr = ProjectsRepository.get_instance(
        SettingsRepository.get_instance(), ProjectScannerFactory.instance())
    
    version_type = version_used.version_type 

    if version_type == ChildVersionType.ARTIFACT_VERSION:
        return MavenVersionChanger(project, ProjectMavenVersionChangerXmlPathFinder(pr), DependencyArtifactXmlFinder())

    elif version_type == ChildVersionType.DEPENDENCY_MANAGEMENT_ARTIFACT_VERSION:
        return MavenVersionChanger(project, ProjectMavenVersionChangerXmlPathFinder(pr), DependencyManagementArtifactXmlFinder())

    elif version_type == ChildVersionType.PROJECT_PROPERTY_VERSION:
        return MavenVersionChanger(project, ProjectMavenVersionChangerXmlPathFinder(pr), PropertiesArtifactXmlFinder())

    elif version_type == ChildVersionType.PARENT_DEPENDECY_MANAGEMENT_ARTIFACT_VERSION:
        return MavenVersionChanger(project, ParentMavenVersionChangerXmlPathFinder(pr), DependencyManagementArtifactXmlFinder())

    elif version_type == ChildVersionType.PARENT_PROJECT_PROPERTY_VERSION:
        return MavenVersionChanger(project, ParentMavenVersionChangerXmlPathFinder(pr), PropertiesArtifactXmlFinder())
    
    else:
        raise VersionChangerError(f"No version changer found for version type {version_type}") 
