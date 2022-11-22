from utils import ABS
from ball import ball_dist, ball_angle

def rank_angle(paths: list, k: int, mode: str = "hybrid") -> list:
    assert mode in ["min", "ave", "hybrid"], mode
    angles = []
    for path in paths:
        if mode == "min":
            angle = 180
        elif mode == "ave":
            angle = 0
        elif mode == "hybrid":
            angle = [180, 0]
        for i in range(len(path) - 2):
            ang = ball_angle(*path[i][:2], *path[i+1][:2], *path[i+2][:2])
            if mode == "min":
                angle = min(angle, ang)
            elif mode == "ave":
                angle += ang
            elif mode == "hybrid":
                angle[0] = min(ang, angle[0])
                angle[1] += ang / (len(path) - 2)
        if mode == "hybrid":
            angle = angle[0] + angle[1]
        angles.append(angle)
    indices = sorted([i for i in range(len(angles))], key=lambda i: -angles[i])
    return indices[:k]

def rank_dist(paths: list, k: int) -> list:
    dists = []
    for path in paths:
        dist = 0
        for i in range(len(path) - 1):
            d = ball_dist(*path[i][:2], *path[i+1][:2])
            dist += d
        dists.append(dist)
    indices = sorted([i for i in range(len(dists))], key=lambda i: dists[i])
    return indices[:k]


def rank_choices(A: ABS, last_node: tuple, next_node: tuple, choices: list, k: int) -> list:
    dists = []

    for choice in choices:
        link = choice[2]
        link_start = [A.link_data[link-1][2], A.link_data[link-1][3]]
        link_end = [A.link_data[link-1][5], A.link_data[link-1][6]]
        d = ball_dist(*link_start, *last_node)
        if next_node is not None:
            d += ball_dist(*link_end, *next_node)
        dists.append(d)

    indices = sorted([i for i in range(len(choices))], key=lambda i: dists[i])
    return indices[:k]

