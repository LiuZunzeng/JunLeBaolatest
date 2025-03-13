# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from data import Data
import os
import time

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
parent_path = os.path.dirname(root_path)


class Solution:
    """
    A class to represent a solution to the TSP problem, including visualization and output generation.
    """

    def __init__(self, data: Data, res):
        """
        Initialize the Solution class.

        Args:
        data (Data): An instance of the Data class containing node information and distances.
        routes (list): A list of routes, where each route is a list of node IDs.
        tasks (list): A list of tasks, where each task is a dictionary containing route and vehicle information.
        """
        self.data = data
        self.solution = res

    def visualize(self):
        """
        Visualize the solution using matplotlib.
        """
        print("\n\n=================================Drawing the Graph======================================")
        plt.figure(0)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("Solution")
        lonLat_depot = self.data.depot["lonLat"]
        plt.scatter(lonLat_depot[0], lonLat_depot[1], c='blue', alpha=1, marker=',',
                    linewidths=3, label='depot')
        for i in range(len(self.data.orders)):
            lonLat = self.data.orders[i]["lonLat"]
            plt.scatter(lonLat[0], lonLat[1], c='black', alpha=1, marker='o', s=15,
                        linewidths=3)

        lonLat_lst = []
        lonLat_lst.append(self.data.depot["lonLat"])
        for i in range(len(self.data.orders)):
            lonLat_lst.append(self.data.orders[i]["lonLat"])
        colors = ['red', 'green', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'brown', 'pink']
        ind = 0
        for route in self.solution.best.routes():
            color = colors[ind % len(colors)]
            p = 0
            for i in route.visits():
                x = [lonLat_lst[p][0], lonLat_lst[i][0]]
                y = [lonLat_lst[p][1], lonLat_lst[i][1]]
                plt.plot(x, y, color, linewidth=2)
                p = i
            ind += 1
            if self.data.config["RETURN_FLAG"] == True:
                x = [lonLat_lst[p][0], lonLat_lst[0][0]]
                y = [lonLat_lst[p][1], lonLat_lst[0][1]]
                plt.plot(x, y, color, linewidth=2)

        plt.grid(False)
        plt.legend(loc='upper right')
        plt.savefig(f"{parent_path}/output/" + str(time.time()) + ".png", bbox_inches='tight')
        plt.show(block=False)

    def write_result(self):
        """
        Write the solution to a JSON file.
        """
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

        def minutes_to_time(total_minutes):
            '''
            将分钟数转换为时间字符串，格式为 "小时:分钟"
            '''
            # 计算小时数
            hours = total_minutes // 60
            # 计算剩余分钟数
            minutes = total_minutes % 60
            # 格式化为字符串，确保分钟数始终为两位数
            time_str = f"{int(hours)}:{int(minutes):02d}"
            return time_str

        fetch_result = {}

        if not self.solution.is_feasible():
            fetch_result["code"] = 2
            fetch_result["result"] = None

        else:
            node_lst = []
            node_lst.append(self.data.depot["deName"])
            for i in range(len(self.data.orders)):
                node_lst.append(self.data.orders[i]["orderNo"])
            vehicle_lst = []
            for i in range(len(self.data.vehicles)):
                vehicle_lst.append(self.data.vehicles[i]["vehicleId"])
            # 整理求解结果
            fetch_result['code'] = 0
            fetch_result['result'] = []
            for route in self.solution.best.routes():
                p = 0
                ind = 1
                time = time_to_minutes(self.data.vehicles[route.vehicle_type() - 1]['departureTime'])
                for i in route.visits():
                    distance = self.data.distance_matrix[node_lst[p], node_lst[i]]
                    p = i
                    time = time + (distance * 60) / self.data.config["SPEED"]
                    eta = minutes_to_time(time)
                    time = time + self.data.orders[i - 1]["weight"] /self.data.config["LOADING_SPEED"]
                    etd = minutes_to_time(time)
                    fetch_result['result'].append({"vehicleId": vehicle_lst[route.vehicle_type() - 1],
                                                   "orderNo": self.data.orders[i - 1]["orderNo"],
                                                   "seq": ind,
                                                   "lonLat": self.data.orders[i - 1]["lonLat"],
                                                   "addressNo": self.data.orders[i - 1]["addressNo"],
                                                   "eta": eta,
                                                   "etd": etd,
                                                   "distance": distance})
                    ind += 1

        # Write the result to a JSON file
        return fetch_result
