from git_project_updater_business.scanners.converter.maven.maven_children_link import MavenProjectChildrenLink
from git_project_updater_business.scanners.converter.maven.maven_dependency_tree_link import MavenProjectDependencyTreeLink
from git_project_updater_business.scanners.converter.project_processor_link_chain import ProjectProcessorLinkChain


class MavenProjectProcessorChainFactory:

    def create_chain(self, projects):
        root = MavenProjectChildrenLink()
        root.add_next(MavenProjectDependencyTreeLink())
        return ProjectProcessorLinkChain(root, projects)
