import pandas as pd
from haversine import haversine
import numpy as np
import requests
import os
import time
import json
from data.order import Order
from data.depot import depot
from data.vehicle import vehicle
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(os.path.dirname(root_path))

class Data:

    def __init__(self):
        self.order_list = []
        self.vehicle_list = []
        self.order_dic = {}
        self.customer_orders = {}
        self.weight_dic = {}
        self.cubic_dic = {}
        self.node_dic = {}
        self.distance = {}
        self.vehicle_dic = {}
        self.city_dic = {}

    def read_excel(self, data=None):
        if data:
            self.data = data
        else:
            # 读取Excel文件
            excel_file = f'{parent_path}/input/combined_excel1.xlsx'
            sheet_names = ['订单信息', '仓库信息', '车辆信息']
            sheet_dic = {'订单信息': 'orders', '仓库信息': 'depots', '车辆信息': 'vehicles'}
            # 创建一个字典来存储每个工作表的数据
            data = {}

            # 使用pandas读取每个工作表
            for sheet_name in sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')
                data[sheet_dic[sheet_name]] = df.to_dict('records')
            self.data = data
        self.customerNum = len(self.data['orders'])
        vehicleNum = len(self.data['vehicles'])
        print("order quantity：", self.customerNum)
        print("vehicle quantity：", vehicleNum)

    def read_order(self):
        # 遍历客户数量，为每个订单创建Order对象并添加到订单列表
        for i in range(self.customerNum):
            # 将订单信息添加到订单列表
            self.order_list.append(Order(self.data['orders'][i]['订单号'],
                                         self.data['orders'][i]['体积'],
                                         self.data['orders'][i]['地址'],
                                         self.data['orders'][i]['重量'],
                                         # 将经纬度字符串分割为浮点数，并组成元组
                                         (float(self.data['orders'][i]['经纬度'].split(',')[1]),
                                          float(self.data['orders'][i]['经纬度'].split(',')[0])),
                                         self.data['orders'][i]['地址编号'],
                                         self.data['orders'][i]['数量'],
                                         self.data['orders'][i]['城市']))

        # 初始化仓库对象
        self.depot = depot(self.data['depots'][0]['地址'],
                           self.data['depots'][0]['地址编号'],
                           # 将经纬度字符串分割为浮点数，并组成元组
                           (float(self.data['depots'][0]['经纬度'].split(',')[1]),
                            float(self.data['depots'][0]['经纬度'].split(',')[0])))

        # 遍历车辆信息，为每辆车创建vehicle对象并添加到车辆列表
        for v in range(len(self.data['vehicles'])):
            self.vehicle_list.append(vehicle(self.data['vehicles'][v]['车辆ID'],
                                             self.data['vehicles'][v]['最大载重'],
                                             self.data['vehicles'][v]['最大件数'],
                                             self.data['vehicles'][v]['最大容量']))

        # 将车辆信息添加到车辆字典
        for i in range(len(self.data['vehicles'])):
            self.vehicle_dic[self.vehicle_list[i].vehicleId] = (
                self.vehicle_list[i].maxVolume, self.vehicle_list[i].maxWeight, self.vehicle_list[i].maxQty)
        print("车辆字典：", self.vehicle_dic)

        orderNo_list = []
        weight = 0
        cubic = 0
        # 计算总重量和总体积
        for i in range(self.customerNum):
            orderNo_list.append(self.order_list[i].addressNo)
            self.order_dic[self.order_list[i].address] = self.order_list[i].lonLat
            self.city_dic[self.order_list[i].address] = self.order_list[i].city
            weight += self.order_list[i].weight
            cubic += self.order_list[i].cubic
        print("total weight：", weight)
        print("total cubic：", cubic)

        # 构建用于写json文件的订单信息字典
        for key in self.order_dic.keys():
            temp = []
            for order in self.order_list:
                if order.addressNo == key:
                    temp.append(order.orderNo)
            resulting_string = ";".join(temp)
            self.customer_orders[key] = resulting_string

        # 构建重量和体积字典
        for key in self.order_dic.keys():
            weight = 0
            cubic = 0
            for i in range(self.customerNum):
                if self.order_list[i].address == key:
                    weight += self.order_list[i].weight
                    cubic += self.order_list[i].cubic
            self.weight_dic[key] = weight
            self.cubic_dic[key] = cubic
        print("重量字典：", self.weight_dic)

        # 使用Counter计算地址编号的出现次数
        from collections import Counter
        self.element_count = dict(Counter(orderNo_list))

        print("total quantity of addressNos：", len(self.order_dic))

    def amap_distance(self, origin, destination, api_key):
        '''
        引入重试机制
        '''
        print("--------------------------")
        base_url = "https://restapi.amap.com/v3/direction/driving"

        # 缓存字典，存储最近的请求结果
        cache = {}

        # 构建请求参数
        params = {
            "origin": f"{origin[1]},{origin[0]}",
            "destination": f"{destination[1]},{destination[0]}",
            "key": api_key
        }

        # 将起点和终点转换为字符串，作为缓存的键
        cache_key = f"{origin[0]},{origin[1]}->{destination[0]},{destination[1]}"

        # 检查缓存中是否有结果
        if cache_key in cache:
            print("Using cache data.")
            return cache[cache_key]
        else:
            # 初始化重试次数和延迟时间
            max_retries = 5
            backoff_factor = 0.5
            retry_delay = 1  # 初始延迟时间为1秒
            timeout = (5, 8)  # 设置连接超时为5秒，读取超时为15秒

            for attempt in range(max_retries):
                try:
                    # 发送请求，设置超时时间
                    response = requests.get(base_url, params=params, timeout=timeout)
                    response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常

                    # 简单的延迟，减少请求频率
                    time.sleep(0.2)

                    data = response.json()
                    if data.get('status') == '1' and data.get('info') == 'OK':
                        route = data.get('route', {})
                        paths = route.get('paths', [])
                        if paths:
                            result = paths[0].get('distance')
                            if result is not None:
                                distance_km = float(result) / 1000.0
                                cache[cache_key] = distance_km
                                return distance_km
                            else:
                                print("Distance not found in the response.")
                                return None
                        else:
                            print("No paths found in the response.")
                            return None
                    else:
                        print("API Error:", data.get('info', 'Unknown error'))
                        return None
                except requests.exceptions.HTTPError as http_err:
                    print(f"HTTP Error on attempt {attempt + 1}: {http_err}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= backoff_factor  # 指数退避
                    else:
                        print("Max retries reached. Giving up.")
                        return None
                except requests.exceptions.ConnectionError as conn_err:
                    print(f"Connection Error on attempt {attempt + 1}: {conn_err}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= backoff_factor
                    else:
                        print("Max retries reached. Giving up.")
                        return None
                except requests.exceptions.Timeout as timeout_err:
                    print(f"Timeout Error on attempt {attempt + 1}: {timeout_err}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= backoff_factor
                    else:
                        print("Max retries reached. Giving up.")
                        return None
                except requests.exceptions.RequestException as req_err:
                    print(f"Request Exception on attempt {attempt + 1}: {req_err}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= backoff_factor
                    else:
                        print("Max retries reached. Giving up.")
                        return None

    def calculate_distance(self):
        print("------------calculate distance-------------")
        for key1, value1 in self.node_dic.items():
            for key2, value2 in self.node_dic.items():
                if key1 != key2:
                    #self.distance[key1, key2] = haversine(value1, value2)
                    api_key = '827a5baf7d29670c622db4fa5a0fa2f0'
                    self.distance[key1, key2] = self.amap_distance(value1, value2, api_key)
                else:
                    self.distance[key1, key2] = 0
        for key1, value1 in self.order_dic.items():
            self.distance[key1, 'end'] = 0
            self.distance[key1, 'start'] = 0
            self.distance['end', key1] = 0

        self.distance['start', 'end'] = 0
        self.distance['end', 'start'] = 0
        # 将距离矩阵转换为JSON格式
        string_key_distance = {'_'.join(map(str, k)): v for k, v in self.distance.items()}

        # 将新的字典转换为JSON格式
        distance_json = json.dumps(string_key_distance)

        # 将JSON字符串写入到文件中
        with open('distance_matrix1.json', 'w') as json_file:
            json_file.write(distance_json)
            # self.distance[key1, key2] = 10000
        #print(self.distance)

    def read_from_json(self):
        with open('distance_matrix1.json', 'r') as json_file:
            distance_json = json_file.read()

        # 将JSON字符串反序列化为字典
        string_key_distance = json.loads(distance_json)

        # 将字符串键转换回元组键
        self.distance = {tuple(k.split('_')): v for k, v in string_key_distance.items()}

        count = 0
        for key1, value1 in self.node_dic.items():
            for key2, value2 in self.node_dic.items():
                if self.distance[key1, key2] is None:
                    api_key = '827a5baf7d29670c622db4fa5a0fa2f0'
                    self.distance[key1, key2] = self.amap_distance(value1, value2, api_key)
                    count += 1
        print("count", count)

    def add_depot(self):
        self.node_dic = self.order_dic.copy()
        self.node_dic['start'] = self.depot.lonLat
        self.node_dic['end'] = self.depot.lonLat
        print("添加仓库后的坐标列表长度：", len(self.node_dic))

if __name__ == '__main__':
    s = Data()
    s.read_excel()
    s.read_order()
    s.add_depot()
    s.calculate_distance()

