from git_project_updater_cli.commands.set_settings_command import SetSettingsCommand
from git_project_updater_cli.commands.print_settings_command import PrintSettingsCommand
from git_project_updater_cli.commands.list_projects_command import ListProjectsCommand
from git_project_updater_cli.commands.list_project_children_command import ListProjectChildrenIds
from git_project_updater_cli.commands.deptree_command import ProjectDependencyTreeCommand
from git_project_updater_cli.commands.project_version_command import ProjectVersionCommand
from git_project_updater_cli.commands.project_version_command_used_in import ProjectVersionUsedInCommand
from git_project_updater_cli.commands.exit_command import ExitCommand
from git_project_updater_cli.commands.unknown_command import UnkownCommand
from git_project_updater_cli.commands.git_info_command import GitInfoCommand
from git_project_updater_cli.commands.git_update_command import GitUpdateCommand
from git_project_updater_cli.commands.build_project_command import BuildProjectCommand
from git_project_updater_cli.commands.change_project_version import ChangeProjectVersionCommand


COMMANDS_REGISTRY = {}

DEFAULT_COMMAND = UnkownCommand()


def register_command(command):
    if command.code in COMMANDS_REGISTRY.keys():
        raise ValueError(
            f"Duplicate command found in registry for code {command.code}")

    COMMANDS_REGISTRY[command.code] = command


def register_commands():
    register_command(SetSettingsCommand())
    register_command(PrintSettingsCommand())
    register_command(ListProjectsCommand())
    register_command(ListProjectChildrenIds())
    register_command(ProjectDependencyTreeCommand())
    register_command(ProjectVersionCommand())
    register_command(ProjectVersionUsedInCommand())
    register_command(GitInfoCommand())
    register_command(GitUpdateCommand())
    register_command(BuildProjectCommand())
    register_command(ChangeProjectVersionCommand())
    register_command(ExitCommand())


def create_command(command_code):
    """
    Creates a new command based on the command code.
    Check also git_project_updater_cli.commands.command.py

    Parameters
    ----------

    command_code : str
        Command code; str that represents a number

    Returns
    -------
        Command instance if successfull

    Raises
    ------
        ValueError if command not found for the given command_code
    """

    if not COMMANDS_REGISTRY:
        register_commands()

    command = COMMANDS_REGISTRY.get(command_code.strip())
    return command if command else DEFAULT_COMMAND
