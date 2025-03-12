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
                创建一个临时子订单，用于逐步构建当前正在处理的子订单，初始化其计划总重量、计划总体积为0，SKU列表为空。
            2. 按温控类型对SKU分组
                遍历订单中的SKU列表，根据SKU的温控类型将它们分为常温组和低温组。
                优先处理常温组的SKU，将它们按重量或体积从大到小排序（可根据实际情况选择排序依据）。
                然后处理低温组的SKU，同样按重量或体积从大到小排序。
                将两个SKU列表合成一个
            3. 构建子订单
                循环开始：依次处理SKU列表中的每个SKU。
                    判断是否能直接加入当前子订单：
                        如果当前子订单加上该SKU的重量不超过最大载重且总体积不超过最大容量，则将该SKU加入当前子订单，更新当前子订单的计划总重量和计划总体积。
                        如果不能直接加入，对SKU进行拆分：
                            计算当前SKU在当前子订单中最多能加入的数量，即根据最大载重和最大容量的限制，分别计算出重量和体积允许的最大数量，取两者的较小值作为实际可加入的数量。
                            将这部分SKU加入当前子订单，更新当前子订单的计划总重量和计划总体积。
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
        result_suborders = []
        
        # 遍历每个订单
        for order in self.orders:
            # 获取可用车型中最大的载重和容量
            max_vehicle = self._get_max_vehicle_capacity(order['vehicleCategory'])
            max_weight = max_vehicle['loadCapacity']
            max_cubic = max_vehicle['capacity']
            
            # 检查是否需要拆分
            total_weight = order['weight']
            total_cubic = order['cubic']
            
            if total_weight <= max_weight and total_cubic <= max_cubic:
                # 不需要拆分的订单，设置计划量等于实际量
                order['qtyPlanned'] = order['qty']
                order['grossWeightPlanned'] = order['weight']
                order['cubicPlanned'] = order['cubic']
                for sku in order['ordersDetails']:
                    sku['qtyPlanned'] = sku['qty']
                    sku['grossWeightPlanned'] = sku['grossWeight']
                    sku['cubicPlanned'] = sku['cubic']
                result_suborders.append(order)
                continue
            
            # 按温控类型对SKU分组并排序
            normal_temp_skus = []
            low_temp_skus = []
            
            for sku in order['ordersDetails']:
                if sku['temperatureType'] == '常温':
                    normal_temp_skus.append(sku)
                else:
                    low_temp_skus.append(sku)
            
            # 按重量和体积排序（这里使用重量作为主要排序依据）
            normal_temp_skus.sort(key=lambda x: x['weight'], reverse=True)
            low_temp_skus.sort(key=lambda x: x['weight'], reverse=True)
            
            # 合并SKU列表，优先处理常温商品
            sorted_skus = normal_temp_skus + low_temp_skus
            
            # 开始构建子订单
            current_suborder = self._create_empty_suborder(order)
            
            for sku in sorted_skus:
                remaining_qty = sku['qty']
                while remaining_qty > 0:
                    # 计算当前子订单还能容纳多少数量
                    weight_capacity = (max_weight - current_suborder['grossWeightPlanned']) / sku['grossWeight']#剩余重量/单位重量
                    cubic_capacity = (max_cubic - current_suborder['cubicPlanned']) / sku['cube']#剩余容量/单位容量
                    available_qty = min(int(weight_capacity), int(cubic_capacity), remaining_qty)
                    
                    if available_qty <= 0:
                        # 当前子订单已满，创建新的子订单
                        result_suborders.append(current_suborder)
                        current_suborder = self._create_empty_suborder(order)
                        continue
                    
                    # 创建新的SKU明细并添加到子订单中
                    new_sku = self._create_sku_detail(sku, available_qty)
                    current_suborder['ordersDetails'].append(new_sku)
                    
                    # 只更新计划相关的字段
                    current_suborder['qtyPlanned'] += available_qty
                    current_suborder['grossWeightPlanned'] += new_sku['grossWeightPlanned']
                    current_suborder['cubicPlanned'] += new_sku['cubicPlanned']
                    
                    remaining_qty -= available_qty
                
            # 添加最后一个子订单
            if current_suborder['qtyPlanned'] > 0:
                result_suborders.append(current_suborder)
            
        return result_suborders

    def _get_max_vehicle_capacity(self, vehicle_categories):
        """获取可用车型中最大的载重和容量"""
        categories = [cat.strip() for cat in vehicle_categories.split(',')]
        max_vehicle = {
            'loadCapacity': 0,
            'capacity': 0
        }
        
        for vehicle in self.vehicles:
            if vehicle['vehicleType'] in categories:
                if vehicle['loadCapacity'] > max_vehicle['loadCapacity']:
                    max_vehicle = vehicle
        
        return max_vehicle

    def _create_empty_suborder(self, original_order):
        """创建空的子订单，复制原订单的基本信息"""
        suborder = original_order.copy()
        # 保持原始订单的qty、weight、cubic不变
        # 只初始化计划相关的字段
        suborder.update({
            'qtyPlanned': 0,
            'grossWeightPlanned': 0,
            'cubicPlanned': 0,
            'ordersDetails': []
        })
        return suborder

    def _create_sku_detail(self, original_sku, planned_qty):
        """创建新的SKU明细"""
        sku_detail = original_sku.copy()
        # 保持原始SKU的qty、weight、cubic不变
        # 只更新计划相关的字段
        sku_detail.update({
            'qtyPlanned': planned_qty,
            'grossWeightPlanned': original_sku['grossWeight'] * planned_qty,
            'cubicPlanned': original_sku['cube'] * planned_qty
        })
        return sku_detail

