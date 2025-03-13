# -*- coding:utf-8 -*-
"""
@Time:2025/3/7
@Auth:Liu Zunzeng
@File:ss.py
"""
vehicleType = [
    {
        "vehicleTypeId": "Type1",
        "vehicleTypeDescr1": "9.6米车型",
        "loadCapacityMin": 10.0,
        "loadCapacity": 16.0,
        "capacity": 40.0,
        "temperatureType": "冷藏"
    }
    # 这里可以添加更多的字典
]

vehicle = [
    {
        "vehicleId": "VE0000000215",
        "licensePlateNo": "沪A88888",
        "vehicleType": "Type1"
    }
    # 这里可以添加更多的字典
]

# 创建一个字典，用于快速查找 vehicleType 列表中的字典
vehicle_type_dict = {item["vehicleTypeId"]: item for item in vehicleType}

# 遍历 vehicle 列表，将对应的 vehicleType 字典合并进去
for vehicle_item in vehicle:
    vehicle_type_id = vehicle_item["vehicleType"]
    if vehicle_type_id in vehicle_type_dict:
        vehicle_item.update(vehicle_type_dict[vehicle_type_id])

# 输出合并后的结果
for item in vehicle:
    print(item)