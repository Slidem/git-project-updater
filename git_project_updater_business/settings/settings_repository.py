import os
import json
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings import Settings

SETTINGS_JSON_PATH = "{baseFolder}/git_project_updater_business/settings/settings.json".format(
    baseFolder=os.environ["PYTHONPATH"]
)

GIT_CREDENTIALS_JSON_KEY = "gitCredentials"
GIT_CREDENTIALS_USERNAME_JSON_KEY = "username"
GIT_CREDENTIALS_PASSWORD_JSON_KEY = "password"
PROJECTS_TYPE_JSON_KEY = "projectsType"
PROJECTS_ROOT_DIRECTORIES_JSON_KEY = "projectsRootDirectories"


class SettingsRepository:

    __instance = None
    __settings_cache = None

    @staticmethod
    def get_instance():
        if SettingsRepository.__instance is None:
            SettingsRepository()
        return SettingsRepository.__instance

    def __init__(self):
        if SettingsRepository.__instance is None:
            SettingsRepository.__instance = self
        else:
            raise Exception("This class is a singleton")

    def get_settings(self):
        """Returns the project updater settings as an `settings instance <settings.Settings>`.

        Returns None if no previous settings were set via `set_settings <settings_repository.set_settings>`"""

        if SettingsRepository.__settings_cache:
            return SettingsRepository.__settings_cache

        with open(SETTINGS_JSON_PATH) as json_file:
            try:
                settings = json.load(json_file)
                if not settings:
                    return None

                SettingsRepository.__settings_cache = self.__create_settings_from_json(
                    settings)
            except json.decoder.JSONDecodeError:
                return None

        return SettingsRepository.__settings_cache

    def set_settings(self, settings):
        if not settings:
            return

        if not isinstance(settings, Settings):
            raise ValueError("settings is not a Settings instance")

        with open(SETTINGS_JSON_PATH, "w") as json_file:
            settings_data = {
                GIT_CREDENTIALS_JSON_KEY: {
                    GIT_CREDENTIALS_USERNAME_JSON_KEY: settings.git_credentials.username,
                    GIT_CREDENTIALS_PASSWORD_JSON_KEY: settings.git_credentials.password,
                },
                PROJECTS_TYPE_JSON_KEY: settings.projects_type,
                PROJECTS_ROOT_DIRECTORIES_JSON_KEY: settings.projects_root_directory,
            }
            json.dump(settings_data, json_file)

        SettingsRepository.__settings_cache = settings

    def __create_settings_from_json(self, settings_json):
        # git credentials
        username = settings_json.get(GIT_CREDENTIALS_JSON_KEY).get(
            GIT_CREDENTIALS_USERNAME_JSON_KEY)

        password = settings_json.get(GIT_CREDENTIALS_JSON_KEY).get(
            GIT_CREDENTIALS_PASSWORD_JSON_KEY)

        credentials = GitCredentials(username, password)

        # project settings
        projects_type = settings_json.get(PROJECTS_TYPE_JSON_KEY)
        projects_root_directories = settings_json.get(
            PROJECTS_ROOT_DIRECTORIES_JSON_KEY)

        return Settings(credentials, projects_root_directories, projects_type)
