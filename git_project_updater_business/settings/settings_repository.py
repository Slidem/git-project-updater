import os
import json
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings import Settings

SETTINGS_JSON_PATH = "{baseFolder}/git_project_updater_business/settings/settings.json".format(
    baseFolder=os.environ["PYTHONPATH"])

settings_cache = None


def get_settings():
    """Returns the project updater settings as an `settings instance <settings.Settings>`.

     Returns None if no previous settings were set via `set_settings <settings_repository.set_settings>`"""

    global settings_cache

    if settings_cache:
        return settings_cache

    with open(SETTINGS_JSON_PATH) as json_file:
        try:
            settings = json.load(json_file)
            if not settings:
                return None

            settings_cache = create_settings_from_json(settings)
        except json.decoder.JSONDecodeError:
            return None

    return settings_cache


def set_settings(settings):
    global settings_cache

    if not settings:
        return

    if not isinstance(settings, Settings):
        raise ValueError("settings is not a Settings instance")

    settings_data = {
        "gitCredentials": {
            "username": settings.get_git_credentials().get_username(),
            "password": settings.get_git_credentials().get_password(),
        },
        "projectsType": settings.get_projects_type(),
        "projectsRootDirectories": settings.get_project_root_directories(),
    }

    with open(SETTINGS_JSON_PATH, "w") as json_file:
        json.dump(settings_data, json_file)

    settings_cache = settings


def create_settings_from_json(settings_json):
    # git credentials
    username = settings_json.get("gitCredentials").get("username")
    password = settings_json.get("gitCredentials").get("password")
    credentials = GitCredentials(username, password)

    # project settings
    projects_type = settings_json.get("projectsType")
    projects_root_directories = settings_json.get("projectsRootDirectories")

    return Settings(credentials, projects_root_directories, projects_type)