if __name__ == "__main__":
    # 测试数据
    test_vehicles = [
        {
            "vehicleId": "V001",
            "licensePlateNo": "沪A11111",
            "vehicleType": "6T",
            "vehicleTypeId": "6T",
            "vehicleTypeDescr1": "6吨车型",
            "loadCapacityMin": 0.0,
            "loadCapacity": 6.0,
            "capacity": 30.0,
            "temperatureType": "常温"
        },
        {
            "vehicleId": "V002",
            "licensePlateNo": "沪A22222",
            "vehicleType": "10.5T",
            "vehicleTypeId": "10.5T",
            "vehicleTypeDescr1": "10.5吨车型",
            "loadCapacityMin": 6.0,
            "loadCapacity": 10.5,
            "capacity": 50.0,
            "temperatureType": "常温"
        },
        {
            "vehicleId": "V003",
            "licensePlateNo": "沪A33333",
            "vehicleType": "16T",
            "vehicleTypeId": "16T",
            "vehicleTypeDescr1": "16吨车型",
            "loadCapacityMin": 10.5,
            "loadCapacity": 16.0,
            "capacity": 60.0,
            "temperatureType": "常温"
        }
    ]

    test_order = {
        "dispatchZoneCode": "DISZONE001",
        "taskNo": "PO001",
        "orderNo": "PO001",
        "DC": "WH01",
        "orderType": "D",
        "createTime": "2025-03-04T10:00",
        "qty": 400,
        "weight": 40.0,
        "cubic": 120.0,
        "money": 100000.0,
        "bulkFlag": 1,
        "routeNo": "",
        "routeNoNext": "",
        "offeringType": "汽运",
        "temperatureClass": "常温",
        "addressNo": "ADDR001",
        "address": "上海市浦东新区张江高科技园区",
        "timeWindowFrom": "00:00",
        "timeWindowTo": "23:59",
        "vehicleCategory": "6T,10.5T,16T",
        "longitude": "121.50389",
        "latitude": "31.29665",
        "consigneeId": "A001",
        "companyClass": "0点",
        "availableVehicleType": "6T,10.5T,16T",
        "vehicleCategoryCus": "6T,10.5T,16T",
        "unloadingTimeWindow": "8:00-18:00",
        "nonUnloadingTimeWindow": "18:00-8:00",
        "leadTime": 24.0,
        "SDD": "1,2,3",
        "ordersDetails": [
            {
                "taskNo": "PO001",
                "taskLineNo": "1",
                "sku": "SKU001",
                "skuDescr1": "重货物品A",
                "qty": 100,
                "weight": 10.0,
                "cubic": 30.0,
                "temperatureType": "冷藏",
                "grossWeight": 0.1,
                "cube": 0.3
            },
            {
                "taskNo": "PO001",
                "taskLineNo": "2",
                "sku": "SKU002",
                "skuDescr1": "重货物品B",
                "qty": 300,
                "weight": 30.0,
                "cubic": 90.0,
                "temperatureType": "常温",
                "grossWeight": 0.1,
                "cube": 0.3
            }
        ]
    }

    # 实例化订单拆分器并执行拆分
    splitter = OrderSplitter([test_order], test_vehicles)
    result = splitter.split_according_to_largest()
    print("订单拆分结果：")
    import json
    print(json.dumps(result, indent=4, ensure_ascii=False))
    # 打印拆分结果
    print("\n=== 订单拆分结果 ===")
    for idx, suborder in enumerate(result):
        print(f"\n子订单 {idx + 1}:")
        print(f"计划数量: {suborder['qtyPlanned']}")
        print(f"计划重量: {suborder['grossWeightPlanned']:.1f}吨")
        print(f"计划体积: {suborder['cubicPlanned']:.1f}立方米")
        print("SKU明细:")
        for sku in suborder['ordersDetails']:
            print(f"- SKU: {sku['sku']}, "
                  f"计划数量: {sku['qtyPlanned']}, "
                  f"计划重量: {sku['grossWeightPlanned']:.1f}吨, "
                  f"计划体积: {sku['cubicPlanned']:.1f}立方米")

