from tkinter import messagebox, simpledialog
from src.models import KnowledgeBase, Node
import config


class AkinatorController:
    def __init__(self):
        self.db = KnowledgeBase()
        self.root_node = self.db.load()
        self.current_node = self.root_node
        self.step_count = 0
        self.view = None

    def set_view(self, view):
        self.view = view
        self.refresh_ui()

    def refresh_ui(self):
        if self.step_count >= config.MAX_QUESTIONS and self.current_node.is_character == False:
            self.view.draw_jinni("shocked")
            messagebox.showinfo("Я сдаюсь!", "Я не смог отгадать персонажа за 20 вопросов. Рассказали, кто это!")
            self.learn_new_character()
            return

        if self.current_node.is_character == False:
            self.step_count = self.step_count + 1
            self.view.lbl_step.config(text="ВОПРОС №" + str(self.step_count))
            self.view.lbl_text.config(text=self.current_node.text, fg="#1e272e")

            self.view.b_yes.config(text="Да", bg="#1b9cfc")
            self.view.b_no.config(text="Нет", bg="#1b9cfc")

            self.view.b_dont_know.config(state="normal")
            self.view.b_maybe.config(state="normal")
            self.view.b_probably_not.config(state="normal")

            if self.step_count <= 10:
                self.view.draw_jinni("thinking")
                self.view.bubble.config(text="Загадывайте! Я готов.")
            else:
                self.view.draw_jinni("shocked")
                self.view.bubble.config(text="Круг сужается... Хмм...")
        else:
            self.view.lbl_step.config(text="АКИНАТОР ДУМАЕТ...")
            self.view.draw_jinni("confident")
            self.view.bubble.config(text="Я прочитал ваши мысли!")
            self.view.lbl_text.config(text="Это должно быть:\n\n👉 " + self.current_node.text + " 👈", fg="#2ecc71")

            self.view.b_yes.config(text="ДА, ВЕРНО!", bg="#2ecc71")
            self.view.b_no.config(text="НЕТ, НЕ ОН", bg="#e74c3c")

            self.view.b_dont_know.config(state="disabled")
            self.view.b_maybe.config(state="disabled")
            self.view.b_probably_not.config(state="disabled")

    def handle_answer(self, is_yes):
        if self.current_node.is_character == True:
            if is_yes == True:
                messagebox.showinfo("Победа!", "Акинатор снова всех победил!")
                self.restart_game()
            else:
                self.learn_new_character()
        else:
            if is_yes == True:
                if self.current_node.yes is not None:
                    self.current_node = self.current_node.yes
            else:
                if self.current_node.no is not None:
                    self.current_node = self.current_node.no
            self.refresh_ui()

    def skip_question(self):
        if self.current_node.is_character == False:
            if self.current_node.no is not None:
                self.current_node = self.current_node.no
                self.refresh_ui()

    def learn_new_character(self):
        new_char = simpledialog.askstring("Акинатор проиграл", "Кого же вы загадали?")
        if new_char is None or new_char == "":
            self.restart_game()
            return

        if self.current_node.is_character == False:
            q = simpledialog.askstring("Обучение", "Задайте вопрос для " + new_char + " (Ответ 'ДА'):")
            if q is None or q == "":
                self.restart_game()
                return
            old_yes = self.current_node.yes
            self.current_node.yes = Node(q)
            self.current_node.yes.yes = Node(new_char, True)
            if old_yes is not None:
                self.current_node.yes.no = old_yes
            else:
                self.current_node.yes.no = Node("Кто-то другой", True)
        else:
            wrong_char = self.current_node.text
            q = simpledialog.askstring("Обучение",
                                       "Чем " + new_char + " отличается от " + wrong_char + "?\n(Ответ 'ДА' должен быть для " + new_char + "):")
            if q is None or q == "":
                self.restart_game()
                return
            self.current_node.text = q
            self.current_node.is_character = False
            self.current_node.yes = Node(new_char, True)
            self.current_node.no = Node(wrong_char, True)

        self.db.save(self.root_node)
        messagebox.showinfo("Успех!", "Новый персонаж успешно добавлен в базу данных!")
        self.restart_game()

    def restart_game(self):
        self.current_node = self.root_node
        self.step_count = 0
        self.refresh_ui()