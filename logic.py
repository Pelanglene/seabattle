import server
import random


def game():
    server.wait_players()
    server.get_maps(random.randint(0, 1))
    last = 100
    while last != -1:
        last, num = server.get_player_cell()
        if last != -1:
            server.send_player_cell(num ^ 1, last)
    server.get_player_cell()


while True:
    game()