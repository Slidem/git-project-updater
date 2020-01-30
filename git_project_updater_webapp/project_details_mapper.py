def map_to_dict_details(project, project_type):
    if project_type == "maven":
        return map_maven_details(project)
    
    raise ValueError("Unknown project type " + project_type)

def map_maven_details(project):
    maven_pom = project.maven_pom
    artifact = maven_pom.artifact
    return {
        "artifactId":artifact.artifact_id,
        "groupId":artifact.group_id,
        "scope":artifact.scope,
        "packaging":artifact.packaging
    } 