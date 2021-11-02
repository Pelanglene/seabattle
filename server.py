import socket

host = ""
port = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
print("socket binded to port", port)
clients = []


def get_client(addr):
    if addr == clients[0]:
        return 0
    return 1


def send_player_cell(num, data):
    s.sendto(str(data).encode('ascii'), clients[num])


def wait_players():
    counter = 0
    while counter < 2:
        s.settimeout(None)
        data, addr = s.recvfrom(1024)
        counter += 1
        clients.append(addr)
        print(addr, 'connected')
    s.sendto('1'.encode('ascii'), clients[0])
    s.sendto('1'.encode('ascii'), clients[1])


def get_maps(num):
    field = [0, 0]
    for i in range(2):
        data, addr = s.recvfrom(1024)
        field[get_client(addr) ^ 1] = data
    s.sendto('1'.encode('ascii'), clients[num])
    s.sendto('0'.encode('ascii'), clients[num ^ 1])
    s.sendto(field[0], clients[0])
    s.sendto(field[1], clients[1])


def get_player_cell():
    data, addr = s.recvfrom(1024)
    data.decode('ascii')
    return int(data), get_client(addr)