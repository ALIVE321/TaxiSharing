import numpy as np
from utils import ABS, visualize
from path_enum import *
from prune import rank_angle, rank_dist

A = ABS(r"F:\files\CLS-algorithm_design\final\Project-Data-Code")
opt = [0, 16238.686025, 22143.401350, 23042.185038, 10417.087363, 16918.735420, 13903.357405, 13350.400109, 19324.210062, 15757.836315, 33871.153866]

def main(k):
    res = []
    for case_id, case_dict in enumerate(A.cases):
        case_id += 1
        if case_id > 5:
            case = [
                [case_dict['经度.6'], case_dict['纬度.6'], case_dict['所在link'], case_dict['ratio.6']],
                [case_dict['经度'], case_dict['纬度'], case_dict['邻近link'], case_dict['ratio']],
                [case_dict['经度.2'], case_dict['纬度.2'], case_dict['邻近link.2'], case_dict['ratio.2']],
                [case_dict['经度.4'], case_dict['纬度.4'], case_dict['邻近link.4'], case_dict['ratio.4']],
                [case_dict['经度.1'], case_dict['纬度.1'], case_dict['邻近link.1'], case_dict['ratio.1']],
                [case_dict['经度.3'], case_dict['纬度.3'], case_dict['邻近link.3'], case_dict['ratio.3']],
                [case_dict['经度.5'], case_dict['纬度.5'], case_dict['邻近link.5'], case_dict['ratio.5']],
            ]
            node_map = node_map_triple
            rank_k = k
        else:
            case = [
                [case_dict['经度.6'], case_dict['纬度.6'], case_dict['所在link'], case_dict['ratio.6']],
                [case_dict['经度'], case_dict['纬度'], case_dict['邻近link'], case_dict['ratio']],
                [case_dict['经度.2'], case_dict['纬度.2'], case_dict['邻近link.2'], case_dict['ratio.2']],
                [case_dict['经度.1'], case_dict['纬度.1'], case_dict['邻近link.1'], case_dict['ratio.1']],
                [case_dict['经度.3'], case_dict['纬度.3'], case_dict['邻近link.3'], case_dict['ratio.3']],
            ]
            node_map = node_map_double
            rank_k = k
        # import pdb
        # pdb.set_trace()
        paths = enum_path(case)
        paths_case = [[case[i] for i in path_ids] for path_ids in paths]
        dists = []
        A.empty_cache()

        # paths_indices = rank_angle(paths_case, rank_k, "hybrid")
        paths_indices = rank_dist(paths_case, rank_k)

        for i, path in enumerate(paths_case):
            if i not in paths_indices:
                dists.append(99999999999999)
            else:
                dists.append(A.path_dist(path))
        idx = np.argmin(dists)
        print("| {:2d} | {} | ${}$ | {:.2f} | {:3d} | {:3.2f}% |".format(case_id,  "三拼" if case_id > 5 else "双拼",
                    "".join([node_map[i] for i in paths[idx]]), dists[idx], A.lookup_times, dists[idx] / opt[case_id] * 100))
        res.append((A.lookup_times, dists[idx] / opt[case_id] * 100))
        visualize(case, paths[idx], "prune_enum/case{:02d}".format(case_id))
    return sum([i[0] for i in res]) / len(res), sum([i[1] for i in res]) / len(res)


main(1)
# for i in range(1, 9):
#     x, y = main(i)
#     print("{}\t{:.2f}".format(x, y))

