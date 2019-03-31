import os
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings import Settings

settings_cache = None


def get_settings():
    """Returns the project updater settings as an `settings instance <settings.Settings>`.

     Returns None if no previous settings were set via `set_settings <settings_repository.set_settings>`"""

    global settings_cache

    if settings_cache:
        return settings_cache

    git_credentials = get_git_credentials_from_en()
    project_root_directories = os.environ.get(
        "PROJECT_UPDATER_ROOT_DIRECTORIES")
    project_type = os.environ.get("PROJECT_UPDATER_TYPE")

    if not (git_credentials and project_root_directories and project_type):
        return None

    settings_cache = Settings(
        git_credentials, project_root_directories, project_type)

    return settings_cache


def set_settings(settings):
    global settings_cache

    if not settings:
        return

    if not isinstance(settings, Settings):
        raise ValueError("settings is not a Settings instance")

    os.environ["PROJECT_UPDATER_GIT_USERNAME"] = settings.get_git_credentials(
    ).get_username()
    os.environ["PROJECT_UPDATER_GIT_USERNAME"] = settings.get_git_credentials(
    ).get_password()
    os.environ["PROJECT_UPDATER_ROOT_DIRECTORIES"] = settings.get_project_root_directories()
    os.environ["PROJECT_UPDATER_TYPE"] = settings.get_project_type()

    settings_cache = settings


def get_git_credentials_from_en():
    username = os.environ.get("PROJECT_UPDATER_GIT_USERNAME")
    password = os.environ.get("PROJECT_UPDATER_GIT_PASSWORD")

    if not username or not password:
        return None

    return GitCredentials(username, password)
