from git_project_updater_business.scanners.converter.project_processor_link import ProjectProcessorLink


class MavenProjectDependencyTreeLink(ProjectProcessorLink):

    def process(self, projects):

        return projects

    def __get_dependency_tree(self, projects, current_project):
        dependencies = self.__compute_project_dependencies(current_project)
        

    def __compute_project_dependencies(self, projects, project):
        maven_pom = project.maven_pom

        if not maven_pom:
            return

        mvn_artifact = maven_pom.artifact

        if mvn_artifact.packaging == "pom":
            return [d for d in m_id for self.__get_project_dependencies(projects, m_id) in maven_pom.modules]
        else:
            return self.__get_project_dependencies(projects, project.project_id)

    def __get_project_dependencies(self, projects, project_id):
        all_dependencies = projects[project_id].maven_pom.dependencies
        return map(lambda artifact: projects[artifact.artifact_id], filter(lambda d: d.artifact_id in projects, all_dependencies))
    
