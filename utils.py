import pandas as pd
import numpy as np
import folium
from folium import plugins, PolyLine


class ABS:

    def __init__(self, dir: str):
        self._read_data(dir)
        self.empty_cache()

    def dist(self, x: int, y: int) -> float:
        if x == y:
            return 0
        if self.dist_cache[x][y] < 1e-5:
            self.dist_cache[x][y] = self._distance_data[x][y]
            self.lookup_times += 1
        return self.dist_cache[x][y]

    def path_dist(self, s: list) -> float:
        # [[经度，纬度，邻近Link，所占比例]]
        distance=0
        for i in range(len(s) - 1):
            Link_O = s[i][2]
            Ratio_O = s[i][3]
            Link_D = s[i+1][2]
            Ratio_D = s[i+1][3]

            # Node_1为出发点对应边的终点
            Node_1 = int(self.link_data[Link_O - 1][4])
            # Node_2为目的地对应边的起点
            Node_2 = int(self.link_data[Link_D - 1][1])
            
            distance += self.dist(Node_1,Node_2)
            distance += self.link_data[Link_O - 1][7] * (1 - Ratio_O)
            distance += self.link_data[Link_D - 1][7] * Ratio_D

        return distance

    def empty_cache(self):
        self.lookup_times = 0
        self.dist_cache = np.zeros(self._distance_data.shape)

    def _read_data(self, dir: str):
        """
        print("Cases列表: ", cases)
        print("Cases字段: ", cases_data.keys())
        print("访问一个case:", cases[0])
        print("访问一个case中某个值:", cases[0]['纬度.2'])
        candidates = eval(cases[0]['经纬度'])
        print("访问一个case中起点1所有候选点的经纬度:", candidates)
        print("节点数量: ", len(list(G_nodes_dic.keys())))
        print("边数量", len(G_edges))
        print("输出节点3的经纬度: ",G_nodes_dic[3])
        print("输出第0条边的起点、终点、长度: ",G_edges[0])
        """
        self.cases_data = pd.read_csv(f"{dir}/R3-case-14.csv", encoding="utf-8", skiprows=[0])
        self._distance_data = pd.read_csv(f"{dir}/R1-distance.csv", header=None)
        self.link_data = pd.read_csv(f"{dir}/R2-link.csv").values
        self.cases =[]
        for i in range(self.cases_data.shape[0]):
            d = dict(self.cases_data.iloc[i])
            self.cases.append(d)
        
        # self.G_edges=[]
        # self.G_nodes_dic={}
        # for i in range(self.link_data.shape[0]):
        #     dic = dict(self.link_data.iloc[i])
        #     self.G_nodes_dic[dic['Node_Start']]=(dic['Longitude_Start'], dic['Latitude_Start'])
        #     self.G_edges.append((int(dic['Node_Start']), int(dic['Node_End']),dic['Length']))


def visualize(case: list, path: list, name: str = "map_visualization"):
    if len(case) == 5:
        visualize_double(case, path, name + "_2")
    elif len(case) == 7:
        visualize_triple(case, path, name + "_3")

def visualize_double(case: list, path: list, name: str):
    map1 = folium.Map(
        location=[30.66,104.11],
        zoom_start=13,
        control_scale = True,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; <a href="http://ditu.amap.com/">高德地图</a>'
    )

    #folium标记函数中第一个参数是位置，先纬度，后经度
    folium.Marker([case[0][1], case[0][0]], popup='<i>车点</i>', icon=folium.Icon(icon='home', color='orange')).add_to(map1)
    folium.Marker([case[1][1], case[1][0]], popup='<i>起点1</i>', icon=folium.Icon(icon='cloud', color='blue')).add_to(map1)
    folium.Marker([case[3][1], case[3][0]], popup='<i>终点1</i>', icon=folium.Icon(icon='cloud', color='red')).add_to(map1)
    folium.Marker([case[2][1], case[2][0]], popup='<i>起点2</i>', icon=folium.Icon(icon='ok-sign', color='blue')).add_to(map1)
    folium.Marker([case[4][1], case[4][0]], popup='<i>终点2</i>', icon=folium.Icon(icon='ok-sign', color='red')).add_to(map1)

    for i in range(4):
        PolyLine([(case[path[i]][1],case[path[i]][0]), (case[path[i+1]][1],case[path[i+1]][0])], 
                weight=5, color='blue', opacity=0.8).add_to(map1)

    map1.save(f"{name}.html")

def visualize_triple(case: list, path: list, name: str):
    map1 = folium.Map(
        location=[30.66,104.11],
        zoom_start=13,
        control_scale = True,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; <a href="http://ditu.amap.com/">高德地图</a>'
    )

    #folium标记函数中第一个参数是位置，先纬度，后经度
    folium.Marker([case[0][1], case[0][0]], popup='<i>车点</i>', icon=folium.Icon(icon='home', color='orange')).add_to(map1)
    folium.Marker([case[1][1], case[1][0]], popup='<i>起点1</i>', icon=folium.Icon(icon='cloud', color='blue')).add_to(map1)
    folium.Marker([case[4][1], case[4][0]], popup='<i>终点1</i>', icon=folium.Icon(icon='cloud', color='red')).add_to(map1)
    folium.Marker([case[2][1], case[2][0]], popup='<i>起点2</i>', icon=folium.Icon(icon='ok-sign', color='blue')).add_to(map1)
    folium.Marker([case[5][1], case[5][0]], popup='<i>终点2</i>', icon=folium.Icon(icon='ok-sign', color='red')).add_to(map1)
    folium.Marker([case[3][1], case[3][0]], popup='<i>起点3</i>', icon=folium.Icon(icon='info-sign', color='blue')).add_to(map1)
    folium.Marker([case[6][1], case[6][0]], popup='<i>终点3</i>', icon=folium.Icon(icon='info-sign', color='red')).add_to(map1)

    for i in range(6):
        PolyLine([(case[path[i]][1],case[path[i]][0]), (case[path[i+1]][1],case[path[i+1]][0])], 
                weight=5, color='blue', opacity=0.8).add_to(map1)

    map1.save(f"{name}.html")


