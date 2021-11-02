# половина кода - пробелы и этот коммент
from tkinter import *
from tkinter import messagebox
import checker
import client_sock
import time
import make_ships

SQ_SIZE = 40
pl_map = ['*'] * 100
en_map = []
state = num = 0

client_sock.window.geometry("225x175")
# client_sock.window.iconbitmap(r"C:\Py37\DLLs\py.ico")
client_sock.window.title("SeaBattle")
c = Canvas(client_sock.window)
c2 = Canvas(client_sock.window)
lb = Label(client_sock.window)
lb_ban = Label(client_sock.window)
lb_nab = Label(client_sock.window)
my_tag = en_tag = []
winner = 2
button1 = button2 = Button(client_sock.window)
my_boat_pos = my_boat_h = my_boats = en_boat_pos = en_boat_h = en_boats = []
my_health = en_health = 10


def state1():
    global state, c, button, num
    state = 1
    button['state'] = DISABLED
    messagebox.showinfo("SeaBattle: подбор игрока", "Привет. Скоро мы подберем тебе соперника, после чего ты"
                                                    "сможешь приступить к расстановке кораблей. Когда соперник"
                                                    "будет подобран, мы оповестим тебя.")
    client_sock.start()

    button.destroy()
    rules.destroy()
    button = Button(client_sock.window, text="Продолжить", width=15, height=3, command=state2)
    button.place(x=172.5, y=450)

    client_sock.window.geometry("475x550")
    c = Canvas(client_sock.window, width=SQ_SIZE * 10, height=SQ_SIZE * 10, bg="white")
    c.place(x=30, y=30)

    for i in range(10):
        for j in range(10):
            my_tag.append(c.create_rectangle(j * SQ_SIZE, i * SQ_SIZE,
                                             j * SQ_SIZE + SQ_SIZE,
                                             i * SQ_SIZE + SQ_SIZE, fill="#0070A0"))
    messagebox.showinfo("SeaBattle: расстановка кораблей", "    Привет снова. Надеюсь, ты ждал не очень долго и без "
                                                           "происшествий :)\n\n    Клетки можно заполнять частями "
                                                           "корабля, нажимая на них левой клавишей мыши. Удалять "
                                                           "часть - правой. Корабли представляют собой строку или "
                                                           "столбец, размером Nx1 и 1xN соответственно. Какие "
                                                           "корабли могут быть по размерам и количеству:\n\n    1. "
                                                           "Одноклеточные корабли (1x1), 4 корабля,"
                                                           "\n    2. Двуклеточные корабли (2x1), 3 корабля,"
                                                           "\n    3. Трёхклеточные корабли (3x1), 2 корабля,"
                                                           "\n    4. Четырёхклеточный корабль (4x1), 1 корабль.\n\n"
                                                           "    Корабли не должны пересекаться и(или) всячески "
                                                           "изгибаться. Всё абсолютно как в классическом морском бое. "
                                                           "Теперь ты можешь начинать создавать флот :) Когда "
                                                           "закончишь - нажимай на кнопку \"Продолжить\"")

    c.bind("<Button-1>", l_click)
    c.bind("<Button-3>", r_click)


