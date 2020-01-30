from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.repository.projects_repository import ProjectsRepository, ProjectScannerFactory
from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.utils.node_dependency_tree_traversal import NodeTraversalObserver, TraversalStrategyType, TraversalSate
from git_project_updater_webapp.exceptions import UpdaterWebappException
from git_project_updater_webapp.project_details_mapper import map_to_dict_details

app = Flask(__name__)
cors = CORS(app)

project_scanner_factory = ProjectScannerFactory.instance()
settings_repository = SettingsRepository.instance()
projects_repository = ProjectsRepository.instance(
    settings_repository, project_scanner_factory)
projects_service = ProjectsService.instance(projects_repository)


@app.route("/projects")
def projects():
    """
    Returns the a list of projects ids as a json collection
    """
    response = jsonify(projects_service.get_top_level_projects_ids())
    return response


@app.route("/projects/<project_id>/tree")
def project_tree(project_id):
    project_dep_tree_node = get_project_from_repository(project_id).dependency_tree
    return build_dep_tree_json(project_dep_tree_node, None)



@app.route("/projects/<project_id>/info")
def project_info(project_id):
    project = get_project_from_repository(project_id) 
    project_type = settings_repository.settings.projects_type
    return {
        "projectId":project_id,
        "projectType": project_type,
        "path":str(project.path),
        "version":project.version,
        "details":map_to_dict_details(project, project_type) 
    }

def get_project_from_repository(project_id):
    project = projects_repository.projects.get(project_id)

    if not project:
        raise UpdaterWebappException("Project not found for id: " + project_id)

    return project
 
def build_dep_tree_json(dependecy_tree_node, parent_project_id):
    json = {}
    project_id = dependecy_tree_node.project_id
    json["projectId"] = project_id
    json["version"] = str(projects_service.get_project_version(project_id))

    if parent_project_id:
        json["versionUsed"] = str(
            projects_service.get_version_used(project_id, parent_project_id))

    if dependecy_tree_node.children:
        dependencies = [build_dep_tree_json(
            n, project_id) for n in dependecy_tree_node.children]
        json["dependencies"] = dependencies

    return json


if __name__ == '__main__':
    app.run()
