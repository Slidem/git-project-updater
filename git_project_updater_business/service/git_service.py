from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.models.git.git_model import *
from git_project_updater_business.utils.date_utils import millis_to_date

from pygit2 import Repository
from pygit2 import GitError
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_WT_NEW, GIT_STATUS_INDEX_MODIFIED, GIT_STATUS_WT_MODIFIED, GIT_STATUS_INDEX_DELETED, GIT_STATUS_WT_DELETED


class GitService:
    __instance = None

    new_file_flags = {GIT_STATUS_INDEX_NEW, GIT_STATUS_WT_NEW}
    modified_file_flags = {GIT_STATUS_INDEX_MODIFIED, GIT_STATUS_WT_MODIFIED}
    deleted_file_flags = {GIT_STATUS_INDEX_MODIFIED, GIT_STATUS_WT_DELETED}

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

        return GitInfo(
            self.__build_git_branch_status(repo),
            self.__build_git_files_status(repo),
            self.__build_git_last_commit_status(repo)
        )

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

    def __build_git_branch_status(self, repo):
        current_branch = repo.head.shorthand
        remote = repo.branches[current_branch].upstream_name
        return Branch(current_branch, remote)

    def __build_git_last_commit_status(self, repo):
        commit_id = repo.head.target
        last_commit = repo[commit_id]
        message = last_commit.message
        author = last_commit.author

        return Commit(
            str(commit_id),
            message,
            author.name,
            author.email,
            str(millis_to_date(last_commit.commit_time))
        )

    def __build_git_files_status(self, repo):
        modified = set()
        new = set()
        deleted = set()

        status = repo.status()

        for filepath, flags in status.items():
            if flags in GitService.new_file_flags:
                new.add(filepath)
            elif flags in GitService.modified_file_flags:
                modified.add(filepath)
            elif flags in GitService.deleted_file_flags:
                deleted.add(filepath)

        return GitFilesStatus(modified, new, deleted)
