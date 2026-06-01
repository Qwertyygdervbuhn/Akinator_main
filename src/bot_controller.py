from telebot import types
from src.models import KnowledgeBase, Node
import config


class TelegramAkinatorController:
    def __init__(self, bot):
        # Сохраняем объект бота для отправки сообщений
        self.bot = bot
        # Инициализируем объект для работы с базой данных
        self.db = KnowledgeBase()
        # Загружаем корневой узел бинарного дерева из JSON-файла
        self.root_node = self.db.load()

        # Словарь для отслеживания текущего узла дерева для каждого игрока по его ID
        self.user_nodes = {}
        # Словарь для хранения счетчика вопросов для каждого пользователя отдельно
        self.user_steps = {}

    def start_game(self, chat_id, user_id):
        # При старте сбрасываем указатель на начало дерева персонажей
        self.user_nodes[user_id] = self.root_node
        # Обнуляем счетчик шагов для данного пользователя
        self.user_steps[user_id] = 0
        # Вызываем метод отправки текущего вопроса в чат
        self.send_question(chat_id, user_id)

    def send_question(self, chat_id, user_id):
        # Получаем узел дерева и шаг конкретного пользователя из словарей
        current_node = self.user_nodes[user_id]
        step = self.user_steps[user_id]

        # Проверка условия окончания игры по лимиту в 20 вопросов (согласно ТЗ)
        if step >= config.MAX_QUESTIONS and current_node.is_character == False:
            self.bot.send_message(chat_id,
                                  "Я сдаюсь! Я не смог угадать персонажа за 20 вопросов. Напишите /start, чтобы начать заново.")
            return

        # Если текущий узел — это вопрос, а не конечный персонаж
        if current_node.is_character == False:
            # Инкрементируем счетчик шагов на 1
            self.user_steps[user_id] = step + 1
            # Формируем строку текста для отправки в Телеграм
            text = "Вопрос №" + str(self.user_steps[user_id]) + "\n\n" + current_node.text

            # Создаем блок экранных кнопок для удобства пользователя
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            # Добавляем кнопки в строки с помощью метода row
            markup.row("Да", "Нет")
            markup.row("Я не знаю", "Возможно")
            markup.row("Скорее нет", "Заново")

            # Отправляем сообщение с прикрепленной клавиатурой ответов
            self.bot.send_message(chat_id, text, reply_markup=markup)

        # Если дерево дошло до листа (конечного узла с именем персонажа)
        else:
            text = "Я думаю, это:\n\n👉 " + current_node.text + " 👈\n\nЯ угадал?"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row("Да, верно!", "Нет, не он")

            self.bot.send_message(chat_id, text, reply_markup=markup)

    def handle_user_answer(self, chat_id, user_id, answer):
        # Защита: если пользователь пишет боту без предварительного нажатия /start
        if user_id not in self.user_nodes:
            self.start_game(chat_id, user_id)
            return

        current_node = self.user_nodes[user_id]

        # Если нажата кнопка экстренного сброса игры
        if answer == "Заново":
            self.start_game(chat_id, user_id)
            return

        # Обработка ответов на этапе, когда бот назвал персонажа
        if current_node.is_character == True:
            if answer == "Да, верно!":
                # Случай победы бота — удаляем кнопки и очищаем данные сессии
                self.bot.send_message(chat_id, "Ура! Я снова выиграл! Напишите /start, чтобы сыграть еще раз.",
                                      reply_markup=types.ReplyKeyboardRemove())
                del self.user_nodes[user_id]
            elif answer == "Нет, не он":
                # Случай проигрыша бота
                self.bot.send_message(chat_id,
                                      "Эх, я проиграл... База данных Телеграм-версии пока обучается через консоль. Напишите /start для новой игры.",
                                      reply_markup=types.ReplyKeyboardRemove())
                del self.user_nodes[user_id]
            return

        # Навигация по бинарному дереву в зависимости от выбранного ответа
        if answer == "Да":
            if current_node.yes is not None:
                # Переходим по левой ветке (истина)
                self.user_nodes[user_id] = current_node.yes
        elif answer == "Нет" or answer == "Скорее нет":
            if current_node.no is not None:
                # Переходим по правой ветке (ложь)
                self.user_nodes[user_id] = current_node.no
        elif answer == "Я не знаю" or answer == "Возможно":
            # Нейтральные ответы для простоты кода приравниваем к ветке "Нет"
            if current_node.no is not None:
                self.user_nodes[user_id] = current_node.no

        # Рекурсивный переход к следующему шагу игры
        self.send_question(chat_id, user_id)