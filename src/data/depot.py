# -*- coding:utf-8 -*-
"""
@Time:2024/5/29
@Auth:Liu Zunzeng
@File:Depot.py
"""
class depot:
    #def __init__(self, address, deName, province, city, addressNo, district, deCode, lonLat):
    def __init__(self, address, addressNo, lonLat):
        self.address = address
        #self.deName = deName
        #self.province = province
        #self.city = city
        self.addressNo = addressNo
        #self.district = district
        #self.deCode = deCode
        self.lonLat = lonLat