def visualize_choices_triple(case: list, choices: list) -> folium.Map:
    map1 = folium.Map(
        location=[30.66,104.11],
        zoom_start=13,
        control_scale = True,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; <a href="http://ditu.amap.com/">高德地图</a>'
    )

    #folium标记函数中第一个参数是位置，先纬度，后经度
    folium.Marker([case[0][1], case[0][0]], popup='<i>车点</i>', icon=folium.Icon(icon='home', color='orange')).add_to(map1)

    folium.Marker([case[1][1], case[1][0]], popup='<i>起点1</i>', icon=folium.Icon(icon='info-sign', color='blue')).add_to(map1)
    folium.Marker([case[4][1], case[4][0]], popup='<i>终点1</i>', icon=folium.Icon(icon='info-sign', color='blue')).add_to(map1)
    for i, choice in enumerate(choices[0]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>起点1候车点{i+1}</i>', icon=folium.Icon(icon='cloud', color='blue')).add_to(map1)
    for i, choice in enumerate(choices[3]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>终点1候车点{i+1}</i>', icon=folium.Icon(icon='ok-sign', color='blue')).add_to(map1)
    
    folium.Marker([case[2][1], case[2][0]], popup='<i>起点2</i>', icon=folium.Icon(icon='info-sign', color='red')).add_to(map1)
    folium.Marker([case[5][1], case[5][0]], popup='<i>终点2</i>', icon=folium.Icon(icon='info-sign', color='red')).add_to(map1)
    for i, choice in enumerate(choices[1]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>起点2候车点{i+1}</i>', icon=folium.Icon(icon='cloud', color='red')).add_to(map1)
    for i, choice in enumerate(choices[4]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>终点2候车点{i+1}</i>', icon=folium.Icon(icon='ok-sign', color='red')).add_to(map1)
    
    folium.Marker([case[3][1], case[3][0]], popup='<i>起点3</i>', icon=folium.Icon(icon='info-sign', color='green')).add_to(map1)
    folium.Marker([case[6][1], case[6][0]], popup='<i>终点3</i>', icon=folium.Icon(icon='info-sign', color='green')).add_to(map1)
    for i, choice in enumerate(choices[2]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>起点3候车点{i+1}</i>', icon=folium.Icon(icon='cloud', color='green')).add_to(map1)
    for i, choice in enumerate(choices[5]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>终点3候车点{i+1}</i>', icon=folium.Icon(icon='ok-sign', color='green')).add_to(map1)
    
    map1.save(f"tmp_3.html")
    return map1
    
def visualize_choices_double(case: list, choices: list) -> folium.Map:
    map1 = folium.Map(
        location=[30.66,104.11],
        zoom_start=13,
        control_scale = True,
        tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
        attr='&copy; <a href="http://ditu.amap.com/">高德地图</a>'
    )

    #folium标记函数中第一个参数是位置，先纬度，后经度
    folium.Marker([case[0][1], case[0][0]], popup='<i>车点</i>', icon=folium.Icon(icon='home', color='orange')).add_to(map1)

    folium.Marker([case[1][1], case[1][0]], popup='<i>起点1</i>', icon=folium.Icon(icon='info-sign', color='blue')).add_to(map1)
    folium.Marker([case[3][1], case[3][0]], popup='<i>终点1</i>', icon=folium.Icon(icon='info-sign', color='blue')).add_to(map1)
    for i, choice in enumerate(choices[0]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>起点1候车点{i+1}</i>', icon=folium.Icon(icon='cloud', color='blue')).add_to(map1)
    for i, choice in enumerate(choices[2]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>终点1候车点{i+1}</i>', icon=folium.Icon(icon='ok-sign', color='blue')).add_to(map1)
    
    folium.Marker([case[2][1], case[2][0]], popup='<i>起点2</i>', icon=folium.Icon(icon='info-sign', color='red')).add_to(map1)
    folium.Marker([case[4][1], case[4][0]], popup='<i>终点2</i>', icon=folium.Icon(icon='info-sign', color='red')).add_to(map1)
    for i, choice in enumerate(choices[1]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>起点2候车点{i+1}</i>', icon=folium.Icon(icon='cloud', color='red')).add_to(map1)
    for i, choice in enumerate(choices[3]):
        folium.Marker([choice[1], choice[0]], popup=f'<i>终点2候车点{i+1}</i>', icon=folium.Icon(icon='ok-sign', color='red')).add_to(map1)

    map1.save(f"tmp_2.html")
    return map1

def add_link(map: folium.Map, point1: tuple, point2: tuple) -> folium.Map:
    PolyLine([point1, point2], weight=5, color='blue', opacity=0.8).add_to(map)
    return map

def add_path(map: folium.Map, path: list) -> folium.Map:
    for i in range(len(path) - 1):
        add_link(map, (path[i][1], path[i][0]), (path[i+1][1], path[i+1][0]))
    return map
