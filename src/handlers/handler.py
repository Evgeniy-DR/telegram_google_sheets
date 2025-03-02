
from google_sheets import add_data_to_sheet, get_last_row_from_sheet, get_second_column_except_header, get_18th_column_last_row, get_10th_column_last_row, get_11th_column_last_row, update_salary, get_18th_column_last_row
import telebot
import logging
from telebot import types
from time import time as current_time, sleep  # Импортируем sleep отдельно
from datetime import datetime
from functools import partial
from user_message import authorization_messages, get_operator_greeting

# Объявляем токен бота и создаем объект бота
BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# ID ваших Google таблиц
google_sheet_ids = {
    #____________________lists of long sheets_______________________

    'password2': "1F7dlxhD5FhQ0MLlel1QDVG8DQLFCk5Q5WPpiFpA2oBI", # name sheets: Local_ForYouCars
    'спутник тюбинг': "1I8fF6UXZA7S4U3qqMSjlOkCGQ1CnPlYVvLnhWx54q50", # name sheets: misha for relise


    #____________________lists of short sheets_______________________

    'password3': "1f9qWotOTJg_8I22QGFiH6bHsKQ2YliX9iYYlRB6jud0",
    'password4': "1C7GVuk9mHNfy2dgkY_h1uguAJX6-lwqx6PiImz5w_vE", # name sheets: Local_ForYouCars_Short
}

# Словарь для хранения временных данных пользователей и их авторизации
authorized_users = []
user_data = {}
start_sum_entered = False


AUTHORIZATION_TIMEOUT = 600  # Тайм-аут для повторной авторизации в секундах (1 час)

# Настройки колонок для ввода

passwords_data = {
    'password': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
            'T': "Статистика \nпоездок без оплаты",
            'U': "Танк:",
            'V': "Карета:",
            'W': "Маквин:",
            'X': "Кошечка:",
            'Y': "Спорткар:",
            'Z': "Полиция:"
        }
    },
    'password1': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
            'T': "Статистика \nпоездок без оплаты",
            'U': "Танк:",
            'V': "Карета:",
            'W': "Маквин:",
            'X': "Кошечка:",
            'Y': "Спорткар:",
            'Z': "Полиция:"
        }
    },
    'password2': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате Ч,M):",
            'D': "Время закрытия (в формате Ч,M):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
            'T': "Статистика \nпоездок без оплаты",
            'U': "Танк:",
            'V': "Карета:",
            'W': "Маквин:",
            'X': "Кошечка:",
            'Y': "Спорткар:",
            'Z': "Полиция:"
        }
    },
    'password3': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'N', 'O', 'P', 'Q', 'S'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
        }
    },
    'password4': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'O', 'P', 'Q', 'S'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
        }
    },
    'спутник тюбинг':  {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'O', 'P', 'Q', 'S'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
        }
    },
    'password for future': {
        'columns': ['B', 'C', 'D', 'G', 'H', 'I', 'N', 'O', 'P', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        'column_prompts': {
            'B': "Смена:",
            'C': "Время открытия (в формате HH,MM):",
            'D': "Время закрытия (в формате HH,MM):",
            'G': "Выручка Наличные:",
            'H': "Выручка Переводы:",
            'I': "Выручка Терминал:",
            'N': "Забрали ЗП:",
            'O': "Расходы:",
            'P': "Перевод Мише или Антону:",
            'Q': "Забрал нал. Миша или Антон:",
            'S': "Примечание:",
            'T': "Статистика \nпоездок без оплаты",
            'U': "Танк:",
            'V': "Карета:",
            'W': "Маквин:",
            'X': "Кошечка:",
            'Y': "Спорткар:",
            'Z': "Полиция:"
        }
    },
}


def is_authorization_expired(chat_id):
    auth_time = user_data.get(chat_id, {}).get('authorized_at')
    return auth_time is None or (current_time() - auth_time) > AUTHORIZATION_TIMEOUT

