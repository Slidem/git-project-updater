COMMANDS_REGISTRY = {}


def register_command(command):
    if command.code in COMMANDS_REGISTRY.keys():
        raise ValueError("Duplicate command found in registry")

    COMMANDS_REGISTRY[command.code] = command


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

    command = COMMANDS_REGISTRY.get(command_code)
    if not command:
        raise ValueError(
            f"Command not found in registry for command code: {command_code}")

    return command
