from git_project_updater_cli.commands.exit_command import ExitCommand
from git_project_updater_cli.commands.list_project_children_command import ListProjectChildrenIds
from git_project_updater_cli.commands.print_settings_command import PrintCommand
from git_project_updater_cli.commands.set_settings_command import SetSettingsCommand
from git_project_updater_cli.commands.list_projects_command import ListProjectsCommand


def create_command(command):
    if "0" == command:
        return ExitCommand()
    if "1" == command:
        return SetSettingsCommand()
    if "2" == command:
        return PrintCommand()
    if "3" == command:
        return ListProjectsCommand()
    if "4" == command:
        return ListProjectChildrenIds()
    