# Функция повторной авторизации
def reauthorize_user(chat_id):
    """Удаляет пользователя из списка авторизованных, позволяя заново ввести пароль."""
    if chat_id in authorized_users:
        authorized_users.remove(chat_id)  # Удаляем пользователя из списка авторизованных
        user_data.pop(chat_id, None)  # Очищаем данные, привязанные к пользователю
    bot.send_message(chat_id, "Вы вышли из системы.")

@bot.message_handler(commands=['start'])
def start_command(m):
    if m.chat.id in authorized_users and not is_authorization_expired(m.chat.id):
        show_main_menu(m.chat.id)
    else:
        bot.send_message(m.chat.id, "Для авторизации введите пароль:")


# Обработчик для аутентификации пользователя
@bot.message_handler(func=lambda m: m.chat.id not in authorized_users or is_authorization_expired(m.chat.id))
def authenticate_user(m):
    password = m.text.lower()
    if password in passwords_data:
        data = passwords_data[password]
        google_sheet_id = google_sheet_ids[password]
        columns = data['columns']
        column_prompts = data['column_prompts']

    else:
        bot.send_message(m.chat.id, "Неверный пароль. Попробуйте снова.")
        return

    # Авторизация пользователя с привязкой к таблице
    if m.chat.id not in authorized_users:
        authorized_users.append(m.chat.id)
    
    user_data[m.chat.id] = {
        'google_sheet_id': google_sheet_id,
        'authorized_at': current_time(),
        'columns': columns,  # Сохраняем колонки в данные пользователя
        'column_prompts': column_prompts,  # Сохраняем подсказки в данные пользователя
        'password': password
    }
    
    sleep(1.5)  # Пауза перед отправкой меню
    request_phone_number(m.chat.id)

    # Отображение главного меню после короткой паузы
    sleep(1.5)  # Пауза перед отправкой меню


