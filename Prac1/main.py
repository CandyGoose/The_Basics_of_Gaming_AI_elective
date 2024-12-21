import numpy as np
from tkinter import *
import tkinter.messagebox
from ai import AI


class Game:
    def __init__(self):
        self.ai = AI(15, 15)
        self.chess = np.zeros((15, 15), dtype=int)
        self.isAI = True

        self.root = Tk()
        self.root.title('Игра: 5 в ряд')
        self.canvas = Canvas(self.root, width=650, height=650, bg="white")
        self.canvas.pack()
        self.canvas.create_rectangle(25, 25, 625, 625, fill="#CA9762")
        for i in range(1, 16):
            self.canvas.create_line(25, 25 + 40 * (i - 1), 625, 25 + 40 * (i - 1))
            self.canvas.create_line(25 + 40 * (i - 1), 25, 25 + 40 * (i - 1), 625)
        self.canvas.bind("<Button-1>", self.player)
        self.root.mainloop()

    def drawBlack(self, i, j):
        x = 25 + 40 * j
        y = 25 + 40 * i
        self.canvas.create_oval(x, y, x + 40, y + 40, fill="#000000")

    def drawWhite(self, i, j):
        x = 25 + 40 * j
        y = 25 + 40 * i
        self.canvas.create_oval(x, y, x + 40, y + 40, fill="#FFFFFF")

    def player(self, event):
        y = event.y
        x = event.x
        if self.isAI and (25 <= x <= 625) and (25 <= y <= 625):
            i = int((y - 25) / 40)
            j = int((x - 25) / 40)
            if not self.ai.is_ended:
                if not self.ai.isValid(i, j):
                    tkinter.messagebox.showerror(title='Ошибка', message='Выберите свободную клетку')
                else:
                    self.ai.put(i, j, 1)
                    self.drawBlack(i, j)

                    if self.ai.isMaxWin():
                        self.ai.end()
                        tkinter.messagebox.showinfo(title='Конец игры', message='Вы выиграли!')
                    else:
                        if self.ai.is_ended:
                            tkinter.messagebox.showinfo(title='Конец игры', message='Ничья')
                        else:
                            res = self.ai.min(2)
                            self.ai.put(res["row"], res["column"], 2)
                            self.drawWhite(res["row"], res["column"])

                            if self.ai.isMinWin():
                                self.ai.end()
                                tkinter.messagebox.showinfo(title='Конец игры', message='Вы проиграли')


if __name__ == '__main__':
    Game()
