import json
import os
from config import DB_FILENAME


class Node:
    def __init__(self, text, is_character=False):
        self.text = text
        self.is_character = is_character
        self.yes = None
        self.no = None

    def to_dict(self):
        if self.is_character:
            return {"text": self.text, "is_character": True}
        return {
            "text": self.text,
            "is_character": False,
            "yes": self.yes.to_dict() if self.yes else None,
            "no": self.no.to_dict() if self.no else None
        }

    @staticmethod
    def from_dict(d):
        if d is None:
            return None
        node = Node(d["text"], d["is_character"])
        if not node.is_character:
            node.yes = Node.from_dict(d.get("yes"))
            node.no = Node.from_dict(d.get("no"))
        return node


class KnowledgeBase:
    def __init__(self):
        self.filename = DB_FILENAME

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Node.from_dict(data)

        root = Node("Ваш персонаж реальный человек?")

        root.yes = Node("Ваш персонаж мужчина?")
        root.yes.yes = Node("Он связан с Ютубом или блогерством?")
        root.yes.yes.yes = Node("Это русскоязычный блогер/стример?")
        root.yes.yes.yes.yes = Node("Он известен своими летсплеями?")
        root.yes.yes.yes.yes.yes = Node("Куплинов (Kuplinov Play)", True)
        root.yes.yes.yes.yes.no = Node("Влад А4", True)
        root.yes.yes.yes.no = Node("У него самый популярный канал на Ютубе в мире?")
        root.yes.yes.yes.no.yes = Node("MrBeast (Мистер Бист)", True)
        root.yes.yes.yes.no.no = Node("IShowSpeed", True)

        root.yes.yes.no = Node("Он профессиональный спортсмен?")
        root.yes.yes.no.yes = Node("Он играет в футбол?")
        root.yes.yes.no.yes.yes = Node("Лионель Месси", True)
        root.yes.yes.no.yes.no = Node("Конор Макгрегор", True)
        root.yes.yes.no.no = Node("Он занимается технологиями или миллиардер?")
        root.yes.yes.no.no.yes = Node("Илон Маск", True)
        root.yes.yes.no.no.no = Node("Этот мужчина актер кино?")
        root.yes.yes.no.no.no.yes = Node("Райан Гослинг", True)
        root.yes.yes.no.no.no.no = Node("Алишер Моргенштерн", True)

        root.yes.no = Node("Она профессионально поет песни (певица)?")
        root.yes.no.yes = Node("Билли Айлиш", True)
        root.yes.no.no = Node("Она имеет отношение к королевской семье?")
        root.yes.no.no.yes = Node("Королева Елизавета II", True)
        root.yes.no.no.no = Node("Мэрилин Монро", True)

        root.no = Node("Этот персонаж из японского аниме?")
        root.no.yes = Node("У него яркие желтые волосы и он хочет стать Хокаге?")
        root.no.yes.yes = Node("Наруто Узумаки", True)
        root.no.yes.no = Node("Этот персонаж — ниндзя в маске, закрывающей пол-лица?")
        root.no.yes.no.yes = Node("Какаши Хатаке", True)
        root.no.yes.no.no = Node("Он обладает силой 'Тетради смерти'?")
        root.no.yes.no.no.yes = Node("Ягами Лайт", True)
        root.no.yes.no.no.no = Node("Леви Аккерман (Атака Титанов)", True)

        root.no.no = Node("Этот персонаж изначально из компьютерной игры?")
        root.no.no.yes = Node("Это культовый водопроводчик в красной кепке?")
        root.no.no.yes.yes = Node("Марио", True)
        root.no.no.yes.no = Node("Это суровый ведьмак с двумя мечами за спиной?")
        root.no.no.yes.no.yes = Node("Геральт из Ривии", True)
        root.no.no.yes.no.no = Node("Он квадратный и состоит из блоков?")
        root.no.no.yes.no.no.yes = Node("Стив (Minecraft)", True)
        root.no.no.yes.no.no.no = Node("Кратос (God of War)", True)

        root.no.no.no = Node("Он из мультфильма?")
        root.no.no.no.yes = Node("Он большой, зеленый и живет на болоте?")
        root.no.no.no.yes.yes = Node("Шрек", True)
        root.no.no.no.yes.no = Node("Это желтая губка, которая живет на дне океана?")
        root.no.no.no.yes.no.yes = Node("Губка Боб Квадратные Штаны", True)
        root.no.no.no.yes.no.no = Node("Это говорящий пес, который расследует мистику?")
        root.no.no.no.yes.no.no.yes = Node("Скуби-Ду", True)
        root.no.no.no.yes.no.no.no = Node("Молния Маккуин (Тачки)", True)

        root.no.no.no.no = Node("Это супергерой в костюме красно-синего цвета?")
        root.no.no.no.no.yes = Node("Человек-Паук (Питер Паркер)", True)
        root.no.no.no.no.no = Node("Это мальчик со шрамом в виде молнии?")
        root.no.no.no.no.no.yes = Node("Гарри Поттер", True)
        root.no.no.no.no.no.no = Node("Это круглый хлеб из сказки?")
        root.no.no.no.no.no.no.yes = Node("Колобок", True)
        root.no.no.no.no.no.no.no = Node("Бэтмен (Брюс Уэйн)", True)

        self.save(root)
        return root

    def save(self, root_node):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(root_node.to_dict(), f, ensure_ascii=False, indent=4)