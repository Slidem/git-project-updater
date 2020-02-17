def map_settings(settings):
    return {
        "gitCredentials": {
            "username": settings.git_credentials.username,
            "password": settings.git_credentials.password,
        },
        "projectsType": settings.projects_type,
        "projectsRootDirectories": settings.projects_root_directory
    }
