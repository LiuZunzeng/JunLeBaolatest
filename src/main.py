# -*- coding:utf-8 -*-
"""
@Time:2025/1/18
@Auth:Liu Zunzeng
@File:main.py.py
"""
from data import Data
from vrpSolver import VrpSolver
from solution import Solution
import json
import time
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)

class Solver:
    def __init__(self, data):
        """
        Initialize the Solver class with data.
        """
        self.data = Data(data)

    def start(self):
        '''
        主流程:
            遍历self.data.orders列表：
                如果所有订单允许的车辆类型都一样：
                    那么直接进入排线模块vrpSolver，
                否则：
                    进入订单车辆匹配模块orderVehicleMatcher
        '''
        self.data.calculate_distance()
        for item in self.data.dispatchZone:

            p = VrpSolver(config=self.data.config,
                          departure_wave= item['departureWave'],
                          depot= depot,
                          orders= item['orders'],
                          vehicles= item['vehicle'],
                          tariff= item['tariff'],
                          distance_matrix=self.data.distance_matrix
                          )
            #p.build_model()
            print(f"\n=========================开始求解{item['dispatchZoneCode']}区域的调度=========================\n")
            #res = p.solve()
        #S = Solution(self.data, res)
        #fetch_result = S.write_result()
        #S.visualize()
        fetch_result = {
                            "success": True,
                            "code": "10000",
                            "msg": "成功",
                            "results": [
                                {
                                    "dispatchId": "DIS0001",
                                    "waybillNo": "BIL001",
                                    "vehicleId": "VE0000000215",
                                    "vehicleType": "Type1",
                                    "temperatureType": "冷藏",
                                    "ETD": "00:00",
                                    "vehicleLeaveSeq": 1,
                                    "routeNoRos": "R0001",
                                    "routeNameRos": "石家庄-济南-潍坊-青岛",
                                    "totalMile": 390.0,
                                    "vehicleVolumeRatio": 0.69,
                                    "vehicleWeightRatio": 0.99,
                                    "orders": [
                                        {
                                            "taskNo": "PO001-2",
                                            "orderNo": "PO001",
                                            "seq": 1,
                                            "eta": "2025-03-04T10:00",
                                            "etd": "2025-03-04T10:20",
                                            "distance": 16.0,
                                            "duration": 0.36,
                                            "qty": 10,
                                            "grossWeight": 15.5,
                                            "cubic": 42.7,
                                            "qtyPlanned": 10,
                                            "grossWeightPlanned": 15.5,
                                            "cubicPlanned": 42.7,
                                            "goods": [
                                                {
                                                    "taskNo": "PO001-2",
                                                    "taskLineNo": "1",
                                                    "sku": "210001",
                                                    "skuDescr1": "老酸奶",
                                                    "qty": 2,
                                                    "grossweight": 2.0,
                                                    "cubic": 6.2,
                                                    "qtyPlanned": 2,
                                                    "grossWeightPlanned": 2.0,
                                                    "cubicPlanned": 6.2
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
        }
        with open(f"{parent_path}/output/output_{time.time()}.json", 'w', encoding='utf-8') as f:
            json.dump(fetch_result, f, ensure_ascii=False, indent=4)

        return fetch_result
