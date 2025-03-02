from datetime import datetime
from config import USERS, LAST_AUTH

def check_password(username, password):
    """Проверка введенного пароля пользователя"""
    return USERS.get(username, {}).get('password') == password

def is_authenticated(username):
    """Проверяет, был ли пользователь аутентифицирован сегодня"""
    last_auth = LAST_AUTH.get(username)
    if last_auth is None:
        return False
    return last_auth.date() == datetime.now().date()

def update_last_auth(username):
    """Обновляет метку времени последней успешной аутентификации и сбрасывает счетчик сообщений"""
    LAST_AUTH[username] = datetime.now()
    USERS[username]['message_count'] = 0  # Сброс счетчика сообщений

def is_admin(username):
    """Проверяет, является ли пользователь администратором"""
    return USERS.get(username, {}).get('is_admin', False)
