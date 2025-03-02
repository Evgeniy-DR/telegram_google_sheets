
TOKEN = '7049713479:AAHGvr0WUFJL7wk65ZgnvMon-IU3juobS-I'

# Список пользователей и их данные
USERS = {
    'username1': {'password': 'password1', 'sheet_id': '1-pX8pltLU2IwFBjMir6j0nHDXVRxp-BcNPfo_9okH40', 'message_count': 0, 'is_admin': False},
    'admin_username': {'password': 'admin_password', 'sheet_id': None, 'message_count': 0, 'is_admin': True},
    # Добавьте других пользователей
}

# Хранение последней успешной аутентификации пользователей
LAST_AUTH = {user: None for user in USERS}
