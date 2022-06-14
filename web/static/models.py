class BaseModel:
    def toJSON(self):
        return vars(self)


class Server(BaseModel):
    def __init__(self, username, host, port, auth_method, password=None,
                 ssh_key=None, _id=None):
        self._id = _id
        self.username = username
        self.host = host
        self.port = port
        self.auth_method = auth_method
        self.password = password
        self.ssh_key = ssh_key

    @staticmethod
    def fromJSON(data: dict):
        return Server(data["username"], data["host"],
                      data["port"], data.get("auth_method"),
                      data.get("password"), data.get("ssh_key"))
