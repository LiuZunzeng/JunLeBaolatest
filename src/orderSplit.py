# -*- coding:utf-8 -*-
"""
@Time:2025/3/8
@Auth:Liu Zunzeng
@File:orderSplit.py
"""

class OrderSplitter:
    '''
    拆单模块：
    1. 目的：在物流配送过程中，当订单的重量或体积超出其允许的最大车型（如9.6米车型）的最大载重或最大容量时，需对订单进行拆分，以满足运输要求。
    2. 约束：（1）拆分后的每个子订单的总重量不得超过最大载重；（2）拆分后的每个子订单的总体积不得超过最大容量; （3）尽量将相同温控类型的SKU放在一起
    '''
    def __init__(self,
                 orders: list,
                 vehicles: list):
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

        def split_according_to_largest(self) -> list:
            '''
            遍历self.orders中的每个订单，如果订单总重量（体积）超过了 "vehicleCategory"里面最大车型的最大载重(最大容量)，执行以下算法流程：
            1. 初始化
                创建一个空的子订单列表，用于存放拆分后的子订单。
                创建一个临时子订单，用于逐步构建当前正在处理的子订单，初始化其总重量、总体积为0，SKU列表为空。
            2. 按温控类型对SKU分组
                遍历订单中的SKU列表，根据SKU的温控类型将它们分为常温组和低温组。
                优先处理常温组的SKU，将它们按重量或体积从大到小排序（可根据实际情况选择排序依据）。
                然后处理低温组的SKU，同样按重量或体积从大到小排序。
                将两个SKU列表合成一个
            3. 构建子订单
                循环开始：依次处理SKU列表中的每个SKU。
                    判断是否能直接加入当前子订单：
                        如果当前子订单加上该SKU的总重量不超过最大载重且总体积不超过最大容量，则将该SKU加入当前子订单，更新当前子订单的总重量和总体积。
                        如果不能直接加入，对SKU进行拆分：
                            计算当前SKU在当前子订单中最多能加入的数量，即根据最大载重和最大容量的限制，分别计算出重量和体积允许的最大数量，取两者的较小值作为实际可加入的数量。
                            将这部分SKU加入当前子订单，更新当前子订单的总重量和总体积。
                            从原SKU中移除已加入子订单的SKU数量，如果该SKU剩余数量为0，则从列表中移除该SKU。
                            将当前子订单加入子订单列表，创建一个新的临时子订单，继续处理剩余的SKU。

            return: 拆分后的子订单列表suborders
            suborders:[
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
            '''

