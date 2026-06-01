import tkinter as tk


class AkinatorView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("Akinator")
        self.root.geometry("850x500")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=850, height=500, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        for i in range(500):
            r = int(14 + 27 * (i / 500))
            g = int(33 + 95 * (i / 500))
            b = int(70 + 115 * (i / 500))
            self.canvas.create_line(0, i, 850, i, fill=f"#{r:02x}{g:02x}{b:02x}")

        frame_left = tk.Frame(self.canvas, bg="#0e2146", bd=0)
        self.canvas.create_window(160, 440, window=frame_left, width=280, height=60)
        self.bubble = tk.Label(frame_left, text="Загадывайте! Я готов.", font=("Arial", 11, "bold italic"),
                               fg="#f1c40f", bg="#112754", bd=1, relief="groove")
        self.bubble.pack(fill="both", expand=True)

        frame_right = tk.Frame(self.canvas, bg="#ffffff", padx=25, pady=20)
        self.canvas.create_window(580, 240, window=frame_right, width=420, height=420)

        self.lbl_step = tk.Label(frame_right, text="ВОПРОС №1", font=("Arial", 10, "bold"), fg="#7f8c8d", bg="#ffffff")
        self.lbl_step.pack(anchor="w", pady=(0, 5))

        self.lbl_text = tk.Label(frame_right, text="", font=("Arial", 14, "bold"), fg="#1e272e", bg="#ffffff",
                                 wraplength=370, justify="left", height=3, anchor="nw")
        self.lbl_text.pack(fill="x", pady=(0, 10))

        self.btn_area = tk.Frame(frame_right, bg="#ffffff")
        self.btn_area.pack(fill="x", expand=True)

        self.b_yes = tk.Button(self.btn_area, text="Да", font=("Arial", 11, "bold"), bg="#1b9cfc", fg="#ffffff",
                               relief="flat", height=2, command=lambda: self.controller.handle_answer(True))
        self.b_yes.pack(fill="x", pady=2)

        self.b_no = tk.Button(self.btn_area, text="Нет", font=("Arial", 11, "bold"), bg="#1b9cfc", fg="#ffffff",
                              relief="flat", height=2, command=lambda: self.controller.handle_answer(False))
        self.b_no.pack(fill="x", pady=2)

        self.b_dont_know = tk.Button(self.btn_area, text="Я не знаю", font=("Arial", 10, "bold"), bg="#f1f2f6",
                                     fg="#57606f", relief="flat", command=self.controller.skip_question)
        self.b_dont_know.pack(fill="x", pady=2)

        self.b_maybe = tk.Button(self.btn_area, text="Возможно Частично", font=("Arial", 10, "bold"), bg="#f1f2f6",
                                 fg="#57606f", relief="flat", command=self.controller.skip_question)
        self.b_maybe.pack(fill="x", pady=2)

        self.b_probably_not = tk.Button(self.btn_area, text="Скорее нет Не совсем", font=("Arial", 10, "bold"),
                                        bg="#f1f2f6", fg="#57606f", relief="flat",
                                        command=lambda: self.controller.handle_answer(False))
        self.b_probably_not.pack(fill="x", pady=2)

        self.b_restart = tk.Button(frame_right, text="Начать игру заново ↻", font=("Arial", 9, "bold"), bg="#ffffff",
                                   fg="#e74c3c", relief="flat", command=self.controller.restart_game)
        self.b_restart.pack(side="bottom", fill="x")

    def draw_jinni(self, mood="thinking"):
        self.canvas.delete("j")
        cx = 160
        self.canvas.create_oval(cx - 40, 380, cx + 40, 410, fill="#d35400", tags="j")
        self.canvas.create_oval(cx - 25, 345, cx + 25, 365, fill="#f1c40f", tags="j")
        self.canvas.create_polygon(cx, 350, cx - 40, 260, cx - 60, 200, cx + 60, 200, cx + 40, 260, fill="#3498db",
                                   tags="j")
        self.canvas.create_oval(cx - 45, 110, cx + 45, 200, fill="#54a0ff", tags="j")
        self.canvas.create_oval(cx - 50, 85, cx + 50, 130, fill="#ffffff", outline="#c0392b", width=2, tags="j")

        if mood == "thinking":
            self.canvas.create_oval(cx - 25, 140, cx - 5, 155, fill="#ffffff", tags="j")
            self.canvas.create_oval(cx + 5, 140, cx + 25, 155, fill="#ffffff", tags="j")
            self.canvas.create_line(cx - 15, 175, cx + 15, 175, fill="#2c3e50", width=2, tags="j")
        elif mood == "confident":
            self.canvas.create_arc(cx - 25, 140, cx - 5, 155, start=0, extent=180, style="arc", width=3, tags="j")
            self.canvas.create_arc(cx + 5, 140, cx + 25, 155, start=0, extent=180, style="arc", width=3, tags="j")
            self.canvas.create_arc(cx - 20, 165, cx + 20, 185, start=180, extent=180, fill="#2c3e50", tags="j")
        elif mood == "shocked":
            self.canvas.create_oval(cx - 25, 135, cx - 5, 155, fill="#ffffff", tags="j")
            self.canvas.create_oval(cx + 5, 135, cx + 25, 155, fill="#ffffff", tags="j")
            self.canvas.create_oval(cx - 8, 170, cx + 8, 186, fill="#2c3e50", tags="j")