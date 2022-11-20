import numpy as np

_R = 6378.137

def _radius(x: float) -> float:
    return x * np.pi / 180

def ball_dist(long1: float, lat1: float, long2: float, lat2: float) -> float:
    a = np.sin((_radius(lat1) - _radius(lat2)) / 2) ** 2
    b = np.sin(_radius(long1 - long2) / 2) ** 2
    c = np.cos(lat1) * np.cos(lat2)
    s = 2 * np.arcsin(np.sqrt(a + b * c)) * _R

    return s

def _xyz(long: float, lat: float) -> float:
    a = (np.pi * lat) / 180
    b = (np.pi * long) / 180

    x = _R * np.cos(a) * np.cos(b)
    y = _R * np.cos(a) * np.sin(b)
    z = _R * np.sin(a)

    return x, y, z

def ball_angle( long1: float, lat1: float, 
                long2: float, lat2: float, 
                long3: float, lat3: float) -> float:

    x1, y1, z1 = _xyz(long1, lat1)
    x2, y2, z2 = _xyz(long2, lat2)
    x3, y3, z3 = _xyz(long3, lat3)

    p12 = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    p32 = np.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2 + (z3 - z2) ** 2)

    p = (x1 - x2) * (x3 - x2) + (y1 - y2) * (y3 - y2) + (z1 - z2) * (z3 - z2)
    angle = np.arccos(p / (p12 * p32)) / np.pi * 180

    return angle


if __name__ == "__main__":
    print(ball_dist(116.4, 39.9, 114.3, 30.5))
    print(ball_angle(10, 11, 11, 11, 11, 12))
