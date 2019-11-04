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
        stack.append(self.__build_node_wrapper(
            id, projects, solved_projects_ids))

        node_parents_dict = {}

        # keep memo while going through a chain of dependencies depth wise,
        # and check for circular dependencies
        depth_memo = set()
        depth_memo.add(id)

        while stack:
            # peek the stack
            node = stack[-1]

            if node.dependencies_solved():
                projects[node.project_id].dependency_tree = node.dependecy_node

                if node.project_id in node_parents_dict:
                    node_parents_dict[node.project_id].solve(node)

                solved_projects_ids.add(node.project_id)
                stack.pop()
                depth_memo.remove(node.project_id)
                continue

            # add dependencies to stack
            for dependency_id in node.dependencies_to_solve:
                # add dependency to stack
                dependency_node = self.__build_node_wrapper(
                    dependency_id, projects, solved_projects_ids)

                stack.append(dependency_node)

                # detect circular dependency
                self.__check_for_circular_dependency(dependency_id, depth_memo)
                depth_memo.add(dependency_id)

                # save parent mapping
                node_parents_dict[dependency_id] = node

    def __build_node_wrapper(self, id, projects, resolved_projects):
        dependency_node = None
        if id in resolved_projects:
            dependency_node = projects[id].dependency_tree
        dependencies_to_solve = self.__get_dependencies_to_solve(id, projects)
        return DependencyTreeNodeWrapper(id, dependencies_to_solve, dependency_node)

    def __get_dependencies_to_solve(self, project_id, projects):

        dependencies_to_solve = set()

        project = projects[project_id]

        if project.maven_pom.is_parent():
            for child_id in project.children_ids:
                if child_id in projects.keys():
                    child_dependencies = self.__get_pom_dependencies(
                        child_id, projects)
                    dependencies_to_solve.update(child_dependencies)

        dependencies_to_solve.update(
            self.__get_pom_dependencies(project_id, projects))

        return dependencies_to_solve

    def __get_pom_dependencies(self, project_id, projects):
        if project_id not in projects.keys():
            return []

        project_parent_id = projects[project_id].project_parent_id

        def is_local_project_filter(pid): return pid in projects.keys()

        def does_not_have_the_same_parent(pid):
            return not project_parent_id or (project_parent_id in projects.keys() and projects[pid].project_parent_id != project_parent_id)

        filters = (is_local_project_filter, does_not_have_the_same_parent)

        return list(filter(lambda pid: all(f(pid) for f in filters), projects[project_id].maven_pom.dependencies.keys()))

    def __check_for_circular_dependency(self, id, depth_memo):
        if id in depth_memo:
            raise RuntimeError(
                "Circular maven dependency found for artifact id " + id)


class DependencyTreeNodeWrapper:

    def __init__(self, project_id, dependencies_to_solve, dependecy_node):
        self.project_id = project_id
        self.dependecy_node = dependecy_node if dependecy_node else ProjectDependencyTreeNode(
            project_id, None)
        self.dependencies_to_solve = dependencies_to_solve

        if not dependencies_to_solve:
            dependencies_to_solve = []

    def dependencies_solved(self):
        return set(self.dependecy_node.children_ids) == set(self.dependencies_to_solve)

    def solve(self, node):
        self.dependecy_node.add_child(node.dependecy_node)
