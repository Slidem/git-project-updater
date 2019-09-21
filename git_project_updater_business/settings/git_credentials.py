class GitCredentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "Username: {username} \nPassword: {password}".format(
            username=self.username,
            password=self.password
        )
