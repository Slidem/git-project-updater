from git_project_updater_business.models.git.git_model import GitInfo
from flask import jsonify

def map_git_info_to_json(git_info: GitInfo):
    return {
        "branch":map_branch_info_to_json(git_info),
        "lastCommit":map_last_commit_to_json(git_info),
        "workingDir":map_working_dir_to_json(git_info) 
    }

def map_branch_info_to_json(git_info: GitInfo):

    branch = git_info.branch

    if not branch:
        return {}

    return {
        "local": branch.local,
        "remote": branch.remote
    }

def map_last_commit_to_json(git_info: GitInfo):
    last_commit = git_info.last_commit
    if not last_commit:
        return {}
    return {
        "date": last_commit.date,
        "authorName":last_commit.author_name,
        "authorEmail":last_commit.author_email,
        "message":last_commit.message
    }

def map_working_dir_to_json(git_info: GitInfo):
    git_file_status = git_info.git_files_status

    if not git_file_status:
        return {
            "newFiles": [],
            "modified": [],
            "deleted": [],    
        }

    return {
        "newFiles": set_to_array(git_file_status.new),
        "modified": set_to_array(git_file_status.modified),
        "deleted": set_to_array(git_file_status.deleted),
    }

def set_to_array(s):
    if not s:
        return []
    return [x for x in s]
