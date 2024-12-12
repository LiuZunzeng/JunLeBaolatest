# -*- coding:utf-8 -*-
"""
@Time:2024/5/24
@Auth:Liu Zunzeng
@File:Solution.py
"""
import matplotlib.pyplot as plt
import os
from data.data import Data
import pandas as pd
from map_display import Route_display
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)

class Solution:

    def __init__(self, data: Data, routes, tasks):
        self.data = data
        self.m = 0
        self.routes = routes
        self.routeNum = len(routes)
        self.tasks = tasks

    def visualize(self):

        print("\n\n===============================Drawing the Graph========================================")
        plt.figure(0)
        plt.xlabel('lat')
        plt.ylabel('lon')
        plt.title("Solution")
        plt.scatter(self.data.node_dic['start'][0], self.data.node_dic['start'][1], c='blue', alpha=1, marker=',',
                    linewidths=3, label='Depot')
        for i in self.data.order_dic.keys():
            plt.scatter(self.data.node_dic[i][0], self.data.node_dic[i][1], c='black', alpha=1, marker='o', s=15,
                        linewidths=3)
        colors = ['red', 'green', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'brown', 'pink']

        for k in range(self.routeNum):
            color = colors[k % len(colors)]
            for i in range(len(self.routes[k]) - 1):
                a = self.routes[k][i]
                b = self.routes[k][i + 1]
                x = [self.data.node_dic[a][0], self.data.node_dic[b][0]]
                y = [self.data.node_dic[a][1], self.data.node_dic[b][1]]
                plt.plot(x, y, color, linewidth=2)

        plt.grid(False)
        plt.legend(loc='upper right')

        plt.savefig(f"{parent_path}/output/" + "配送方案" + ".png", bbox_inches='tight')

        plt.show(block=False)

    def visualize_map_gaode(self):
        '''
        配送方案在高德地图中的可视化
        '''
        route = []
        for i in range(self.routeNum):
            route_dic = {}
            self.routes[i].pop()
            for add in self.routes[i]:
                if add == '鹿泉区石铜路36号':
                    route_dic[add] = self.data.node_dic['start']
                else:
                    route_dic[add] = self.data.node_dic[add]
            route.append(route_dic)
        map = Route_display(route, map_center=self.data.node_dic['start'])
        map.draw()
        map.save('../src/static/11月2日路线图.html')

    def write_excel(self):
        '''
        将配送方案写入excel
        '''
        df = pd.read_excel(f"{parent_path}/input/智能排线测算1101.xlsx", sheet_name="运费", engine='openpyxl')
        info = df.to_dict('records')
        cost_info = {}
        for i in info:
            cost_info[i['结算点']] = (i['里程数'], i['供应商提报价格（冷藏）元/吨.公里'])
        for ind in range(len(self.tasks)):
            self.tasks[ind]['运输路线'].pop(0)
            self.tasks[ind]['运输路线'].pop()
            total_weight = 0
            total_cubic = 0
            for address in self.tasks[ind]['运输路线']:
                total_weight += self.data.weight_dic[address]
                total_cubic += self.data.cubic_dic[address]
            customer_route = []
            city_route = []
            for address in self.tasks[ind]['运输路线']:
                customer_route.append(self.data.customer_orders[address])
                city_route.append(self.data.city_dic[address])
            self.tasks[ind]['客户路线'] = customer_route
            self.tasks[ind]['城市路线'] = city_route
            self.tasks[ind]['货物总重量'] = total_weight
            self.tasks[ind]['货物总体积'] = total_cubic
            if city_route[-1][-1].isdigit():
                lastcity = city_route[-1][:-1]
            else:
                lastcity = city_route[-1]
            self.tasks[ind]['供应商提报价格（冷藏）元/吨.公里']  = cost_info[lastcity][1]
            self.tasks[ind]['费用'] = self.tasks[ind]['总距离'] * self.tasks[ind]['货物总重量'] * cost_info[lastcity][1]
            self.tasks[ind]['车辆载重'] = self.data.vehicle_dic[self.tasks[ind]['车辆ID']][1]
            self.tasks[ind]['车辆容量'] = self.data.vehicle_dic[self.tasks[ind]['车辆ID']][0]
            self.tasks[ind]['运输路线'].insert(0, self.data.depot.address)
            self.tasks[ind]['运输路线'].append(self.data.depot.address)
        # 将任务列表转换为DataFrame
        df = pd.DataFrame(self.tasks)
    
        # 将DataFrame写入Excel文件
        df.to_excel(f'{parent_path}/output/tasks.xlsx', index=False)





