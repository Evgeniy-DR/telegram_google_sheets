# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы из текущей директории в контейнер
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл с учетными данными для Google API
COPY for-example.json /app/for-example.json

# Открываем порт, если ваш бот работает через вебхуки (не обязательно)
EXPOSE 5000

# Указываем команду для запуска бота
CMD ["python", "/app/src/main.py"]

