from git_project_updater_cli.commands.command_factory import create_command


def main():
    while True:
        print_menu()
        command_number = input("Enter action number:")
        command = create_command(command_number)
        print("\n", command)
        command.execute()


def print_menu():
    print("\n=========================================")
    print("Git project updater CLI. Choose a number and press enter")
    print("1. Set project settings")
    print("2. Print project settings")
    print("3. List projects")
    print("0. Exit")
    print("=========================================\n")


if __name__ == "__main__":
    main()
