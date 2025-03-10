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
            with open(f'{parent_path}/input/new_example.json', 'r', encoding='utf-8') as f:
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

        self.orders = temp["orders"]

        for item in self.dispatchZone:

            print(f"\n=========================区域{item['dispatchZoneCode']}的订单信息=========================\n")
            item['orders'] = []
            for item1 in self.orders:
                if item1['dispatchZoneCode'] == item['dispatchZoneCode']:
                    item['orders'].append(item1)
                    print(item1)

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
        for i in range(len(self.orders)):
            for j in range(len(self.orders)):
                lonLat_1 = (float(self.orders[i]["latitude"]), float(self.orders[i]["longitude"]))
                lonLat_2 = (float(self.orders[j]["latitude"]), float(self.orders[j]["longitude"]))
                self.distance_matrix[self.orders[i]["orderNo"], self.orders[j]["orderNo"]] = haversine(lonLat_1, lonLat_2)

        for depot in self.depots:
            lonLat_depot = (float(depot["latitude"]), float(depot["longitude"]))
            for i in range(len(self.orders)):
                lonLat_1 = (float(self.orders[i]["latitude"]), float(self.orders[i]["longitude"]))
                self.distance_matrix[depot["branchId"], self.orders[i]["orderNo"]] = haversine(lonLat_depot, lonLat_1)
                self.distance_matrix[self.orders[i]["orderNo"], depot["branchId"]] = 0

            self.distance_matrix[depot["branchId"], depot["branchId"]] = 0

