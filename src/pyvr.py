# -*- coding:utf-8 -*-
"""
@Time:2024/6/4
@Auth:Liu Zunzeng
@File:pyVRP.py
"""
from pyvrp import Model  # 用于创建和解决VRP问题的模型
from data.data import Data  # 包含数据读取和处理的类
import matplotlib.pyplot as plt  # 用于绘图的库
from solution import Solution  # 用于输出解决方案的类
import json  # 用于处理JSON数据的库
from pyvrp.stop import MaxRuntime  # 用于设置求解器的最大运行时间

# 定义一个函数，用于调用pyvrp库来解决VRP问题
def call_pyvry(data):
    m = Model()  # 创建一个模型实例
    # 为每种车辆类型添加车辆
    for key, value in data.vehicle_dic.items():
        m.add_vehicle_type(capacity=value[1] * 100000000, name=key)
        # m.add_vehicle_type(capacity=value[2] * 10000, name=key)  # 这行代码被注释掉了

    # 添加仓库（起点）
    depot = m.add_depot(x=data.depot.lonLat[0], y=data.depot.lonLat[1], name='start')
    # 为客户添加订单
    clients = [
        m.add_client(x=value[0], y=value[1], delivery=data.weight_dic[key] * 10000, name=key)
        for key, value in data.order_dic.items()]

    # 获取所有位置（仓库和客户）
    locations = [depot] + clients
    # 为每对位置添加边（距离）
    for frm in locations:
        for to in locations:
            distance = data.distance[frm.name, to.name] * 10000  # Manhattan距离
            m.add_edge(frm, to, distance=distance)

    '''from pyvrp.plotting import plot_coordinates

    _, ax = plt.subplots(figsize=(8, 8))
    plot_coordinates(m.data(), ax=ax)'''  # 这一段代码被注释掉了，用于绘制坐标图

    # 解决VRP问题，设置最大运行时间为3秒，显示求解过程
    res = m.solve(stop=MaxRuntime(3), display=True)
    return res  # 返回求解结果

# 定义一个函数，用于输出解决方案
def output(res, data):
    tasks = []  # 存储任务信息
    routes = []  # 存储路线信息
    orderName = list(data.order_dic.keys())  # 获取订单名称列表
    # 遍历最佳路线
    for route in res.best.routes():
        task = {}  # 创建一个任务字典
        route1 = ["start"]  # 创建一个路线列表，以起点开始
        # 遍历路线中的访问点
        for i in route.visits():
            route1.append(orderName[i - 1])
        route1.append("end")  # 以终点结束
        routes.append(route1)  # 添加到路线列表
        task['运输路线'] = route1  # 添加路线信息到任务字典
        task['总距离'] = route.distance()/10000  # 添加总距离信息到任务字典
        task['车辆ID'] = list(data.vehicle_dic.keys())[route.vehicle_type()]  # 添加车辆ID信息到任务字典
        tasks.append(task)  # 添加任务字典到任务列表
    print(tasks)  # 打印任务列表

    # 创建Solution实例，用于进一步处理和输出解决方案
    s = Solution(data, routes, tasks)
    s.visualize()  # 可视化解决方案
    s.write_excel()  # 将解决方案写入Excel文件
    s.visualize_map_gaode()  # 使用高德地图可视化解决方案
    # result = s.write_file()  # 这行代码被注释掉了，用于将解决方案写入文件

# 定义一个函数，用于启动整个VRP求解过程
def pyvrp_start():
    data = Data()  # 创建Data实例
    data.read_excel()  # 从Excel文件读取数据
    data.read_order()  # 读取订单数据
    data.add_depot()  # 添加仓库信息
    # data.calculate_distance()  # 这行代码被注释掉了，用于计算距离
    data.read_from_json()  # 从JSON文件读取数据
    # print(data.distance)  # 打印距离信息
    res = call_pyvry(data)  # 调用call_pyvry函数求解VRP问题
    output(res, data)  # 输出解决方案

if __name__ == '__main__':
    pyvrp_start()