def state2():
    if not checker.check_field(pl_map):
        messagebox.showwarning("SeaBattle: расстановка кораблей", "Привет. Построенная карта кораблей является "
                                                                  "неправильной, так как какое-то из правил не было "
                                                                  "соблюдено:\n\n    1. Размеры кораблей не "
                                                                  "соблюдены\n "
                                                                  "  2. Количество кораблей отлично от 10\n    3. "
                                                                  "Корабли прикосаются друг к другу\n    4. Корабли "
                                                                  "неверной формы\n\nНапоминаю размеры и количество "
                                                                  "кораблей:\n\n    1. "
                                                                  "Одноклеточные корабли (1x1), 4 корабля,"
                                                                  "\n    2. Двуклеточные корабли (2x1), 3 корабля,"
                                                                  "\n    3. Трёхклеточные корабли (3x1), 2 корабля,"
                                                                  "\n    4. Четырёхклеточный корабль (4x1), "
                                                                  "1 корабль.\n\nПерепроверь и исправь своё поле, "
                                                                  "а затем нажми сюда ещё раз.")
        return

    global button, state, c, c2, lb_ban, lb_nab, lb, num
    state = 2
    button['state'] = DISABLED
    messagebox.showinfo("SeaBattle: ожидание игрока", "И ещё раз привет! Ожидай, пока твой соперник не завершит "
                                                      "расстановку своих кораблей и нажмёт на эту же кнопку. После "
                                                      "этого сразу же начнётся игра.")
    global en_map, my_boats, my_boat_h, my_boat_pos, en_boats, en_boat_h, en_boat_pos
    num, en_map = client_sock.wait(pl_map)
    client_sock.window.geometry("1000x550")
    button.destroy()
    my_boats, my_boat_h, my_boat_pos = make_ships.make(pl_map)
    en_boats, en_boat_h, en_boat_pos = make_ships.make(en_map)

    c.place(x=40, y=50)
    c2 = Canvas(client_sock.window, width=SQ_SIZE * 10, height=SQ_SIZE * 10, bg="white")
    c2.place(x=SQ_SIZE * 13, y=50)
    for i in range(10):
        for j in range(10):
            en_tag.append(c2.create_rectangle(j * SQ_SIZE, i * SQ_SIZE,
                                              j * SQ_SIZE + SQ_SIZE,
                                              i * SQ_SIZE + SQ_SIZE, fill="#0070A0"))
    lb['font'] = "Arial 25"
    lb_ban['text'] = "Поле соперника"
    lb_nab['text'] = "Твоё поле"
    lb_nab['font'] = lb_ban['font'] = "Arial 17"
    lb_nab.place(x=52, y=12.5)
    lb_ban.place(x=SQ_SIZE * 13 + 3, y=12.5)

    c2.bind("<Button-1>", fire)
    print_maps()
    global winner, my_health
    while winner == 2:
        if num == 0:
            cell = client_sock.get_cell()
            if pl_map[cell] == '#':
                pl_map[cell] = 'X'
            else:
                pl_map[cell] = '/'
                num = 1
            if pl_map[cell] == 'X':
                my_boat_h[my_boats[cell]] -= 1
                if my_boat_h[my_boats[cell]] == 0:
                    my_health -= 1
                    for i in my_boat_pos[my_boats[cell]]:
                        pl_map[i] = 'D'
                    if my_health == 0:
                        winner = 0
            print_maps()
        client_sock.window.update()
        time.sleep(0.1)
    print_maps()
    lb['text'] = "Победил игрок {}!".format("слева" if winner == 1 else "справа")
    lb.place(x=300, y=475)
    if winner == 1:
        messagebox.showinfo("SeaBattle: конец игры", "Короче, ты выиграл, красава.\n\nСейчас появятся две кнопки, "
                                                     "нажав на первую из них тебя кинет на стартовый экран, а на вторую - выход "
                                                     "из игры.")
    else:
        messagebox.showinfo("SeaBattle: конец игры", "Короче, ты проиграл, но все равно красава.\n\nСейчас появятся "
                                                     "две кнопки, нажав на первую из них тебя кинет на стартовый экран, "
                                                     "а на вторую - выход из игры.")
    global button1, button2
    button1 = Button(client_sock.window, text="Старт", width=11, height=2, command=to_start)
    button2 = Button(client_sock.window, text="Выход", width=11, height=2, command=leave)
    button1.place(x=700, y=483)
    button2.place(x=790, y=483)


def l_click(event):
    idx = c.find_withtag(CURRENT)[0]
    if state == 1:
        pl_map[idx - 1] = '#'
        c.itemconfig(CURRENT, fill="#12CE10")
    c.update()


def r_click(event):
    idx = c.find_withtag(CURRENT)[0]
    if state == 1:
        pl_map[idx - 1] = '*'
        c.itemconfig(CURRENT, fill="#0070A0")
    c.update()


def fire(event):
    global num, winner, en_boat_h, en_health, en_boat_pos, en_boats
    idx = c2.find_withtag(CURRENT)[0] - 1
    if state == 2 and num == 1:
        if en_map[idx] in ['X', 'D', '/']:
            messagebox.showwarning("SeaBattle: игра", "Привет. Выбранная клетка уже была посещена раннее. Походи "
                                                      "ещё раз, но только в ту клетку, которая ещё не была посещена.")
        else:
            client_sock.send_cell(idx)
            if en_map[idx] == '*':
                en_map[idx] = '/'
                num ^= 1
            else:
                en_map[idx] = 'X'
                en_boat_h[en_boats[idx]] -= 1
                if en_boat_h[en_boats[idx]] == 0:
                    en_health -= 1
                    for i in en_boat_pos[en_boats[idx]]:
                        en_map[i] = 'D'
                    if en_health == 0:
                        winner = 1
            print_maps()


