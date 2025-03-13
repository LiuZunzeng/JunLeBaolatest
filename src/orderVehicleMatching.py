# -*- coding:utf-8 -*-
"""
@Time:2025/3/8
@Auth:Liu Zunzeng
@File:orderVehicleMatching.py
"""

class orderVehicleMatcher:
    '''
        目的：订单与车型匹配模块旨在根据订单的重量、体积和允许的最大车型，将订单合理分配到合适的车辆上，同时考虑车辆的装载率和运输成本，以优化物流配送效率。
        约束：（1）每个订单只能分配到其允许的最大车型或更小的车型；（2）车辆的总订单重量不得超过其最大载重；（3）车辆的总订单体积不得超过其最大容量。
    '''
    def __init__(self,
                 orders,
                 vehicles):
        '''
        orders:[
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
                "qtyPlanned": 10, //
                "grossWeightPlanned": 15.5, //
                "cubicPlanned": 42.7, //
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
                        "cube": 3.1,
                        "qtyPlanned": 2, //
                        "grossWeightPlanned": 2.0, //
                        "cubicPlanned": 6.2 //
                        }
                ]
            }
        ]
        vehicles: [
            {
                "vehicleId": "VE0000000215",
                "licensePlateNo": "沪A88888",
                "vehicleType": "Type1",
                "vehicleTypeId": "Type1",
                "vehicleTypeDescr1": "9.6米车型",
                "loadCapacityMin": 10.0,
                "loadCapacity": 16.0,
                "capacity": 40.0,
                "temperatureType": "冷藏"
            }
        ]
        '''
        self.orders = orders
        self.vehicles = vehicles
        self.beta = 0.8 #控制车辆装载率的阈值（例如0.8，表示车辆装载率低于80%时触发重新排线）

    def match_least_underload(self) -> list:
        '''
        1 初始化
            创建一个空的重排订单列表：rearrangement_list
            初始化underload_distance为0
        2 按订单允许的最大车型分类
            遍历订单列表，根据订单允许的最大车型对订单进行分类，将同一类订单存储在一个子列表中
        3 对每一类订单调用排线模块
            遍历每一类订单：
                调用排线模块，输入为当前类订单允许使用的车辆列表
            从排线模块的结果中获取以下信息：
                每辆车装载的订单列表
                每辆车的总订单重量
                所有路线的总距离
        4 检查车辆装载率并处理欠载情况
            遍历每个排线结果：
                找出当前排线结果中（最大载重 - 总订单重量）最大的车辆
                判断该车辆的总订单重量 / 车辆最大载重是否小于β
                如果小于β：
                    underload_distance += 这条路线的长度
                    将这辆车装载的所有订单存入rearrangement_list
        5 对重排订单列表执行排线模块
            如果rearrangement_list不为空：
                确定rearrangement_list中允许最大车型最小的订单所允许的车辆列表
                调用排线模块，输入为上述车辆列表
                将排线模块的结果合并到最终排线结果中

        return [Result, Result...]
        class Result:
            best: Solution
            stats: Statistics
            num_iterations: int
            runtime: float
        '''
