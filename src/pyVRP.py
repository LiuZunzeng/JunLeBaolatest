# -*- coding:utf-8 -*-
from pyvrp.stop import MaxRuntime
from pyvrp import Model
import numpy as np
from data import Data

class PyVRP:
    '''
        使用混合遗传算法求解VRPTW问题
    '''
    def __init__(self,
                 config: dict,
                 departure_wave: str,
                 depot: dict,
                 orders: list,
                 vehicles: list,
                 tariff: list,
                 distance_matrix: dict):
        """
            config：{
                "DELIVERY_LOADING_SPEED": 1.5,
                "DELIVERY_STAY_MINUTE": 5,
                "ROS_VEHICLE_SPEED": 50,
                "ROS_SPLIT_ORDER": "Y",
                "ROS_NORMAL_TEMPERATURE_RATIO": 0.90
            }
            departureWave: "0:00-1:00,2:00-4:00"
            depot: {
                "branchId": "WH01",
                "branchDescr": "张江物流中⼼",
                "longitude": "121.50389",
                "latitude": "31.29665",
                "notes": "说明",
                "branch_status": "0"
            }
            orders: [
                {
                    "dispatchZoneCode": "DISZONE001",
                    "taskNo": "PO001-2",
                    "orderNo": "PO001",
                    "DC": "WH01",
                    "orderType": "D",
                    "createTime": "2025-03-04T10:00",
                    "qty": 10,
                    "weight": 15.5,
                    "cubic": 42.7,
                    "money": 100.0,
                    "bulkFlag": 1,
                    "routeNo": "",
                    "routeNoNext": "",
                    "offeringType": "汽运",
                    "temperatureClass": "冷藏",
                    "addressNo": "ADDR001",
                    "address": "上海市杨浦区邯郸路某某号",
                    "timeWindowFrom": "00:00",
                    "timeWindowTo": "23:59",
                    "vehicleCategory": "type1, type2",
                    "longitude": "121.50389",
                    "latitude": "31.29665",
                    "consigneeId": "A001",
                    "companyClass": "0点",
                    "availableVehicleType": "type1, type2",
                    "vehicleCategoryCus": "type1, type2",
                    "unloadingTimeWindow": "8:00-12:00,14:00-18:00",
                    "nonUnloadingTimeWindow": "12:00-14:00,18:00-24:00",
                    "leadTime": 36.0,
                    "SDD": "1, 2, 3",
                    "ordersDetails":[
                        {
                            "taskNo": "PO001-2",
                            "taskLineNo": "1",
                            "sku": "210001",
                            "skuDescr1": "老酸奶",
                            "qty": 2,
                            "weight": 2.0,
                            "cubic": 6.2,
                            "temperatureType": "冷藏",
                            "grossWeight": 1.0,
                            "cube": 3.1
                        }
                    ]
                }
            ]
            tariff:[
                {
                    "tariffID": "JLB-JT-202410-00098",
                    "offeringType": "整车运输",
                    "shipperProvince": "河北",
                    "shipperCity": "石家庄",
                    "shipperDistrict": "",
                    "consigneeProvince": "山东",
                    "consigneeCity": "济南",
                    "consigneeDistrict": "",
                    "temperatureType": "冷藏",
                    "mileage": 399.0,
                    "rateBase": "吨公里",
                    "initialRate": 0.650
                }
            ]
        """
        self.config = config
        self.departure_wave = departure_wave
        self.depot = depot
        self.orders = orders
        self.vehicles = vehicles
        self.tariff = tariff
        self.distance_matrix = distance_matrix
        self.solution_status = 0

    def build_model(self):
        """
        将必要的信息传入pyvrp的model类当中
        """

        def weight_or_cubic(data):
            "return 0: Use weight constraint; 1: Use volume constraint"
            cubic = 0
            weight = 0
            for i in range(len(data.orders)):
                cubic += data.orders[i]["cubic"]
                weight += data.orders[i]["weight"]
            average_cubic = cubic / len(data.orders)
            average_weight = weight / len(data.orders)

            weight_lst = []
            volume_lst = []
            for i in range(len(data.vehicles)):
                weight_lst.append(data.vehicles[i]["maxWeight"])
                volume_lst.append(data.vehicles[i]["maxVolume"])
            max_weight = max(weight_lst)
            max_volume = max(volume_lst)

            if (max_weight / average_weight < max_volume / average_cubic):
                return 0
            else:
                return 1

        def time_to_minutes(time_str):
            '''
            time_str:"2:00"
            '''

            # 分割字符串
            hours, minutes = time_str.split(":")

            # 将小时和分钟转换为整数
            hours = int(hours)
            minutes = int(minutes)

            # 将小时转换为分钟并加上分钟部分
            total_minutes = hours * 60 + minutes

            return total_minutes

        self.m = Model()

        for i in range(len(self.vehicles)):
            if self.departureWave == "":
                tw_begin = 0
            else:
                tw_begin = time_to_minutes(self.departureWave)

            if self.vehicles[i]["maxWeight"] >= 0 or weight_or_cubic(self.orders) == 0:
                self.m.add_vehicle_type(capacity=self.vehicles[i]["maxWeight"] * 10000,
                                   name=self.vehicles[i]["vehicleId"],
                                   tw_early=tw_begin,
                                   unit_distance_cost=self.vehicles[i]["mileageCost"])

            elif self.vehicles[i]["maxVolume"] >= 0 or weight_or_cubic(self.orders) == 1:
                self.m.add_vehicle_type(capacity=self.vehicles[i]["maxVolume"] * 10000,
                                       name=self.vehicles[i]["vehicleId"],
                                       tw_early=tw_begin,
                                       unit_distance_cost=self.vehicles[i]["mileageCost"])

        depot = self.m.add_depot(x=self.depot["latitude"], y=self.depot["longitude"], name=self.depot["branchId"])

        weight_or_cubic = weight_or_cubic(self.orders)
        clients = []
        for i in range(len(self.orders)):
            if self.orders[i]['timeWindow'] == "":
                tw_early = 0
                tw_late = 1e10
            else:
                times = self.orders[i]['timeWindow'].split("-")
                tw_early = time_to_minutes(times[0])
                tw_late = time_to_minutes(times[1])

            if self.orders[i]["weight"] >= 0 or weight_or_cubic == 0:
                #print(self.data.orders[i]["lonLat"][0])
                client = self.m.add_client(x=self.orders[i]["lonLat"][0],
                                  y=self.orders[i]["lonLat"][1],
                                  delivery=self.orders[i]["weight"],
                                  service_duration = self.orders[i]["weight"] /self.config["DELIVERY_LOADING_SPEED"],
                                  tw_early = tw_early,
                                  tw_late = tw_late ,
                                  name=self.orders[i]['orderNo'])

            '''if self.data.orders[i]["cubic"] >= 0 or weight_or_cubic == 1:
                self.m.add_client(x=self.data.orders[i]["lonLat"][0],
                                  y=self.data.orders[i]["lonLat"][1],
                                  delivery=self.data.orders[i]["cubic"],
                                  service_duration = self.data.orders[i]["cubic"]/self.data.config["LOADING_SPEED"],
                                  tw_early = tw_early,
                                  tw_late = tw_late,
                                  name=self.data.orders[i]['orderNo'])'''
            clients.append(client)

        locations = [depot] + clients
        for frm in locations:
            for to in locations:
                distance = self.distance_matrix[frm.name, to.name] * 10000  # Manhattan
                duration = (self.distance_matrix[frm.name, to.name] * 60)/self.config["ROS_VEHICLE_SPEED"]
                self.m.add_edge(frm, to, distance=distance,  duration = duration)

    def solve(self):
        """
        调用pyvrp当中的混合遗传算法进行求解
        return Result
        class Result:
            best: Solution
            stats: Statistics
            num_iterations: int
            runtime: float
        """
        res = self.m.solve(stop=MaxRuntime(10), display=True)
        if res.is_feasible():
            self.solution_status = "feasible"
        else:
            self.solution_status = 'infeasible'
        return res

