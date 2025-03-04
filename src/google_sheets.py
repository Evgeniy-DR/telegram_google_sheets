import gspread
import logging
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение пути к файлу учетных данных из переменной окружения
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')

# Авторизация и настройка соединения с Google Sheets
def authorize_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"Файл учетных данных '{CREDENTIALS_FILE}' не найден.")

    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(credentials)
        logger.info("Авторизация прошла успешно.")
        return client
    except Exception as e:
        logger.error("Ошибка авторизации: %s", e)
        raise

# Добавление данных в Google Sheets
def add_data_to_sheet(sheet_id, data):
    if not isinstance(data, list):
        return "Ошибка: данные должны быть в формате списка."
    
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)
        
        # Получение текущего времени в формате строки
        current_time = datetime.now().strftime("%d-%m-%Y")
        
        # Добавление отметки времени к данным
        data_with_timestamp = [current_time] + data
        
        # Добавление данных в конец таблицы
        worksheet.append_row(data_with_timestamp)
        
        logger.info("Данные успешно добавлены в таблицу (sheet_id: %s)", sheet_id)
        return "Данные успешно добавлены в таблицу!"
    except Exception as e:
        logger.error("Ошибка при добавлении данных: %s", e)
        return f"Ошибка при добавлении данных: {str(e)}"

def update_salary(sheet_id, new_value):
    column_index = 14

    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        # Получение номера последней строки с данными
        last_row = len(worksheet.get_all_values())

        if last_row == 0:
            return "Ошибка: таблица пуста."

        # Обновление данных в указанной колонке последней строки
        worksheet.update_cell(last_row, column_index, new_value)

        logger.info("Данные в колонке %d последней строки обновлены (sheet_id: %s)", column_index, sheet_id)
        return "Данные успешно добавлены в таблицу!"
    except Exception as e:
        logger.error("Ошибка при обновлении данных: %s", e)
        return f"Ошибка при обновлении данных: {str(e)}"

# Получение последней строки из Google Sheets
def get_last_row_from_sheet(sheet_id):
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        if all_rows:
            last_row = all_rows[-1]
            logger.info("Последняя строка получена (sheet_id: %s)", sheet_id)
            return last_row
        else:
            return "Таблица пуста."
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return f"Ошибка при чтении данных: {str(e)}"

# Получение данных из второй колонки всех строк, кроме первой строки
def get_second_column_except_header(sheet_id):
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        # Получаем все строки таблицы
        all_rows = worksheet.get_all_values()

        if all_rows:
            # Извлекаем данные из второй колонки, пропуская заголовок (первую строку)
            second_column_data = [row[1] for row in all_rows[1:] if len(row) > 1]
            logger.info("Данные из второй колонки получены (sheet_id: %s)", sheet_id)
            return second_column_data
        else:
            return "Таблица пуста."
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return f"Ошибка при чтении данных: {str(e)}"

def get_18th_column_last_row(sheet_id):
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        if all_rows:
            last_row = all_rows[-1]
            if len(last_row) >= 18:
                value_18th_column = last_row[17]  # Индекс 17 соответствует 18-й колонке
                logger.info("Значение из 18-й колонки получено (sheet_id: %s)", sheet_id)
                return value_18th_column
            else:
                logger.warning("В последней строке нет 18 колонок (sheet_id: %s)", sheet_id)
                return None
        else:
            logger.warning("Таблица пуста (sheet_id: %s)", sheet_id)
            return None
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return None

def get_11th_column_last_row(sheet_id):  # Зарплата
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        if all_rows:
            last_row = all_rows[-1]
            if len(last_row) >= 11:
                value_11th_column = last_row[10]  # Индекс 10 соответствует 11-й колонке
                logger.info("Значение из 11-й колонки получено (sheet_id: %s)", sheet_id)
                return value_11th_column
            else:
                logger.warning("В последней строке нет 11 колонок (sheet_id: %s)", sheet_id)
                return None
        else:
            logger.warning("Таблица пуста (sheet_id: %s)", sheet_id)
            return None
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return None

def get_10th_column_last_row(sheet_id):  # Выручка за день
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        if all_rows:
            last_row = all_rows[-1]
            if len(last_row) >= 10:
                value_10th_column = last_row[9]  # Индекс 9 соответствует 10-й колонке
                logger.info("Значение из 10-й колонки получено (sheet_id: %s)", sheet_id)
                return value_10th_column
            else:
                logger.warning("В последней строке нет 10 колонок (sheet_id: %s)", sheet_id)
                return None
        else:
            logger.warning("Таблица пуста (sheet_id: %s)", sheet_id)
            return None
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return None

# Исправлено: дублирующаяся функция get_18th_column_last_row заменена на правильную нумерацию
def get_18th_column_last_row(sheet_id):  # Остаток наличных в конце смены
    try:
        client = authorize_google_sheets()
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)

        all_rows = worksheet.get_all_values()

        if all_rows:
            last_row = all_rows[-1]
            if len(last_row) >= 18:
                value_18th_column = last_row[17]  # Индекс 17 соответствует 18-й колонке
                logger.info("Значение из 18-й колонки получено (sheet_id: %s)", sheet_id)
                return value_18th_column
            else:
                logger.warning("В последней строке нет 18 колонок (sheet_id: %s)", sheet_id)
                return None
        else:
            logger.warning("Таблица пуста (sheet_id: %s)", sheet_id)
            return None
    except Exception as e:
        logger.error("Ошибка при чтении данных: %s", e)
        return None