def request_phone_number(chat_id, message=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    markup.add(button_phone)
    bot.send_message(chat_id, "Пожалуйста, нажмите кнопку 'Отправить номер' для завершения авторизации:", reply_markup=markup)

    if message is None:
        return

    authorized_phone_numbers = get_second_column_except_header("1BNby3mDFw7OBeMAn8F9q0wDFEc_PF4M0ON5JzX_bb6A")
    authorized_phone_numbers = [num.strip() for num in authorized_phone_numbers]  # Убираем пробелы
    print(authorized_phone_numbers)

    if message.contact:
        phone_number = message.contact.phone_number

        if phone_number in authorized_phone_numbers:
            bot.send_message(chat_id, "Авторизация пройдена", reply_markup=types.ReplyKeyboardRemove())

            show_main_menu(chat_id)
        else:
            bot.send_message(chat_id, "Ваш номер телефона не найден в системе. Авторизация отклонена.", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Ошибка. Попробуйте снова отправить ваш номер телефона.")



@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    
    try:
        # Загрузка списка номеров из Google Sheets
        authorized_phone_numbers = get_second_column_except_header("1BNby3mDFw7OBeMAn8F9q0wDFEc_PF4M0ON5JzX_bb6A")
        authorized_phone_numbers = [f"7{num.strip()}" for num in authorized_phone_numbers]  # Преобразуем формат
        logger.info("Список авторизованных номеров: %s", authorized_phone_numbers)
    except Exception as e:
        logger.error("Ошибка загрузки номеров из Google Sheets: %s", e)
        bot.send_message(chat_id, "Временная ошибка сервера. Попробуйте позже.")
        return

    if message.contact and message.contact.phone_number:
        # Убираем "+"
        phone_number = message.contact.phone_number.lstrip('+')
        logger.info("Полученный номер телефона: %s", phone_number)

        if phone_number in authorized_phone_numbers:
            # Успешная авторизация
            bot.send_message(chat_id, "Авторизация завершена", reply_markup=types.ReplyKeyboardRemove())

            password = user_data[chat_id]['password']
            welcome_message = authorization_messages.get(password)

            operator_greeting = get_operator_greeting()
            bot.send_message(chat_id, f"{message.from_user.first_name}, {operator_greeting}")

            if callable(welcome_message):  # Проверяем, является ли сообщение функцией
                welcome_message = welcome_message()
                bot.send_message(chat_id, welcome_message)
                sleep(2)
            show_main_menu(chat_id)
        else:
            # Номер телефона не найден
            bot.send_message(chat_id, "Ваш номер телефона не найден в системе. Авторизация отклонена.", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Ошибка. Попробуйте снова отправить ваш номер телефона.")


def send_session_expired_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton("Авторизоваться заново", callback_data="start_auth")
    markup.add(start_button)
    bot.send_message(chat_id, "Время сессии истекло. Пожалуйста, авторизуйтесь снова, нажав на кнопку ниже.", reply_markup=markup)
    if chat_id in authorized_users:
        authorized_users.remove(chat_id)

@bot.callback_query_handler(func=lambda call: call.data == "start_add_data")
def start_add_data(call):
    chat_id = call.message.chat.id
    if is_authorization_expired(call.message.chat.id):
        send_session_expired_message(call.message.chat.id)
        return

    # Очищаем данные и начинаем процесс добавления данных по колонкам
    user_data[call.message.chat.id]['data'] = []
    ask_for_column_data(call.message.chat.id, 0)
    # show_confirmation_menu(call.message.chat.id)
    # show_main_menu(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "start_auth")
def handle_start_auth(call):
    chat_id = call.message.chat.id
    reauthorize_user(chat_id)  # Вызываем функцию для повторной авторизации
    start_command(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "start_get_data")
def start_get_data(call):
    chat_id = call.message.chat.id
    
    # Проверяем, истекла ли сессия
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    # Проверяем наличие пароля у пользователя
    if chat_id not in user_data or 'password' not in user_data[chat_id]:
        bot.send_message(chat_id, "Ошибка: пользователь не авторизован.")
        return

    password = user_data[chat_id]['password']
    user_data[chat_id]['data'] = []
    google_sheet_id = user_data[chat_id]['google_sheet_id']
    last_row = get_last_row_from_sheet(google_sheet_id)
    
    # Получаем данные для указанного пароля из passwords_data
    password_data = passwords_data.get(password)
    
    if not password_data:
        bot.send_message(chat_id, "Ошибка: неверный пароль или нет данных для этого пароля.")
        return
    
    # Список основных колонок
    columns = [
        'Дата', 'Смена', 'Время открытия', 'Время закрытия', 'Отработано часов',
        'Касса наличные', 'Выручка Наличные', 'Выручка Переводы', 'Выручка Терминал',
        'ВЫРУЧКА ВСЕГО', 'Зарплата/Оклад', 'Премия', 'Штраф', 'Забрали ЗП', 'Расходы',
        'Перевод Мише или Антону', 'Забрал нал. Миша или Антон', 'Остаток наличные', 'Примечание'
    ]
    
    # Дополнительные колонки для расширенных данных
    extended_columns = [
        'Без оплаты', 'Танк', 'Карета', 'Маквин', 'Кошечка',
        'Спорткар', 'Police', 'Статистика'
    ]
    
    column_prompts = password_data['column_prompts']

    # Проверка наличия данных о колонках
    if not columns or not column_prompts:
        bot.send_message(chat_id, "Ошибка. Не удалось получить данные о колонках.")
        return
    
    # Формируем строку для основных колонок
    data_preview = "\n".join(
        f"{column_prompts.get(columns[i], columns[i])}: {last_row[i]}" 
        for i in range(len(columns))  # Для первых основных колонок
    )

    # Добавляем дополнительные данные, если они есть
    if len(last_row) > len(columns):
        extended_data = "\n".join(
            f"{extended_columns[i]}: {last_row[i + len(columns)]}" 
            for i in range(len(extended_columns))  # Дополнительные колонки
        )
        data_preview += "\n" + extended_data

    # Отправляем сообщение с данными
    bot.send_message(chat_id, f"Последняя строка в таблице:\n{data_preview}")

    # Отображаем основное меню
    show_main_menu(chat_id)


# Функция для запроса данных для конкретной колонки
def ask_for_column_data(chat_id, column_index):
    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Ошибка авторизации. Пожалуйста, попробуйте авторизоваться заново.")
        return

    columns = user_info.get('columns')
    column_prompts = user_info.get('column_prompts')
    if column_index < len(columns):
        column_letter = columns[column_index]
        prompt = column_prompts[column_letter]
        msg = bot.send_message(chat_id, prompt)

        # Используем partial, чтобы зафиксировать значение column_index
        bot.register_next_step_handler(msg, partial(handle_column_input, column_index=column_index))
    else:
        show_confirmation_menu(chat_id)


# Обработчик для ввода данных в колонку
def handle_column_input(message, column_index):
    chat_id = message.chat.id
    user_data[chat_id]['data'].append(message.text)
    ask_for_column_data(chat_id, column_index + 1)


def show_confirmation_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    
    # Извлекаем данные пользователя
    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Ошибка авторизации. Пожалуйста, попробуйте авторизоваться заново.")
        return

    columns = user_info.get('columns')
    column_prompts = user_info.get('column_prompts')
    user_data_entries = user_info.get('data', [])

    # Формируем текст для подтверждения без кнопок редактирования рядом с каждым пунктом
    data_preview = ""
    for i in range(len(columns)):
        data_preview += f"{i + 1}. {column_prompts[columns[i]]} {user_data_entries[i]}\n"

    # Кнопки "Подтвердить", "Изменить" и "Отменить" на одном уровне
    bt_confirm = types.InlineKeyboardButton("Подтвердить", callback_data="confirm")
    bt_edit = types.InlineKeyboardButton("Изменить", callback_data="edit_menu")
    bt_cancel = types.InlineKeyboardButton("Отменить", callback_data="cancel")
    markup.row(bt_confirm, bt_edit, bt_cancel)

    # Отправляем сообщение с данными и кнопками
    bot.send_message(chat_id, f"Проверьте данные перед добавлением:\n\n{data_preview}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "edit_menu")
def show_edit_menu(call):
    chat_id = call.message.chat.id
    
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    user_info = user_data.get(chat_id)
    columns = user_info.get('columns')
    column_prompts = user_info.get('column_prompts')
    user_data_entries = user_info.get('data', [])

    markup = types.InlineKeyboardMarkup()
    for i in range(len(columns)):
        prompt = column_prompts[columns[i]].rstrip(':')  # Удаляем двоеточие в конце, если есть
        markup.add(types.InlineKeyboardButton(
            f"{prompt}: {user_data_entries[i]}",
            callback_data=f"edit_{i}"
        ))
    markup.add(types.InlineKeyboardButton("Назад", callback_data="back_to_confirm"))

    try:
        data_preview = call.message.text.split(':\n\n')[1]
    except IndexError:
        data_preview = "Данные недоступны"
    bot.edit_message_text(
        text=f"Выберите пункт для редактирования:\n\n{data_preview}",
        chat_id=chat_id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


# Обработчик для выбора конкретного пункта редактирования
@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_"))
def handle_edit(call):
    chat_id = call.message.chat.id
    edit_index = int(call.data.split("_")[1])  # Извлекаем индекс строки для редактирования
    
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    user_info = user_data.get(chat_id)
    column_prompt = user_info['column_prompts'][user_info['columns'][edit_index]]
    bot.send_message(chat_id, f"Введите новое значение для '{column_prompt}' ")
    
    bot.register_next_step_handler_by_chat_id(chat_id, lambda message: update_data(message, edit_index))

# Обработчик для возврата к меню подтверждения
@bot.callback_query_handler(func=lambda call: call.data == "back_to_confirm")
def back_to_confirm(call):
    chat_id = call.message.chat.id
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    show_confirmation_menu(chat_id)  # Возвращаемся к меню подтверждения

def update_data(message, edit_index):
    chat_id = message.chat.id
    new_value = message.text
    
    # Обновляем данные в user_data
    user_data[chat_id]['data'][edit_index] = new_value
    
    # Возвращаемся к меню подтверждения с обновленными данными
    show_confirmation_menu(chat_id)

@bot.callback_query_handler(func=lambda call: call.data in ["confirm", "cancel"])
def handle_answer(call):
    chat_id = call.message.chat.id

    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    if call.data == "confirm":
        user_info = user_data.get(chat_id)
        if not user_info or 'data' not in user_info:
            bot.send_message(chat_id, "Ошибка: данные отсутствуют. Повторите ввод.")
            return
        
        password = user_data[chat_id]['password']
        columns = passwords_data.get(password, {}).get('columns', [])
        columns_user_input = user_info.get('columns', [])

        if columns:
            max_index = max(ord(col) - ord('B') for col in columns)
            full_row = [''] * (max_index + 1)
            data_to_add = user_info['data']
            google_sheet_id = user_info['google_sheet_id']

            for i, col in enumerate(columns_user_input):
                col_index = ord(col) - ord('B')
                if 0 <= col_index < len(full_row):
                    full_row[col_index] = data_to_add[i]

            add_data_to_sheet(google_sheet_id, full_row)

            bot.edit_message_text("Данные успешно добавлены в таблицу!", chat_id, call.message.message_id)
            sleep(6)
            get_11_colums = get_11th_column_last_row(google_sheet_id)
            get_10_colums = get_10th_column_last_row(google_sheet_id)
            get_18_colums = get_18th_column_last_row(google_sheet_id)
            
            bot.send_message(chat_id, f"Выручка за день составляет: {get_10_colums} \nВаша зарплата: {get_11_colums} \nСумма в кассе в конце смены: {get_18_colums} \n\nВведите сумму, которую вы забрали из кассы, выбрав соответствующее меню")
            show_main_menu(chat_id)
            user_data[chat_id].pop('data', None)
    elif call.data == "cancel":
        bot.edit_message_text("Отмена добавления данных.", chat_id, call.message.message_id)
        user_data[chat_id].pop('data', None)
        show_main_menu(chat_id)




        # Удаляем данные пользователя после добавления
        user_data[chat_id].pop('data', None)
    elif call.data == "cancel":
        # Сообщаем об отмене добавления данных
        bot.edit_message_text("Отмена добавления данных.", chat_id, call.message.message_id)

        # Удаляем временные данные
        user_data[chat_id].pop('data', None)


# Сравнение с введенными данными
@bot.callback_query_handler(func=lambda call: call.data == "start_add_data_first")
def start_add_data_first(call):
    chat_id = call.message.chat.id

    # Проверяем авторизацию
    if chat_id not in authorized_users or is_authorization_expired(chat_id):
        bot.send_message(chat_id, "Ваша сессия истекла или вы не авторизованы. Пожалуйста, авторизуйтесь снова.")
        reauthorize_user(chat_id)  # Принудительная деавторизация, если истек срок
        return

    # Инициализируем данные
    if chat_id not in user_data:
        user_data[chat_id] = {}

    google_sheet_id = user_data.get(chat_id, {}).get('google_sheet_id', None)

    if not google_sheet_id:
        bot.send_message(chat_id, "Не найден Google Sheet ID для этого пользователя.")
        return

    # Получаем значение из 18-й колонки последней строки таблицы
    last_value_18th_column = get_18th_column_last_row(google_sheet_id)

    if last_value_18th_column is None:
        bot.send_message(chat_id, "Не удалось получить данные из таблицы. Пожалуйста, проверьте доступ.")
        return

    user_data[chat_id]['expected_value'] = last_value_18th_column
    user_data[chat_id]['notify_chat_id'] = 123456789  # Укажите chat_id получателя уведомлений

    bot.send_message(chat_id, "Введите сумму в кассе:")
    bot.register_next_step_handler_by_chat_id(chat_id, handle_cash_sum)


# Обработчик для ввода суммы в кассе

   # Проверяем авторизацию
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

def handle_cash_sum(message):
    chat_id = message.chat.id
    user_value = message.text.strip()

    # Проверяем авторизацию
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    # Формируем более наглядное отображение имени пользователя
    if message.from_user.username:
        user_display_name = f"@{message.from_user.username}"
    else:
        user_display_name = f"{message.from_user.first_name} {message.from_user.last_name}".strip()
        if not user_display_name:
            user_display_name = f"Пользователь с ID {chat_id}"

    if chat_id not in user_data or 'expected_value' not in user_data[chat_id]:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте начать заново.")
        return

    # Получаем ожидаемое значение и данные для уведомления
    expected_value = user_data[chat_id]['expected_value']
    notify_chat_id = 895889833  # chat_id для уведомления (Мише)
    passwords_data = user_data.get(chat_id, {}).get('password', 'нет данных')  # Пароль пользователя

    # Отправляем пользователю сообщение о добавлении данных
    bot.send_message(chat_id, "👉 Данные успешно добавлены. Оставшиеся пункты заполните после завершения смены.")

    # Проверяем совпадение и формируем сообщение для администратора
    if str(user_value) == str(expected_value):
        bot.send_message(chat_id, "Введенная сумма совпадает с данными в таблице!")
        admin_message = f"Пользователь {passwords_data} ввел сумму: {user_value} (совпадает с ожидаемой: {expected_value})."
    else:
        admin_message = f"Пользователь {passwords_data} ввел некорректное значение суммы: {user_value} (ожидаемое: {expected_value}). Проверьте ситуацию."

    # Всегда отправляем уведомление администратору
    bot.send_message(notify_chat_id, admin_message)

    # Переход в главное меню
    show_main_menu(chat_id)


@bot.callback_query_handler(func=lambda call: call.data == "get_salary")
def get_salary(call):
    chat_id = call.message.chat.id

    # Проверяем авторизацию
    if is_authorization_expired(chat_id):
        send_session_expired_message(chat_id)
        return

    # Инициализируем данные
    if chat_id not in user_data:
        user_data[chat_id] = {}

    google_sheet_id = user_data.get(chat_id, {}).get('google_sheet_id', None)

    if not google_sheet_id:
        bot.send_message(chat_id, "Не найден Google Sheet ID для этого пользователя.")
        return

    bot.send_message(chat_id, "Введите сумму зарплаты, забранной из кассы:")

    # Устанавливаем обработчик следующего сообщения
    bot.register_next_step_handler(call.message, process_salary_input, google_sheet_id)

def process_salary_input(message, google_sheet_id):
    chat_id = message.chat.id
    salary_amount = message.text

    # Проверяем, что введено число
    try:
        salary_amount = float(salary_amount)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректное числовое значение.")
        return
    


    # Добавляем значение в Google Sheet в последнюю строку 14-й колонки
    result_message = update_salary(google_sheet_id, salary_amount)

    bot.send_message(chat_id, result_message)
    show_main_menu(chat_id)


def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔄 Авторизироваться заново", callback_data="start_auth"))
    markup.add(types.InlineKeyboardButton("📊 Отправка статистики", callback_data="show_statistics"))
    # markup.add(types.InlineKeyboardButton("📈 Получение данных", callback_data="start_get_data"))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

def statistics_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Сумма в кассе в начале смены", callback_data="start_add_data_first"))
    markup.add(types.InlineKeyboardButton("Окончание смены", callback_data="start_add_data"))
    markup.add(types.InlineKeyboardButton("Забрали зарплату", callback_data="get_salary"))
    markup.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "show_statistics":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите действие для статистики:", reply_markup=statistics_menu())
    elif call.data == "start_add_data_first":
        start_add_data_first(call.message)
    elif call.data == "start_add_data":
        start_add_data(call.message)    
    elif call.data == "get_salary":
        get_salary(call.message)
    elif call.data == "start_auth":
        reauthorize_user(call.message.chat.id)
    elif call.data == "start_get_data":
        start_get_data(call)
    elif call.data == "back_to_main":
        show_main_menu(call.message.chat.id)
