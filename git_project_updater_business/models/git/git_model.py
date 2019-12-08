from collections import namedtuple

Branch = namedtuple("Branch", "local remote")
GitFilesStatus = ("GitFilesStatus", "modified new deleted")
Commit = ("Commit", "hash message")
GitInfo = ("GitInfo", "branch git_files_status last_commit")


def git_info_to_str(git_info):
    files_status = None

    return """ 
    Branch (current)
        - local :
        - remote :

    Commit (last one):
        - hash : 
        - message :
    """
