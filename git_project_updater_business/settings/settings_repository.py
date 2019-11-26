import os
import json
from collections import namedtuple
from git_project_updater_business.settings.git_credentials import GitCredentials
from git_project_updater_business.settings.settings import Settings

SETTINGS_JSON_PATH = "{baseFolder}/settings.json".format(
    baseFolder=os.path.dirname(os.path.realpath(__file__))
)

GitJsonKeys = namedtuple(
    'GitJsonKeys',
    'credentials username password'
)

ProjectsJsonKeys = namedtuple(
    'ProjectsJsonKeys',
    'type root_directories'
)

JsonKeys = namedtuple(
    'JsonKeys',
    'git projects'
)

JSON_KEYS = JsonKeys(
    git=GitJsonKeys(
        credentials="gitCredentials",
        username="username",
        password="password"
    ),
    projects=ProjectsJsonKeys(
        type="projectsType",
        root_directories="projectsRootDirectories"
    )
)


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

    @property
    def settings(self):
        """Returns the project updater settings as an `settings instance <settings.Settings>`.
        Returns None if no previous settings were set via `set_settings <settings_repository.set_settings>`"""

        if SettingsRepository.__settings_cache:
            return SettingsRepository.__settings_cache

        with open(SETTINGS_JSON_PATH) as json_file:
            try:
                self.__add_to_cache(json.load(json_file))
            except json.decoder.JSONDecodeError:
                return None

        return SettingsRepository.__settings_cache

    @settings.setter
    def settings(self, settings):
        if not settings:
            return

        if not isinstance(settings, Settings):
            raise ValueError("settings is not a Settings instance")

        with open(SETTINGS_JSON_PATH, "w") as json_file:
            settings_data = {
                JSON_KEYS.git.credentials: {
                    JSON_KEYS.git.username: settings.git_credentials.username,
                    JSON_KEYS.git.password: settings.git_credentials.password,
                },
                JSON_KEYS.projects.type: settings.projects_type,
                JSON_KEYS.projects.root_directories: settings.projects_root_directory,
            }

            json.dump(settings_data, json_file)

        SettingsRepository.__settings_cache = settings

    # ------------------------------------------------------------------ PRIVATE METHODS

    def __add_to_cache(self, settings_json_dict):
        if not settings_json_dict:
            return

        SettingsRepository.__settings_cache = self.__create_settings_from_json(
            settings_json_dict)

    def __create_settings_from_json(self, settings_json_dict):
        # git credentials
        username = settings_json_dict[JSON_KEYS.git.credentials][JSON_KEYS.git.username]
        password = settings_json_dict[JSON_KEYS.git.credentials][JSON_KEYS.git.password]
        credentials = GitCredentials(username, password)

        # project settings
        projects_type = settings_json_dict[JSON_KEYS.projects.type]
        projects_root_directories = settings_json_dict[JSON_KEYS.projects.root_directories]

        return Settings(credentials, projects_root_directories, projects_type)
