FROM python:3.9-slim

WORKDIR /app

# Копируем файлы из текущей директории в контейнер
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY for-example.json /app/for-example.json

EXPOSE 5000

CMD ["python", "/app/src/main.py"]

