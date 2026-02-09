from datetime import date


class TokenInvalidError(Exception):
    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.message = f"Невалидный токен <{token}>"


class HabitNotFoundError(Exception):
    def __init__(self, title: str, username: str):
        super().__init__()
        self.title = title
        self.username = username
        self.message = f"У пользователя <{username}> нет привычки <{title}>"


class HabitAlreadyExistsError(Exception):
    def __init__(self, title: str, username: str):
        super().__init__()
        self.title = title
        self.username = username
        self.message = f"У пользователя <{username}> уже есть привычка <{title}>"


class HabitAlreadyCompletedTodayError(Exception):
    def __init__(self, title: str, completed_at: date):
        self.title = title
        self.completed_at = completed_at
        self.message = f"Привычка <{title}> уже была отмечена сегодня ({completed_at})"
