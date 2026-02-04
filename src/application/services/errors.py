class HabitNotFoundError(Exception):
    def __init__(self, title: str, username: str):
        super().__init__(f"У пользователя <{username}> нет привычки <{title}>")
        self.title = title
        self.username = username


class HabitAlreadyExistsError(Exception):
    def __init__(self, title: str, username: str):
        super().__init__(f"У пользователя <{username}> уже есть привычка <{title}>")
        self.title = title
        self.username = username
