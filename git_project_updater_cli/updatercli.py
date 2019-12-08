from git_project_updater_cli.commands import command_factory


def main():
    while True:
        print_menu()
        command_number = input("Enter action number:")
        command = command_factory.create_command(command_number)
        print(f"\n{command}")
        command.execute()


def print_menu():
    print("\n======================================================")
    print("Git project updater CLI. Choose a number and press enter")
    print("1. Set project settings")
    print("2. Print project settings")
    print("3. List projects")
    print("4. List project children ids")
    print("5. Print project dependency tree")
    print("6. Get project version")
    print("7. Get project version used in...")
    print("8. Get project git info")
    print("0. Exit")
    print("========================================================\n")


if __name__ == "__main__":
    main()
