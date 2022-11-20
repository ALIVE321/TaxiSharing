import numpy as np
from utils import ABS, visualize
from path_enum import *

A = ABS(r"F:\files\CLS-algorithm_design\final\Project-Data-Code")
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
    else:
        case = [
            [case_dict['经度.6'], case_dict['纬度.6'], case_dict['所在link'], case_dict['ratio.6']],
            [case_dict['经度'], case_dict['纬度'], case_dict['邻近link'], case_dict['ratio']],
            [case_dict['经度.2'], case_dict['纬度.2'], case_dict['邻近link.2'], case_dict['ratio.2']],
            [case_dict['经度.1'], case_dict['纬度.1'], case_dict['邻近link.1'], case_dict['ratio.1']],
            [case_dict['经度.3'], case_dict['纬度.3'], case_dict['邻近link.3'], case_dict['ratio.3']],
        ]
        node_map = node_map_double
    # import pdb
    # pdb.set_trace()
    paths = enum_path(case)
    dists = []
    A.empty_cache()
    for path_ids in paths:
        path = [case[i] for i in path_ids]
        dists.append(A.path_dist(path))
    idx = np.argmin(dists)
    print("| {:2d} | {} | ${}$ | {:.2f} | {:3d} |".format(case_id, "三拼" if case_id > 5 else "双拼", 
                "".join([node_map[i] for i in paths[idx]]), dists[idx], A.lookup_times))
    # print("{:.6f},".format(dists[idx]), end=" ")
    visualize(case, paths[idx], "enum/case{:02d}".format(case_id))

