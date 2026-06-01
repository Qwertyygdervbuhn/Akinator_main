import telebot
from src.bot_controller import TelegramAkinatorController
import config

# Инициализируем объект бота и передаем ему токен из файла конфигурации
bot = telebot.TeleBot(config.BOT_TOKEN)
# Создаем экземпляр нашего контроллера для связи логики и интерфейса мессенджера
controller = TelegramAkinatorController(bot)

# Декоратор для обработки системной команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Передаем ID чата и ID пользователя в контроллер для инициализации сессии
    controller.start_game(message.chat.id, message.from_user.id)

# Декоратор для перехвата любых текстовых сообщений и нажатий кнопок от пользователя
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Передаем входящий текст на обработку в логический блок контроллера
    controller.handle_user_answer(message.chat.id, message.from_user.id, message.text)

# Точка входа для запуска скрипта
if __name__ == "__main__":
    print("Робот-Акинатор успешно запущен...")
    # Запуск постоянного опроса серверов Телеграм на наличие новых сообщений (бесконечный цикл)
    bot.infinity_polling()