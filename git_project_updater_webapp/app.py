from flask import Flask, jsonify
from git_project_updater_business.service.projects_service import ProjectsService
from git_project_updater_business.repository.projects_repository import ProjectsRepository, ProjectScannerFactory
from git_project_updater_business.settings.settings_repository import SettingsRepository 
from git_project_updater_business.utils.node_dependency_tree_traversal import NodeTraversalObserver, TraversalStrategyType, TraversalSate

app = Flask(__name__) 

project_scanner_factory = ProjectScannerFactory.instance()
settings_repository = SettingsRepository.instance() 
projects_repository = ProjectsRepository.instance(settings_repository, project_scanner_factory)
projects_service = ProjectsService.instance(projects_repository)

@app.route("/projects")
def projects():
    """
    Returns the a list of projects ids as a json collection
    """
    response = jsonify(projects_service.get_top_level_projects_ids())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 


@app.route("/projects/<project_id>/tree")
def project_tree(project_id):
    obs = JsonDependencyTreeTraversal()
    projects_service.traverse_project_dependency_tree(
            project_id,
            TraversalStrategyType.BFS,
            ProjectDependencyTreeCommand.level_based_printer
        )
    

class JsonDependencyTreeTraversal(NodeTraversalObserver):

    def __init__(self):
        super().__init__()
        self.dependency_tree = {}
        self.current_level = 1
        self.parent_children = []
    
    def node_visited(self, traversal_state):
        project_id = traversal_state.node.project_id
        project_info = projects_service.get_project_details(traversal_state.project_id)
        if traversal_state.level:
            self.dependency_tree["projectId"] = traversal_state.project_id
            self.dependency_tree[""]
            
            
        return super().node_visited(traversal_state)

    


if __name__ == '__main__':
    app.run()
