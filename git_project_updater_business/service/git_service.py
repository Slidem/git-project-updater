from abc import ABC, abstractmethod

from git_project_updater_business.repository.projects_repository import ProjectsRepository
from git_project_updater_business.models.git.git_model import *
from git_project_updater_business.utils.date_utils import millis_to_date
from git_project_updater_business.errors.git_errors import GitError 


from pygit2 import Repository
from pygit2 import GitError
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_WT_NEW, GIT_STATUS_INDEX_MODIFIED, GIT_STATUS_WT_MODIFIED, GIT_STATUS_INDEX_DELETED, GIT_STATUS_WT_DELETED
from pygit2 import GIT_MERGE_ANALYSIS_UP_TO_DATE
from pygit2 import GIT_MERGE_ANALYSIS_FASTFORWARD


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
        """
        Retrives a project's git info project based on the project_id

        Parameters
        ----------
        
        project_id : str
            The project id to retrieve the info

        Returns
        -------
            GitInfo instance containing the git info for the given project id

        Raises
        ------
            ValueError if no project found for the given project_id  
            GitError if no git repo found for the given project_id
        """
        project = self.__try_get_project(project_id)

        repo = self.__get_repo(project)

        return GitInfo(
            self.__build_git_branch_status(repo),
            self.__build_git_files_status(repo),
            self.__build_git_last_commit_status(repo)
        )

    def update_git_sources(self, project_id, git_process_observer):
        """
        Updates a project's git sources based on the project_id

        Parameters
        ----------
        
        project_id : str
            The project id to be updated

        git_process_observer : GitProcessObserver
            Instance of GitProcessObserver implementation, that listens to events
            during the update process

        Returns
        -------
            GitInfo instance containing the git info for the given project id

        Raises
        ------
            ValueError if no project found for the given project_id  
            GitError if no git repo found for the given project_id
        """

        project = self.__try_get_project(project_id)
        repo = self.__get_repo(project)

        remote = repo.remotes["origin"]

        # first fetch remotes for current branch
        git_process_observer.fetching()
        remote.fetch()
        git_process_observer.fetching_finished()

        # perform merge analasys (what would happen if merging current remote into local branch)
        current_branch_name = repo.head.shorthand
        remote_id = repo.lookup_reference(
            f'refs/remotes/{remote.name}/{current_branch_name}').target
        merge_result, _ = repo.merge_analysis(remote_id)

        # analyze merge result
        if merge_result & GIT_MERGE_ANALYSIS_UP_TO_DATE:
            # nothing to do, already up to date
            git_process_observer.up_to_date()
            return
        elif merge_result & GIT_MERGE_ANALYSIS_FASTFORWARD:
            repo.checkout_tree(repo.get(remote_id))
            try:
                master_ref = repo.lookup_reference(f'refs/heads/{current_branch_name}')
                master_ref.set_target(remote_id)
            except KeyError:
                repo.create_branch(current_branch_name, repo.get(remote_id))
            repo.head.set_target(remote_id)
            git_process_observer.performed_fast_forward()
        else:
            git_process_observer.could_not_update_current_branch(current_branch_name)

    def __try_get_project(self, project_id):
        project = self.projects_repository.projects.get(project_id, None)
        if not project:
            raise ValueError(
                f"Could not find any project for project id {project_id}")
        return project

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
            raise GitError(f"Could not find repo for project_id {project.project_id}")

        return repo

    def __build_git_branch_status(self, repo):
        local_branch = repo.head.shorthand
        remote = repo.branches[local_branch].upstream_name
        return Branch(local_branch, remote)

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

class GitProcessObserver(ABC):

    @abstractmethod
    def fetching(self):
        pass
    
    @abstractmethod
    def fetching_finished(self):
        pass

    @abstractmethod
    def up_to_date(self):
        pass

    @abstractmethod
    def performed_fast_forward(self):
        pass

    @abstractmethod
    def could_not_update_current_branch(self, branch_name):
        pass
