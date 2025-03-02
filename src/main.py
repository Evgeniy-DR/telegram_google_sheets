from handlers.handler import bot
import logging


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
            handlers=[
            logging.StreamHandler()  # Вывод логов в консоль
        ]
    )
    bot.infinity_polling(
        long_polling_timeout = 30
    )

