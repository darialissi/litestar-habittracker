class NotAuthorizedException(Exception):
    def __init__(self, message: str = "You are unauthorized!"):
        super().__init__()
        self.message = message
