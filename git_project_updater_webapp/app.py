from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.repository.projects_repository import ProjectsRepository, ProjectScannerFactory
from git_project_updater_business.settings.settings_repository import SettingsRepository
from git_project_updater_business.utils.node_dependency_tree_traversal import NodeTraversalObserver, TraversalStrategyType, TraversalSate
from git_project_updater_webapp.exceptions import UpdaterWebappException
from git_project_updater_webapp.project_details_mapper import map_to_dict_details
from git_project_updater_business.service.git_service import GitService, GitProcessObserver
from git_project_updater_webapp.git_info_mapper import map_git_info_to_json

app = Flask(__name__)
cors = CORS(app)

project_scanner_factory = ProjectScannerFactory.instance()
settings_repository = SettingsRepository.instance()
projects_repository = ProjectsRepository.instance(
    settings_repository, project_scanner_factory)
projects_service = ProjectsService.instance(projects_repository)
git_service = GitService.get_instance(projects_repository)


@app.route("/projects", methods = ["GET"])
def projects():
    """
    Returns the a list of projects ids as a json collection
    """
    response = jsonify(projects_service.get_top_level_projects_ids())
    return response


@app.route("/projects/<project_id>/tree", methods = ["GET"])
def project_tree(project_id):
    project_dep_tree_node = get_project_from_repository(project_id).dependency_tree
    return build_dep_tree_json(project_dep_tree_node, None)



@app.route("/projects/<project_id>/info", methods = ["GET"])
def project_info(project_id):
    project = get_project_from_repository(project_id) 
    project_type = settings_repository.settings.projects_type
    git_info = git_service.get_git_info(project_id)
    return {
        "projectId":project_id,
        "projectType": project_type,
        "path":str(project.path),
        "version":project.version,
        "details":map_to_dict_details(project, project_type),
        "git":map_git_info_to_json(git_info)
    }


@app.route("/projects/<project_id>/git", methods = ["POST"])
def update_git_project(project_id):
    update_observer = UpdateGitProjectProcessObserver(project_id)
    git_service.update_git_sources(project_id, update_observer)
    return update_observer.response


#############################################################################################3

def get_project_from_repository(project_id):
    project = projects_repository.projects.get(project_id)
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


class UpdateGitProjectProcessObserver(GitProcessObserver):

    def __init__(self, project_id):
        self.__message = ""
        self.__project_id = project_id 
        self.__statuts = "success"

    def fetching(self):
        # do nothing
        pass
    
    def fetching_finished(self):
        # do nothing
        pass

    def up_to_date(self):
        self.__message = f"Updated {self.__project_id}: Project already up to date."

    def performed_fast_forward(self):
        self.__message = f"Updated {self.__project_id}: Performed fast forward"

    def could_not_update_current_branch(self, branch_name):
        self.__message = f"Could not update {self.__project_id}: Consider stashing your working directory and try again."
        self.__state = "failure" 

    @property
    def response():
        return {
            "message":self.__message,
            "status":self.__statuts
        }


if __name__ == '__main__':
    app.run()