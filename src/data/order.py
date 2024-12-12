# -*- coding:utf-8 -*-
"""
@Time:2024/5/29
@Auth:Liu Zunzeng
@File:Order.py
"""
class Order:

    #def __init__(self, orderType, bulkFlag, timeWindow, orderNo, cubic, address, dispatchZoneCode, weight, lonLat, money, addressNo, qty, taskNo, DC):
    def __init__(self, orderNo, cubic,address, weight, lonLat, addressNo, qty, city):
        #self.orderType = orderType
        #self.bulkFlag = bulkFlag
        #self.timeWindow = timeWindow
        self.orderNo = orderNo
        self.cubic = cubic
        self.address = address
        self.weight = weight
        #self.dispatchZoneCode = dispatchZoneCode
        self.lonLat = lonLat
        #self.money = money
        self.addressNo = addressNo
        self.qty = qty
        #self.taskNo = taskNo
        #self.DC = DC
        self.city = city
