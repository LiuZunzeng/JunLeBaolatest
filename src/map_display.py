'''
Descripttion: 
version: 
Author: XingkaiWang
Date: 2024-07-24 10:39:45
LastEditors: XingkaiWang
LastEditTime: 2024-07-26 11:23:47
'''
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))[:-4]
import folium
from folium import plugins
from typing import Tuple
import requests
import time
from loguru import logger
from data.data import Data

class Route_display():
    def __init__(self, route, map_center = None) -> None:
        '''
        route:List，输入车辆的轨迹--[{address:coordnation},...]
        map_center:地图中心的坐标
        '''
        self.route = route
        self.map = folium.Map(
            location=map_center,
            tiles='http://webrd02.is.autonavi.com/appmaptile?''lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
            # tiles='http://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
            # attr="http://ditu.amap.com/",
            attr='jiuzhang',
            zoom_start=6)
        # 全屏按键
        plugins.Fullscreen(position='topright',
                        title='全屏',
                        title_cancel='退出',
                        force_separate_button=True).add_to(self.map)
        #左侧可操作控件
        plugdraw = plugins.Draw()
        plugdraw.add_to(self.map)
        # 获取点的经纬度
        self.map.add_child(folium.LatLngPopup())
        # 在单击位置新建标记点
        #m.add_child(folium.ClickForMarker(popup='Waypoint'))

        self.colors = ['red', 'blue', 'gray', 'darkred', 'orange', 'green',
            'darkgreen', 'lightgreen', 'darkblue', 'lightblue', 'purple',
            'pink', 'cadetblue', 'lightgray', 'black', 'lawngreen',
            'deepskyblue', 'deeppink', 'indigo', 'gold', 'mediumorchid',
            'thistle', 'coral', 'chocolate', 'magenta', 'salmon', 'khaki',
            'darkmagenta', 'powderblue', 'palevioletred', 'lime', 'crimson',
            'aqua', 'cadetblue', 'moccasin', 'tan', 'teal', 'wheat',
            'cornflowerblue']

    def get_direction_driving(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        # FIXME：不考虑当时路况
        # strategy=6,
        strategy=0,
    ) -> dict:
        """
        驾车路径规划 API
        可以规划以小客车、轿车通勤出行的方案，并且返回通勤方案的数据。
        https://lbs.amap.com/api/webservice/guide/api/direction/#driving
        Args:
            origin: 起点
            destination: 终点
            strategy: 驾车选择策略
                0，速度优先，不考虑当时路况，此路线不一定距离最短
                1，费用优先，不走收费路段，且耗时最少的路线
                6，速度优先，不走高速，但是不排除走其余收费路段
                7，费用优先，不走高速且避免所有收费路段
        Returns:
            'is_success': 是否成功
            'distance': 行驶距离
            'duration': 预计行驶时间
            'taxi_cost': 打车费用
            'u_turn_times': 调头次数
            'points': 所有路段坐标点
        """
        o_lng, o_lat = origin
        d_lng, d_lat = destination
        #cur_key = '827a5baf7d29670c622db4fa5a0fa2f0'
        cur_key = '827a5baf7d29670c622db4fa5a0fa2f0'
        res = requests.get(
            f'https://restapi.amap.com/v3/direction/driving?'
            f'key={cur_key}'
            f'&origin={o_lng},{o_lat}'
            f'&destination={d_lng},{d_lat}'
            f'&strategy={strategy}'  # 驾车选择策略
            f'&output=JSON'
            f'&extensions=all',
            timeout=40# taxi_cost打车费用
        ).json()
        time.sleep(0.4)
        if res['status'] == '0':
            logger.error(
                f"error: 高德API: {res['info']}, {cur_key}, {origin}, {destination}"
            )
            query_dict = {'is_success': False}
            return query_dict
        route = res['route']  # 驾车路径规划信息列表
        path = route['paths'][0]  # 驾车换乘方案
        distance = path['distance']  # 0. 行驶距离, 单位：米
        duration = path['duration']  # 1. 预计行驶时间, 单位：秒
        point_str_list = list()
        point_list = list()
        # polyline: 此路段坐标点串
        for point in ';'.join([step['polyline'] for step in path['steps']
                              ]).split(';'):
            if (not point_str_list) or (point != point_str_list[-1]):
                point_str_list.append(point)
                lng, lat = point.split(',')
                point_list.append((float(lat), float(lng)))
        query_dict = {
            'is_success': True,
            'distance': int(distance),
            'duration': int(duration),
            'points': point_list,
        }
        return query_dict
    
    def draw(self):
        vehicle_map = [folium.FeatureGroup(name='车辆_{}'.format(vehicle_id), control=True, show=False) for vehicle_id in range(len(self.route))]
        c_cnt = 0
        for vehicle_id, vehicle in enumerate(self.route):
            if len(vehicle) <= 1: continue
            pre_coord = None
            polyline = []
            for place_name, coord in vehicle.items():
                if pre_coord:
                    polyline+=self.get_direction_driving(pre_coord[::-1], coord[::-1])['points']
                pre_coord = coord

                folium.Marker(
                    location=coord,
                    popup=place_name,
                    icon=folium.Icon(color=self.colors[c_cnt], icon='glyphicon-star', show=True, max_width=300, opacity=0.3,
                                    sticky=True)).add_to(vehicle_map[vehicle_id])

                # c_cnt = (c_cnt + 1) % len(self.colors)
            folium.PolyLine(
                locations=polyline,
                color=self.colors[c_cnt],
                weight=3,
                opacity=1,
                # tooltip=comment,
            ).add_to(vehicle_map[vehicle_id])
            c_cnt = (c_cnt + 1) % len(self.colors)
            self.map.add_child(vehicle_map[vehicle_id])
        
    def save(self, save_path):
        folium.LayerControl().add_to(self.map)
        self.map.save(save_path)

if __name__ == '__main__':
    # st = time.time()
    # try:
    #     with open('direction.json', 'r', encoding='utf-8') as f:
    #         distance_dict = json.load(f)
    # except:
    #     distance_dict = {}
    # print(time.time()-st)
    # for idx1, place1 in enumerate(all_place):
    #     if idx1 > 30: continue
    #     for idx2, place2 in enumerate(all_place):
    #         if idx1 == idx2: continue
    #         distance_dict[place1+'|'+place2] = map_dis.get_direction_driving([all_coord[idx1][1], all_coord[idx1][0]], [all_coord[idx2][1], all_coord[idx2][0]])

    # to_json = json.dumps(distance_dict, indent=4, ensure_ascii=False)
    # with open('direction.json', 'w', encoding='utf-8') as f:
    #     f.write(to_json)
    # exit()
    map_dis = Route_display()
    input_data = Data()
    input_data.read_excel()
    input_data.read_order()
    input_data.add_depot()
    print(input_data.node_dic)
    all_place = []
    all_coord = []
    for name, coord in input_data.node_dic.items():
        if name == 'end': continue
        if name == 'start': 
            name = '湖北省十堰市丹江口市六里坪镇工业园'
        all_place.append(name)
        all_coord.append(coord)
    

    
