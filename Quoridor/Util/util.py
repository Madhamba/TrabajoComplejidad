from math import cos, sin, pi
from random import randint


# Rotates clockwise
def rotate(x, y, theta, c):
    x, y = x - c[0], y - c[1]

    _x = round(x * cos(theta * pi / 180) - y * sin(theta * pi / 180))
    _y = round(x * sin(theta * pi / 180) + y * cos(theta * pi / 180))

    x, y = c[0] + _x, c[1] + _y

    return x, y


def random_color():
    return randint(0, 254), randint(0, 254), randint(0, 254)


def get_player_opponent(player, players):
    i_player = None
    for identity in players:
        if players[identity] == player:
            i_player = identity

    if len(players) == 4:
        return players[(i_player + len(players) // 2) % len(players)]
    else:
        if i_player == 0:
            return players[2]
        else:
            return players[0]
