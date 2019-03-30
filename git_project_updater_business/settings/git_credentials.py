class GitCredentials:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def __str__(self):
        return "Username: {username} \nPassword: {password}".format(
            username=self.__username,
            password=self.__password
        )
