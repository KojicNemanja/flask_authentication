class User:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
    
    def __str__(self):
        s = "Username: {}\n".format(self.username)
        s+= "Password: {}".format(self.password)
        return s