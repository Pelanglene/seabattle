import socket
import select
import time
import tkinter

window = tkinter.Tk()
host = '127.0.0.1'
port = 12346
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = (host, port)
s.connect(server)

is_player_moved = 0


def up_while_not_data():
    ready = select.select([s], [], [], 0.1)
    while not ready[0]:
        window.update()
        ready = select.select([s], [], [], 0.1)


def wait(my_map):
    s.sendto(str(my_map).encode('ascii'), server)
    up_while_not_data()
    num, addr = s.recvfrom(1024)
    data, addr = s.recvfrom(1024)
    num.decode('ascii')
    data.decode('ascii')
    data = eval(data)
    return int(num), data


def start():
    send_cell('1'.encode('ascii'))
    up_while_not_data()
    data = s.recvfrom(1024)


def get_cell():
    up_while_not_data()
    data, addr = s.recvfrom(1024)
    data.decode('ascii')
    return int(data)


def send_cell(data):
    s.sendto(str(data).encode('ascii'), server)