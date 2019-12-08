from git_project_updater_business.repository.projects_repository import ProjectsRepository
import git_project_updater_business.models.git.git_model

from pygit2 import Repository
from pygit2 import GitError


class GitService:
    __instance = None

    @staticmethod
    def get_instance(projects_repository):
        if GitService.__instance is None:
            GitService(projects_repository)
        return GitService.__instance

    def __init__(self, projects_repository):
        if self.__instance is None:
            self.projects_repository = projects_repository
            GitService.__instance = self
        else:
            raise Exception("This class is a singleton")

    def get_git_info(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        if not project:
            raise ValueError(
                f"Could not find any project for project id {project_id}")

        repo = self.__get_repo(project)
        current_branch = repo.head.shorthand
        remote = repo.branches[current_branch].upstream_name

        print(f"Current branch: {current_branch}")
        print(f"Remote branch: {remote}")

        # TODO build git info
        return None

    def __get_repo(self, project):
        repo = None
        path = project.path.joinpath(".git")
        try_count = 0

        # try going 2 folders up
        while not repo and try_count < 2:
            try:
                repo = Repository(str(path))
            except GitError:
                try_count += 1
                path = path.parents[1].joinpath(".git")

        if not repo:
            raise ValueError("Could not find repo for ")

        return repo
