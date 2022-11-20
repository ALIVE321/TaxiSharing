node_map_double = ["pc", "p_o^1", "p_o^2", "p_d^1", "p_d^2"]
node_map_triple = ["pc", "p_o^1", "p_o^2", "p_o^3", "p_d^1", "p_d^2", "p_d^3"]

def enum_path(s: list):
    # s: [[W,S,L,R],...]
    stype = len(s)
    if stype == 5:
        _p, _c, paths = [], list(range(1,5)), []
        iter_double(_p, _c, paths)
    elif stype == 7:
        _p, _c, paths, _g = [], list(range(1,7)), [], []
        iter_triple(_p, _c, paths, _g)
    else:
        raise RuntimeError(f"Invalid Length = {stype}")
    return paths

def iter_triple(path: list, cand: list, res: list, guest: list):
    if len(cand) == 0:
        res.append([0] + path.copy())
        return
    for i in cand.copy():
        if (i > 3) and (i - 3 not in path):
            continue
        if (i <= 3):
            guest.append(i)
        else:
            if len(guest) == 1 and len(cand) > 1:
                continue
            else:
                guest.remove(i - 3)
        path.append(i)
        cand.remove(i)
        iter_triple(path, cand, res, guest)
        path.remove(i)
        cand.append(i)
        if (i <= 3):
            guest.remove(i)
        else:
            guest.append(i - 3)

def iter_double(path: list, cand: list, res: list):
    if len(cand) == 0:
        res.append([0] + path.copy())
        return
    for i in cand.copy():
        if (i == 1 or i == 2) or ((i == 3 or i == 4) and 1 in path and 2 in path):
            path.append(i)
            cand.remove(i)
            iter_double(path, cand, res)
            path.remove(i)
            cand.append(i)


if __name__ == "__main__":
    # import pdb
    # pdb.set_trace()
    paths = enum_path([0,1,2,3,4,5,6])
    dists = set()
    for idx, path in enumerate(paths):
        for i, j in zip(path[:-1], path[1:]):
            dists.add((i, j))
        print("| {} | ${}$ | {} |".format(idx + 1, "".join([node_map_triple[i] for i in path]), len(dists)))
