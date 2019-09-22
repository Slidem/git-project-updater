class ProjectDependencyTreeNode:

    def __init__(self, project_id, children):
        self.project_id = project_id
        self.children = children if children else []

    def add_child(self, project_id):
        self.children.append(ProjectDependencyTreeNode(project_id, None))