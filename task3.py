import numpy as np
from tqdm import tqdm
from utils import *
from path_enum import *
from prune import *

A = ABS(r"F:\files\CLS-algorithm_design\final\Project-Data-Code")
for case_id, case_dict in enumerate(A.cases):
    case_id += 1
    if case_id not in [1, 6]:
        continue
    if case_id > 5:
        case = [    # pc, po1, po2, po3, pd1, pd2, pd3
            [case_dict['经度.6'], case_dict['纬度.6'], case_dict['所在link'], case_dict['ratio.6']],
            [case_dict['经度'], case_dict['纬度'], case_dict['邻近link'], case_dict['ratio']],
            [case_dict['经度.2'], case_dict['纬度.2'], case_dict['邻近link.2'], case_dict['ratio.2']],
            [case_dict['经度.4'], case_dict['纬度.4'], case_dict['邻近link.4'], case_dict['ratio.4']],
            [case_dict['经度.1'], case_dict['纬度.1'], case_dict['邻近link.1'], case_dict['ratio.1']],
            [case_dict['经度.3'], case_dict['纬度.3'], case_dict['邻近link.3'], case_dict['ratio.3']],
            [case_dict['经度.5'], case_dict['纬度.5'], case_dict['邻近link.5'], case_dict['ratio.5']],
        ]
        choices = [ # po1, po2, po3, pd1, pd2, pd3
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度']), eval(case_dict['邻近link.6']), eval(case_dict['ratio.7']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.2']), eval(case_dict['邻近link.8']), eval(case_dict['ratio.9']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.4']), eval(case_dict['邻近link.10']), eval(case_dict['ratio.11']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.1']), eval(case_dict['邻近link.7']), eval(case_dict['ratio.8']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.3']), eval(case_dict['邻近link.9']), eval(case_dict['ratio.10']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.5']), eval(case_dict['邻近link.11']), eval(case_dict['ratio.12']))],
        ]
        node_map = node_map_triple
        visualize = visualize_choices_triple
        opt = 11977.745265270445
        rank_N = 1
        rank_k = 2
    else:
        case = [    # pc, po1, po2, pd1, pd2
            [case_dict['经度.6'], case_dict['纬度.6'], case_dict['所在link'], case_dict['ratio.6']],
            [case_dict['经度'], case_dict['纬度'], case_dict['邻近link'], case_dict['ratio']],
            [case_dict['经度.2'], case_dict['纬度.2'], case_dict['邻近link.2'], case_dict['ratio.2']],
            [case_dict['经度.1'], case_dict['纬度.1'], case_dict['邻近link.1'], case_dict['ratio.1']],
            [case_dict['经度.3'], case_dict['纬度.3'], case_dict['邻近link.3'], case_dict['ratio.3']],
        ]
        choices = [ # po1, po2, pd1, pd2
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度']), eval(case_dict['邻近link.6']), eval(case_dict['ratio.7']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.2']), eval(case_dict['邻近link.8']), eval(case_dict['ratio.9']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.1']), eval(case_dict['邻近link.7']), eval(case_dict['ratio.8']))],
            [[*i[0], i[1], i[2]] for i in zip(eval(case_dict['经纬度.3']), eval(case_dict['邻近link.9']), eval(case_dict['ratio.10']))],
        ]
        node_map = node_map_double
        visualize = visualize_choices_double
        opt = 13506.873184310927
        rank_N = 1
        rank_k = 4

    paths = enum_path(case)
    A.empty_cache()
    min_dist_info = [9999999, [-1 for _ in choices], None]

    def dfs(path: list, n: int, record: list, choices: list, min_dist_info: list):
        # print(n,)
        if n == len(choices):
            d = A.path_dist(record)
            if d < min_dist_info[0]:
                min_dist_info[0] = d
                min_dist_info[1] = record.copy()
                min_dist_info[2] = path
            return
        for i in choices[path[n] - 1]:
            record.append(i)
            dfs(path, n+1, record, choices, min_dist_info)
            record.pop()

    # *** Brute Force: ***
    # for path in tqdm(paths, total=len(paths)):
    #     rec = [case[0]]
    #     dfs(path[1:], 0, rec, choices, min_dist_info)
    
    # *** Prunning: ***
    paths_case = [[case[i] for i in path] for path in paths]
    paths_indices = rank_dist(paths_case, rank_N)

    for path_idx, path in tqdm(enumerate(paths), total=len(paths)):
        if path_idx not in paths_indices:
            continue
        new_choices = [None for _ in choices]
        for i in range(len(choices)):
            last_node = paths_case[path_idx][i][:2]
            next_node = paths_case[path_idx][i+2][:2] if i != len(choices) - 1 else None
            choices_indices = rank_choices(A, last_node, next_node, choices[path[i+1] - 1], rank_k)
            new_choices[path[i+1] - 1] = [choices[path[i+1] - 1][j] for j in choices_indices]
        
        rec = [case[0]]
        dfs(path[1:], 0, rec, new_choices, min_dist_info)

    print(min_dist_info[0], A.lookup_times, min_dist_info[0] / opt)

    print("接乘顺序：", min_dist_info[2])
    print("上车点：")
    for i, node in enumerate(min_dist_info[1][1:]):
        for j, choice in enumerate(choices):
            if node in choice:
                print(choice.index(node) + 1, end=",")
    print()

    map = visualize(case, choices)
    add_path(map, min_dist_info[1])
    # map.save(f"task3-{case_id}-3_2.html")