def print_maps():
    col = "kek"
    global lb, num
    for i in range(10):
        for j in range(10):
            if pl_map[i * 10 + j] == '*':
                col = "#0070A0"
            if pl_map[i * 10 + j] == '/':
                col = "#004070"
            if pl_map[i * 10 + j] == 'X':
                col = "#1E9410"
            if pl_map[i * 10 + j] == 'D':
                col = "#CC0605"
            if pl_map[i * 10 + j] == '#':
                col = "#12CE10"
            c.itemconfig(my_tag[i * 10 + j], fill=col)
    for i in range(10):
        for j in range(10):
            if en_map[i * 10 + j] == '/':
                col = "#004070"
            elif en_map[i * 10 + j] == 'X':
                col = "#1E9410"
            elif en_map[i * 10 + j] == 'D':
                col = "#CC0605"
            else:
                if winner == 2:
                    col = "#0070A0"
                else:
                    if en_map[i * 10 + j] == '*':
                        col = "#0070A0"
                    else:
                        col = "#12CE10"
            c2.itemconfig(en_tag[i * 10 + j], fill=col)
    if winner == 2:
        if num == 1:
            lb.place(x=50, y=470)
            lb['text'] = "Твой ход"
        else:
            lb.place(x=SQ_SIZE * 13 + 10, y=470)
            lb['text'] = "Ход соперника"


def leave():
    exit(0)


def to_start():
    global button1, button2, button, pl_map, state, num, c, c2, lb, lb_ban, lb_nab, my_health, en_health
    global my_tag, en_tag, winner, rules, en_boat_pos, en_boat_h, en_boats, my_boat_pos, my_boat_h, my_boats
    button1.destroy()
    button2.destroy()
    pl_map = ['*'] * 100
    state = num = 0
    my_health = en_health = 10

    client_sock.window.geometry("225x175")
    c.destroy()
    c2.destroy()
    lb.destroy()
    lb_ban.destroy()
    lb_nab.destroy()
    button.destroy()
    c = Canvas(client_sock.window)
    c2 = Canvas(client_sock.window)
    lb = Label(client_sock.window)
    lb_ban = Label(client_sock.window)
    lb_nab = Label(client_sock.window)
    my_tag = en_tag = en_boat_pos = en_boat_h = en_boats = my_boat_pos = my_boat_h = my_boats = []
    winner = 2
    button = Button(client_sock.window, text="Начать игру", width=15, height=3, command=state1)
    button.place(x=50, y=50)
    rules = rules = Button(client_sock.window, text="Правила игры", width=15, height=3,
                           command=lambda: messagebox.showinfo("SeaBattle: правила игры",
                                                               "Привет! Ты решил почитать правила игры. "
                                                               "Когда игра начнётся, справа ты сможешь увидеть поле "
                                                               "соперника, слева своё. "
                                                               "Естественно, с самого начала игры ты не сможешь "
                                                               "увидеть корабли соперника, так же как и "
                                                               "сопреник твои. Чтобы выстрелить в поле соперника, "
                                                               "нажми левой клавишей мыши на то поле, на "
                                                               "которое желаешь. Ествественно, все выстрелы "
                                                               "необходимо совершать по "
                                                               "очереди. После выстрела по полю с кораблём, "
                                                               "оно станет тёмно-зелёным. "
                                                               "Если там ничего не было, оно станет тёмно-синим. А "
                                                               "если мы убили корабль "
                                                               "противника, весь корабль станет красным. Тоже самое и "
                                                               "на твоём "
                                                               "поле. В случае, если игрок попадает на поле с "
                                                               "кораблём, ход сопернику не передаётся, а он ходит ещё "
                                                               "раз.\n\nЭто всё. Удачи :)"))
    rules.place(x=50, y=90)


button = Button(client_sock.window, text="Начать игру", width=15, height=3, command=state1)
button.place(x=50, y=30)
rules = Button(client_sock.window, text="Правила игры", width=15, height=3,
               command=lambda: messagebox.showinfo("SeaBattle: правила игры", "Привет! Ты решил почитать правила игры. "
                                                                              "Когда игра начнётся, справа ты сможешь "
                                                                              "увидеть поле соперника, слева своё. "
                                                                              "Естественно, с самого начала игры ты "
                                                                              "не сможешь увидеть корабли соперника, "
                                                                              "так же как и "
                                                                              "сопреник твои. Чтобы выстрелить в поле "
                                                                              "соперника, нажми левой клавишей мыши "
                                                                              "на то поле, на "
                                                                              "которое желаешь. Ествественно, все "
                                                                              "выстрелы необходимо совершать по "
                                                                              "очереди. После выстрела по полю с "
                                                                              "кораблём, оно станет тёмно-зелёным. "
                                                                              "Если там ничего не было, оно станет "
                                                                              "тёмно-синим. А если мы убили корабль "
                                                                              "противника, весь корабль станет "
                                                                              "красным. Тоже самое и на твоём "
                                                                              "поле. В случае, если игрок попадает на "
                                                                              "поле с кораблём, ход сопернику не "
                                                                              "передаётся, а он ходит ещё раз.\n\nЭто "
                                                                              "всё. Удачи :)"))
rules.place(x=50, y=90)

client_sock.window.mainloop()
