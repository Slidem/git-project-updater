from collections import namedtuple

Branch = namedtuple("Branch", "local remote")
GitFilesStatus = namedtuple("GitFilesStatus", "modified new deleted")
Commit = namedtuple("Commit", "hash message author_name author_email date")
GitInfo = namedtuple("GitInfo", "branch git_files_status last_commit")


def git_info_to_str(git_info):
    # todo build file status str
    modified_str = "      - modified"
    new_str = "      - new"
    deleted_str = "      - deleted"

    for m in git_info.git_files_status.modified:
        modified_str += f"\n               {m}"

    for n in git_info.git_files_status.new:
        new_str += f"\n               {n}"

    for d in git_info.git_files_status.deleted:
        deleted_str += f"\n               {d}"

    return f""" 
    Branch (current)
        - local : {git_info.branch.local}
        - remote : {git_info.branch.remote}

    Commit (last one):
        - hash : {git_info.last_commit.hash}
        - author name : {git_info.last_commit.author_name}
        - author email: {git_info.last_commit.author_email}
        - message : {git_info.last_commit.message.strip()}
        - date : {git_info.last_commit.date}
    
    File status:
    {modified_str}
    {new_str}
    {deleted_str}
    """
GIT_MERGE_ANALYSIS_FASTFORWARD