from git_project_updater_business.builders.maven_builder import MavenBuilder
from git_project_updater_business.models.project import Project

maven_builder = MavenBuilder() 

def get_builder(project: Project):
    if not project:
        raise ValueError("Cannot pass an empty project")

    project_type = project.project_type

    if project_type.strip().lower() == "maven":
        return maven_builder
    
    raise ValueError(f"No valid project builder found for project type {project_type}")


        
    
