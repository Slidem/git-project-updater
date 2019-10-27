from git_project_updater_business.scanners.converter.project_processor_link import ProjectProcessorLink
from git_project_updater_business.models.project_dependency_tree_node import ProjectDependencyTreeNode


class MavenProjectDependencyTreeLink(ProjectProcessorLink):

    def process(self, projects):
        solved_memo = set()
        for project_id, project in projects.items():
            self.__solve_dependency_tree(projects, project, solved_memo)
        return projects

    def __solve_dependency_tree(self, projects, current_project, solved_projects_ids):
        maven_pom = current_project.maven_pom
        if not maven_pom:
            return

        id = current_project.project_id
        if id in solved_projects_ids:
            return

        # do the dfs
        stack = []
        stack.append(DependencyTreeNodeWrapper(
            id, self.__get_dependencies_to_solve(id, projects)))
        node_parents_dict = {}

        # keep memo while going through a chain of dependencies depth wise,
        # and check for circular dependencies
        depth_memo = set()

        while stack:
            # peek the stack
            node = stack[-1]

            if node.project_id in depth_memo:
                raise RuntimeError(
                    "Circular maven dependency found for artifact id " + node.project_id)

            depth_memo.add(node.project_id)

            if node.dependencies_solved():
                projects[node.project_id].dependency_tree = node.dependecy_node

                if node.project_id in node_parents_dict:
                    node_parents_dict[node.project_id].solve(node)

                solved_projects_ids.add(node.project_id)
                stack.pop()
                depth_memo.remove(node.project_id)
            else:
                # add dependencies to stack
                for dependency_id in node.dependencies_to_solve:
                    # add dependency to stack
                    dependency_node = DependencyTreeNodeWrapper(
                        dependency_id, self.__get_dependencies_to_solve(dependency_id, projects))
                    stack.append(dependency_node)
                    # save parent mapping
                    node_parents_dict[dependency_id] = node

    def __get_dependencies_to_solve(self, project_id, projects):

        dependencies_to_solve = set()

        project = projects[project_id]

        if project.maven_pom.is_parent():
            for child_id in project.children_ids:
                if child_id not in projects.keys():
                    continue
                dependencies_to_solve.update(
                    self.__get_child_pom_dependencies(child_id, project_id, projects))

        dependencies_to_solve.update(
            self.__get_pom_dependencies(project_id, projects))

        return list(filter(lambda d: d in projects.keys(), dependencies_to_solve))

    def __get_child_pom_dependencies(self, project_id, parent_id, projects):
        return list(filter(lambda pid: projects[pid].project_parent_id != parent_id, self.__get_pom_dependencies(project_id, parent_id)))

    def __get_pom_dependencies(self, project_id, projects):
        return list(projects[project_id].maven_pom.dependencies.keys())


class DependencyTreeNodeWrapper:

    def __init__(self, project_id, dependencies_to_solve):
        self.project_id = project_id
        self.dependecy_node = ProjectDependencyTreeNode(project_id, None)
        self.dependencies_to_solve = dependencies_to_solve

        if not dependencies_to_solve:
            dependencies_to_solve = []

    def dependencies_solved(self):
        return not self.dependecy_node or (set(self.dependecy_node.children_ids) == set(self.dependencies_to_solve))

    def solve(self, node):
        self.dependecy_node.add_child(node.dependecy_node)
