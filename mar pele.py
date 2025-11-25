import tkinter as tk
import random

snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class SnakeLadderGame:
    def __init__(self, master):
        self.master = master
        self.master.title("بازی مار و پله")

        self.canvas = tk.Canvas(master, width=600, height=600, bg='white')
        self.canvas.pack()

        self.name_frame = tk.Frame(master)
        self.name_frame.pack(pady=10)

        tk.Label(self.name_frame, text="نام بازیکن اول:").grid(row=0, column=0)
        self.name1_entry = tk.Entry(self.name_frame)
        self.name1_entry.grid(row=0, column=1)

        tk.Label(self.name_frame, text="نام بازیکن دوم:").grid(row=1, column=0)
        self.name2_entry = tk.Entry(self.name_frame)
        self.name2_entry.grid(row=1, column=1)

        self.start_button = tk.Button(master, text="شروع بازی", command=self.start_game)
        self.start_button.pack(pady=5)

        self.roll_button = tk.Button(master, text="پرتاب تاس", command=self.roll_dice,
                                     font=('Arial', 14), state='disabled')
        self.roll_button.pack(pady=10)

        self.info = tk.Label(master, text="", font=('Arial', 14))
        self.info.pack()

        self.board = {}
        self.draw_board()
        self.draw_snakes_ladders()

        self.players = {}
        self.positions = {}
        self.turn = 0

    def start_game(self):
        name1 = self.name1_entry.get()
        name2 = self.name2_entry.get()
        if not name1 or not name2:
            self.info.config(text="لطفاً نام هر دو بازیکن را وارد کنید.")
            return

        self.name_frame.destroy()
        self.start_button.destroy()

        self.players = {0: name1, 1: name2}
        self.positions = {0: 1, 1: 1}

        self.player_tokens = {
            0: self.canvas.create_oval(10, 550, 30, 570, fill="blue"),
            1: self.canvas.create_oval(30, 550, 50, 570, fill="red")
        }

        self.roll_button.config(state='normal')
        self.info.config(text=f"{self.players[self.turn]} نوبت شماست.")

    def draw_board(self):
        size = 60
        num = 100
        for row in range(10):
            for col in range(10):
                x = col * size if row % 2 == 0 else (9 - col) * size
                y = 540 - row * size
                self.board[num] = (x + 10, y + 10)
                self.canvas.create_rectangle(x, y, x + size, y + size, outline="black")
                self.canvas.create_text(x + 30, y + 30, text=str(num), font=('Arial', 10))
                num -= 1

    def draw_snakes_ladders(self):
        for start, end in snakes.items():
            x1, y1 = self.board[start]
            x2, y2 = self.board[end]
            self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10,
                                    fill="pink", width=4, arrow="last")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="مار",
                                    fill="pink", font=('Arial', 10, 'bold'))

        for start, end in ladders.items():
            x1, y1 = self.board[start]
            x2, y2 = self.board[end]
            self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10,
                                    fill="pink", width=4, arrow="last")
            self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="نردبان",
                                    fill="pink", font=('Arial', 10, 'bold'))

    def roll_dice(self):
        dice = random.randint(1, 6)
        current = self.turn
        name = self.players[current]

        pos = self.positions[current] + dice
        if pos > 100:
            pos = self.positions[current]

        if pos in snakes:
            pos = snakes[pos]
        elif pos in ladders:
            pos = ladders[pos]

        self.positions[current] = pos
        self.update_player(current)

        if pos == 100:
            self.info.config(text=f"🎉 {name} برنده شد!")
            self.roll_button.config(state='disabled')
        else:
            self.turn = 1 - self.turn
            self.info.config(text=f"{self.players[self.turn]} نوبت شماست. (تاس: {dice})")

    def update_player(self, player):
        x, y = self.board[self.positions[player]]
        offset = -10 if player == 0 else 10
        self.canvas.coords(self.player_tokens[player],
                           x + offset, y - 10, x + offset + 20, y + 10)


root = tk.Tk()
game = SnakeLadderGame(root)
root.mainloop()
