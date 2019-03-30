from git_project_updater_business.settings.settings_repository import set_settings
from git_project_updater_business.settings.settings_repository import get_settings
from git_project_updater_cli.commands.command_factory import create_command


def main():
    while True:
        print_menu()
        command_number = input("Enter action number:")
        command = create_command(command_number)
        print(command)
        command.execute()


def print_menu():
    print("=========================================")
    print("Git project updater CLI. Choose a number and press enter")
    print("1. Set project settings")
    print("2. Print project settings")
    print("0. Exit")
    print("=========================================")

    pass


if __name__ == "__main__":
    main()
