# -*- coding:utf-8 -*-
from haversine import haversine
import json
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)

class Data:
    """
    A class to represent the data for the TSP problem, including orders, vehicles, and depot information.
    """

    def __init__(self, data=None):
        """
        Initialize the Data class with empty attributes.
        """
        if data:
            temp = data
        else:
            print("请求数据失败")
            with open(f'{parent_path}/input/test-2025-03-07.json', 'r', encoding='utf-8') as f:
                temp = json.load(f)
        self.dispatchId = temp["dispatchId"]
        print(self.dispatchId)
        print("\n=========================配置信息=========================\n")
        self.config = temp["config"]
        print(self.config)
        print("\n=========================仓库信息=========================\n")
        self.depots = temp["depots"]
        for item in self.depots:
            print(item)

        self.dispatchZone = temp["dispatchZone"]
        print("\n=========================区域信息=========================\n")
        print("区域数量：", len(self.dispatchZone))
        print("各区域ID：")
        for item in self.dispatchZone:
            print(item['dispatchZoneCode'])

        #把所有区域的订单汇总到self.orders
        self.orders = temp["orders"]

        for item in self.dispatchZone:
            print(f"\n=========================区域{item['dispatchZoneCode']}的仓库信息=========================\n")
            for item1 in self.depots:
                if item1['longitude'] == item['longitude'] and item1['latitude'] == item['latitude']:
                    #当前区域的信息字典里面新增一个键值对: depot: {}
                    item['depot'] = item1
                    print(item1)

            print(f"\n=========================区域{item['dispatchZoneCode']}的订单信息=========================\n")
            #当前区域的信息字典里面新增一个键值对：orders: [], 列表里存放的是当前区域的订单信息
            item['orders'] = []
            # 当前区域的信息字典里面新增一个键值对：locations: {地点名：坐标}
            item['locations'] = {}
            for item1 in self.orders:
                if item1['dispatchZoneCode'] == item['dispatchZoneCode']:
                    item['orders'].append(item1)
                    print(item1)
                    item['locations'][item1['addressNo']] = (float(item1['latitude']), float(item1['longitude']))

            print(f"\n=========================区域{item['dispatchZoneCode']}的车型信息=========================\n")
            for item1 in item['vehicleType']:
                print(item1)

            print(f"\n=========================区域{item['dispatchZoneCode']}的车辆信息=========================\n")
            for item1 in item['vehicle']:
                for item2 in item['vehicleType']:
                    if item1['vehicleType'] == item2['vehicleTypeId']:
                        item1.update(item2)
                print(item1)

            print(f"\n========================区域{item['dispatchZoneCode']}的费率合同信息=======================\n")
            for item1 in item['tariff']:
                print(item1)

    def calculate_distance(self):
        self.distance_matrix = {}
        # 遍历每一个区域的locations字典
        for item in self.dispatchZone:
            for key1, value1 in item['locations'].items():
                for key2, value2 in item['locations'].items():
                    if key1 == key2:
                        self.distance_matrix[key1, key2] = 0
                    else:
                        self.distance_matrix[key1, key2] = haversine(value1, value2)

            lonLat_depot = (float(item['depot']["latitude"]), float(item['depot']["longitude"]))
            for key1, value1 in item['locations'].items():
                self.distance_matrix[item['depot']["branchId"], key1] = haversine(lonLat_depot, value1)
                self.distance_matrix[key1, item['depot']["branchId"]] = 0 #因为不考虑返程

        self.distance_matrix[item['depot']["branchId"], item['depot']["branchId"]] = 0

    def read_from_json(self):
        '''
        从database目录下的json中读取距离矩阵
        '''
        with open(f'{parent_path}/database/distance_matrix.json', 'r') as json_file:
            distance_json = json_file.read()

        # 将JSON字符串反序列化为字典
        string_key_distance = json.loads(distance_json)

        # 将字符串键转换回元组键
        self.distance_matrix = {tuple(k.split('_')): v for k, v in string_key_distance.items()}

        api_key = '827a5baf7d29670c622db4fa5a0fa2f0'

        #遍历每一个区域的locations字典
        for item in self.dispatchZone:
            for key1, value1 in item['locations'].items():
                for key2, value2 in item['locations'].items():
                    if key1 == key2:
                        self.distance_matrix[key1, key2] = 0
                    else:
                        if (key1, key2) not in self.distance.keys():
                            self.distance_matrix[key1, key2] = self.amap_distance(value1, value2, api_key)

            lonLat_depot = (float(item['depot']["latitude"]), float(item['depot']["longitude"]))
            for key1, value1 in item['locations'].items():
                self.distance_matrix[item['depot']["branchId"], key1] = self.amap_distance(lonLat_depot, value1, api_key)
                self.distance_matrix[key1, item['depot']["branchId"]] = 0 #因为不考虑返程

        self.distance_matrix[depot["branchId"], depot["branchId"]] = 0

        # 将距离矩阵转换为JSON格式
        string_key_distance = {'_'.join(map(str, k)): v for k, v in self.distance_matrix.items()}

        # 将新的字典转换为JSON格式
        distance_json = json.dumps(string_key_distance)

        # 将JSON字符串写入到文件中
        with open(f'{parent_path}/database/distance_matrix.json', 'w') as json_file:
            json_file.write(distance_json)

    def amap_distance(self, origin, destination, api_key):
        '''
        引入重试机制
        '''
        print("===========")
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

if __name__ == "__main__":
    d = Data()
    d.calculate_distance()