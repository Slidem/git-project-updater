import sys


def exitable_input(prompt_text):
    """ Util that wraps the actual input function, but exits the program if 0 is typed """

    user_input = input(prompt_text)
    if "0" == user_input:
        sys.exit()

    return user_input
