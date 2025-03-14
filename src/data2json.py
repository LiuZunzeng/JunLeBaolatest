import pandas as pd
import random
from datetime import datetime
import json

class ExcelDataProcessor:
    def __init__(self, file_path):
        self.excel_file = pd.ExcelFile(file_path)
        self.config_sheetname = "配置信息"
        self.depots_sheetname = "仓库信息"
        self.vehicleType_sheetname = "车型车辆信息"
        self.orders_sheetname = "订单信息"
        self.customer_sheetname = "客户信息"
        self.tariff_sheetname = "承运商费率合同信息"
        self.dispatchZoneCode_list = ["DISZONE001"]
        self.tariff_shipper_location_info = {
            "石家庄": {"shipperProvince": "河北省", "shipperCity": "石家庄市", "shipperDistrict": ""},
        }
        self.tariff_consignee_location_info = {
            "桓台": {"consigneeProvince": "山东省", "consigneeCity": "淄博市", "consigneeDistrict": "桓台县"},
            "青州": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": "青州市"},
            "安丘": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": "安丘市"},
            "高密": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": "高密市"},
            "惠民": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "惠民县"},
            "高青": {"consigneeProvince": "山东省", "consigneeCity": "淄博市", "consigneeDistrict": "高青县"},
            "博兴": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "博兴县"},
            "济阳": {"consigneeProvince": "山东省", "consigneeCity": "济南市", "consigneeDistrict": "济阳区"},
            "济南": {"consigneeProvince": "山东省", "consigneeCity": "济南市", "consigneeDistrict": ""},
            "章丘": {"consigneeProvince": "山东省", "consigneeCity": "济南市", "consigneeDistrict": "章丘区"},
            "莱州": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "莱州市"},
            "招远": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "招远市"},
            "龙口": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "龙口市"},
            "蓬莱": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "蓬莱区"},
            "乐陵": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "乐陵市"},
            "即墨": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": "即墨区"},
            "临清": {"consigneeProvince": "山东省", "consigneeCity": "聊城市", "consigneeDistrict": "临清市"},
            "聊城": {"consigneeProvince": "山东省", "consigneeCity": "聊城市", "consigneeDistrict": ""},
            "肥城": {"consigneeProvince": "山东省", "consigneeCity": "泰安市", "consigneeDistrict": "肥城市"},
            "新泰": {"consigneeProvince": "山东省", "consigneeCity": "泰安市", "consigneeDistrict": "新泰市"},
            "蒙阴": {"consigneeProvince": "山东省", "consigneeCity": "临沂市", "consigneeDistrict": "蒙阴县"},
            "青岛": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": ""},
            "胶州": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": "胶州市"},
            "黄岛": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": "黄岛区"},
            "宁津": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "宁津县"},
            "庆云": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "庆云县"},
            "无棣": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "无棣县"},
            "沾化": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "沾化区"},
            "河口": {"consigneeProvince": "山东省", "consigneeCity": "东营市", "consigneeDistrict": "河口区"},
            "夏津": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "夏津县"},
            "高唐": {"consigneeProvince": "山东省", "consigneeCity": "聊城市", "consigneeDistrict": "高唐县"},
            "茌平": {"consigneeProvince": "山东省", "consigneeCity": "聊城市", "consigneeDistrict": "茌平区"},
            "长清": {"consigneeProvince": "山东省", "consigneeCity": "济南市", "consigneeDistrict": "长清区"},
            "泰安": {"consigneeProvince": "山东省", "consigneeCity": "泰安市", "consigneeDistrict": ""},
            "莱芜": {"consigneeProvince": "山东省", "consigneeCity": "济南市", "consigneeDistrict": "莱芜区"},
            "阳信": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "阳信县"},
            "滨州": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": ""},
            "利津": {"consigneeProvince": "山东省", "consigneeCity": "东营市", "consigneeDistrict": "利津县"},
            "广饶": {"consigneeProvince": "山东省", "consigneeCity": "东营市", "consigneeDistrict": "广饶县"},
            "东营": {"consigneeProvince": "山东省", "consigneeCity": "东营市", "consigneeDistrict": ""},
            "禹城": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "禹城市"},
            "齐河": {"consigneeProvince": "山东省", "consigneeCity": "德州市", "consigneeDistrict": "齐河县"},
            "淄博": {"consigneeProvince": "山东省", "consigneeCity": "淄博市", "consigneeDistrict": ""},
            "寿光": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": "寿光市"},
            "潍坊": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": ""},
            "昌邑": {"consigneeProvince": "山东省", "consigneeCity": "潍坊市", "consigneeDistrict": "昌邑市"},
            "威海": {"consigneeProvince": "山东省", "consigneeCity": "威海市", "consigneeDistrict": ""},
            "烟台": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": ""},
            "淄川": {"consigneeProvince": "山东省", "consigneeCity": "淄博市", "consigneeDistrict": "淄川区"},
            "邹平": {"consigneeProvince": "山东省", "consigneeCity": "滨州市", "consigneeDistrict": "邹平市"},
            "平度": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": "平度市"},
            "莱西": {"consigneeProvince": "山东省", "consigneeCity": "青岛市", "consigneeDistrict": "莱西市"},
            "莱阳": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "莱阳市"},
            "海阳": {"consigneeProvince": "山东省", "consigneeCity": "烟台市", "consigneeDistrict": "海阳市"}
        }
        self.config=dict()
        self.depots=[]
        self.dispatchZone=[]
        self.orders=[]
        self.vehicleType=[]

    def process_config(self):
        config_df = self.excel_file.parse(self.config_sheetname)
        config_df["卸货速度（吨/小时）"] = config_df["卸货速度（吨/小时）"].astype("float")
        config_df["车辆最少停留时间（分钟）"] = config_df["车辆最少停留时间（分钟）"].astype("float")
        config_df["车速（千米/小时）"] = config_df["车速（千米/小时）"].astype("float")

        self.config["DELIVERY_LOADING_SPEED"] = config_df["卸货速度（吨/小时）"][0] // 60
        self.config["DELIVERY_STAY_MINUTE"] = config_df["车辆最少停留时间（分钟）"][0]
        self.config["ROS_VEHICLE_SPEED"] = config_df["车速（千米/小时）"][0]
        self.config["ROS_SPLIT_ORDER"] = "Y"
        self.config["ROS_NORMAL_TEMPERATURE_RATIO"] = 0.99

    def process_depots(self):
        depots_df = self.excel_file.parse(self.depots_sheetname)
        depots_df['仓库名称'] = depots_df['仓库名称'].astype("str")
        depots_df['仓库地址'] = depots_df['仓库地址'].astype("str")
        depots_df['地址编号'] = depots_df['地址编号'].astype("str")
        depots_df['仓库经纬度'] = depots_df['仓库经纬度'].astype("str")
        depots_df[['longitude', 'latitude']] = depots_df['仓库经纬度'].str.split(',', expand=True)

        for index, depot_info in depots_df.iterrows():
            depot = dict()
            depot["branchId"] = depot_info["地址编号"]
            depot["branchDesr"] = depot_info["仓库名称"]
            depot["longitude"] = depot_info["longitude"]
            depot["latitude"] = depot_info["latitude"]
            depot["notes"] = "note"
            depot["brach_status"] = "1"
            self.depots.append(depot)

    def __process_vehicle_type(self):
        normal_vehicleType_df = self.excel_file.parse(self.vehicleType_sheetname)
        Refrigerate_vehicleType_df = self.excel_file.parse(self.vehicleType_sheetname)
        normal_vehicleType_df["车辆温控类型"] = "常温"
        Refrigerate_vehicleType_df["车辆温控类型"] = "冷藏"
        vehicleType_df = pd.concat([normal_vehicleType_df, Refrigerate_vehicleType_df], ignore_index=True)
        vehicleType_df["车型编号"] = ['Type' + str(index + 1) for index in vehicleType_df.index]

        vehicleType_df["车辆类型"] = vehicleType_df["车辆类型"].astype("str")
        vehicleType_df["最小载重（吨）"] = vehicleType_df["最小载重（吨）"].astype("float")
        vehicleType_df["最大载重（吨）"] = vehicleType_df["最大载重（吨）"].astype("float")
        vehicleType_df["最大容量（立方米）"] = vehicleType_df["最大容量（立方米）"].astype("float")

        vehicleType_list = list()
        for index, vehicleType_info in vehicleType_df.iterrows():
            vehicleType = dict()
            vehicleType["vehicleTypeId"] = vehicleType_info["车型编号"]
            vehicleType["vehicleTypeDescr1"] = vehicleType_info["车辆类型"]
            vehicleType["loadCapacityMin"] = vehicleType_info["最小载重（吨）"]
            vehicleType["loadCapacity"] = vehicleType_info["最大载重（吨）"]
            vehicleType["capacity"] = vehicleType_info["最大容量（立方米）"]
            vehicleType["temperatureType"] = vehicleType_info["车辆温控类型"]
            self.vehicleType.append(vehicleType)

    def __process_vehicles(self):
        shandong_prefixes = ['鲁A', '鲁B', '鲁C', '鲁D', '鲁E', '鲁F', '鲁G', '鲁H', '鲁J', '鲁K', '鲁L', '鲁M', '鲁N',
                             '鲁P', '鲁Q', '鲁R', '鲁S', '鲁U', '鲁V', '鲁W', '鲁X', '鲁Y']
        vehicle_id_start = 1
        vehicle_types = [f'Type{i}' for i in range(1, 9)]
        vehicle_list = []
        for vehicle_type in vehicle_types:
            for _ in range(50):
                vehicle_id = f"VE{str(vehicle_id_start).zfill(10)}"
                vehicle_id_start += 1
                license_plate_prefix = random.choice(shandong_prefixes)
                license_plate_suffix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))
                license_plate_no = license_plate_prefix + license_plate_suffix
                vehicle_info = {
                    "vehicleId": vehicle_id,
                    "licensePlateNo": license_plate_no,
                    "vehicleType": vehicle_type
                }
                vehicle_list.append(vehicle_info)
        return vehicle_list

    def __process_tariff(self):
        normal_tariff_df = self.excel_file.parse(self.tariff_sheetname)
        Refrigerate_tariff_df = self.excel_file.parse(self.tariff_sheetname)
        normal_tariff_df["运输温控方式"] = "常温"
        normal_tariff_df = normal_tariff_df.iloc[1:, :].drop('冷藏报价', axis=1).rename(columns={'非冷藏报价': '单价'})
        Refrigerate_tariff_df["运输温控方式"] = "冷藏"
        Refrigerate_tariff_df = Refrigerate_tariff_df.iloc[1:, :].drop('非冷藏报价', axis=1).rename(columns={'冷藏报价': '单价'})
        tariff_df = pd.concat([normal_tariff_df, Refrigerate_tariff_df], ignore_index=True)
        tariff_df["计价基准"] = tariff_df['计价单位'].apply(lambda x: '吨公里' if x == '元/吨.公里' else None)
        tariff_df["始发地地点"] = tariff_df['线路'].apply(lambda x: x.split('-')[0])
        tariff_df["目的地地点"] = tariff_df['线路'].apply(lambda x: x.split('-')[-1])
        tariff_df["合同协议编码"] = tariff_df["合同协议编码"].astype("str")
        tariff_df["线路"] = tariff_df["线路"].astype("str")
        tariff_df["运输方式"] = "整车运输"
        tariff_df["始发地地点"] = tariff_df['线路'].apply(lambda x: x.split('-')[0])
        tariff_df["目的地地点"] = tariff_df['线路'].apply(lambda x: x.split('-')[-1])
        tariff_df["运输温控方式"] = tariff_df["运输温控方式"].astype("str")
        tariff_df["里程"] = tariff_df["里程"].astype("float")
        tariff_df["计价基准"] = tariff_df["计价基准"].astype("str")
        tariff_df["单价"] = tariff_df["单价"].astype("float")

        tariff_list = list()
        for index, tariff_info in tariff_df.iterrows():
            tariff = dict()
            tariff["tariffID"] = tariff_info["合同协议编码"]
            tariff["offeringType"] = tariff_info["运输方式"]
            tariff["shipperProvince"] = self.tariff_shipper_location_info[tariff_info["始发地地点"]]["shipperProvince"]
            tariff["shipperCity"] = self.tariff_shipper_location_info[tariff_info["始发地地点"]]["shipperCity"]
            tariff["shipperDistrict"] = self.tariff_shipper_location_info[tariff_info["始发地地点"]]["shipperDistrict"]
            tariff["consigneeProvince"] = self.tariff_consignee_location_info[tariff_info["目的地地点"]]["consigneeProvince"]
            tariff["consigneeCity"] = self.tariff_consignee_location_info[tariff_info["目的地地点"]]["consigneeCity"]
            tariff["consigneeDistrict"] = self.tariff_consignee_location_info[tariff_info["目的地地点"]]["consigneeDistrict"]
            tariff["temperatureType"] = tariff_info["运输温控方式"]
            tariff["mileage"] = tariff_info["里程"]
            tariff["rateBase"] = tariff_info["计价基准"]
            tariff["initialRate"] = tariff_info["单价"]
            tariff_list.append(tariff)
        return tariff_list

    def __process_customer(self):
        customer_df = self.excel_file.parse(self.customer_sheetname)
        customer_df["发货波次"] = customer_df["发货波次"].astype("str")
        customer_df["发货波次"] = customer_df["发货波次"].str.replace("：",":")
        departureWave = ','.join(customer_df["发货波次"].unique())
        return departureWave

    def process_dispatch_zone(self):
        self.__process_vehicle_type()
        vehicle_list = self.__process_vehicles()
        tariff_list = self.__process_tariff() 
        departureWave = self.__process_customer()
        dispatchZone_list = list()
        for dispathZoneCode in self.dispatchZoneCode_list:
            dispatchZone = dict()
            dispatchZone["dispatchZoneCode"] = dispathZoneCode
            dispatchZone["departureWave"] = departureWave
            dispatchZone["longitude"] = random.choice(self.depots)["longitude"]
            dispatchZone["latitude"] = random.choice(self.depots)["latitude"]
            dispatchZone["vehicleType"] = self.vehicleType
            dispatchZone["vehicle"] = vehicle_list
            dispatchZone["tariff"] = tariff_list
            self.dispatchZone.append(dispatchZone)


    def __order_detail_generate(self,orderNo):
        # 生成奶粉的 SKU 信息
        NF_sku_details_info = {}
        for i in range(1, 21):
            sku_code = f"NF{str(i).zfill(4)}"
            NF_sku_details_info[sku_code] = {
                "skuDescr1": "奶粉"+str(i),
                "weight": 1000,
                "cubic": 0.0017,
                "temperatureType": "常温",
                "grossWeight": 800,
                "cube": 0.0015
            }

        # 生成酸奶的 SKU 信息
        SN_sku_details_info = {}
        for i in range(1, 21):
            sku_code = f"NF{str(i).zfill(4)}"
            if i < 10:
                SN_sku_details_info[sku_code] = {
                    "skuDescr1": "酸奶"+str(i),
                    "weight": 320,
                    "cubic": 0.0003,
                    "temperatureType": "常温",
                    "grossWeight": 300,
                    "cube": 0.0003
                }
            elif 10 < i < 15:
                SN_sku_details_info[sku_code] = {
                    "skuDescr1": "酸奶"+str(i),
                    "weight": 182,
                    "cubic": 0.00017,
                    "temperatureType": "冷藏",
                    "grossWeight": 180,
                    "cube": 0.00017
                }
            elif i > 15:
                SN_sku_details_info[sku_code] = {
                    "skuDescr1": "酸奶"+str(i),
                    "weight": 205,
                    "cubic": 0.00019,
                    "temperatureType": "常温",
                    "grossWeight": 200,
                    "cube": 0.00019
                }

        # 合并奶粉和酸奶的 SKU 信息
        all_sku_details_info = {**NF_sku_details_info, **SN_sku_details_info}
        # 订单上限
        MAX_SKU_COUNT = 500
        MIN_WEIGHT = 400000
        MAX_WEIGHT = 3000000

        current_order = {}
        current_sku_count = 0
        current_weight = 0
        available_skus = list(all_sku_details_info.keys())

        while available_skus:
            # 随机选择一个 SKU
            sku = random.choice(available_skus)
            weight = int(all_sku_details_info[sku]["weight"])
            RANDOM_SKU_COUNT = random.randint(100, MAX_SKU_COUNT)
            # 检查加入该 SKU 后是否会超过 SKU 件数上限和总重量上限
            if current_sku_count <= RANDOM_SKU_COUNT:
                if sku in current_order:
                    current_order[sku] += 1
                else:
                    current_order[sku] = 1
                current_sku_count += 1
                current_weight += weight
            else:
                break
        order_detail_list = list()
        for index, (sku, count) in enumerate(current_order.items()):
            order_detail_list.append({"taskNo":orderNo, "taskLineNo": str(index+1),
                                "sku": sku, 
                                "skuDescr1": all_sku_details_info[sku]['skuDescr1'],
                                "qty": count,
                                "weight" : round(count*all_sku_details_info[sku]['weight']/ 1_000_000,5),
                                "cubic" : round(count*all_sku_details_info[sku]['cubic'],5),
                                "temperatureType" : all_sku_details_info[sku]['temperatureType'],
                                "grossWeight" : round(count*all_sku_details_info[sku]['grossWeight']/ 1_000_000,5),
                                "cube" : round(count*all_sku_details_info[sku]['cube'],5)
                                })
            qty = sum(sku["qty"] for sku in order_detail_list)
            weight =  sum(sku["weight"]*sku["qty"] for sku in order_detail_list)
            cubic = sum(sku["cubic"]*sku["qty"] for sku in order_detail_list)
        return qty, round(weight,3), round(cubic,3), order_detail_list

    def __get_time_complement(self,time_str):
        # 将时间字符串拆分成时间区间列表
        intervals = [interval.split('-') for interval in time_str.split(',')]
        # 初始化补集区间列表
        complement_intervals = []
        # 前一个区间的结束时间，初始为 00:00
        prev_end = '00:00'

        for start, end in intervals:
            if start > prev_end:
                # 如果当前区间的开始时间大于前一个区间的结束时间，说明存在空闲区间
                complement_intervals.append(f"{prev_end}-{start}")
            # 更新前一个区间的结束时间
            prev_end = end

        # 检查最后一个区间结束后到 24:00 是否有空闲区间
        if prev_end < '24:00':
            complement_intervals.append(f"{prev_end}-24:00")

        # 将补集区间列表转换为字符串
        return ','.join(complement_intervals)
    
    def process_orders(self):
        depots_df = self.excel_file.parse(self.depots_sheetname)
        orders_df = self.excel_file.parse(self.orders_sheetname)
        customer_df = self.excel_file.parse(self.customer_sheetname)
        customer_df = customer_df.rename(columns={"客户编码":"客户编号","维度":"纬度"})
        orders_df = orders_df.rename(columns={"维度":"纬度"})
        order_c_df = pd.merge(orders_df, customer_df, on='客户编号', how='outer')

        order_c_df["订单编号"] = order_c_df["订单编号"].astype("str")
        order_c_df["创建时间"] = order_c_df.apply(lambda _: f"{datetime.now().strftime('%Y-%m-%d')}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}", axis=1)
        order_c_df["温控类型"] = order_c_df["温控类型"].astype("str")
        order_c_df['目的地省市区详细地址'] = order_c_df['目的地省市区详细地址'].astype("str")
        encoded_values = pd.factorize(order_c_df['目的地省市区详细地址'])[0]

        # 将编码值转换为指定格式
        order_c_df["地址编码"] = ['DZ{:06d}'.format(val + 1) for val in encoded_values]

        order_c_df["经度"] = order_c_df["经度"].astype("float")
        order_c_df["纬度"] = order_c_df["纬度"].astype("float")
        order_c_df["客户编号"] = order_c_df["客户编号"].astype("str")
        order_c_df["客户允许的可用车型"] = order_c_df["客户允许的可用车型"].astype("str")
        name_atr_to_code = {(vehicleType["vehicleTypeDescr1"],vehicleType["temperatureType"]): vehicleType["vehicleTypeId"] for vehicleType in self.vehicleType}

        # 定义一个函数用于处理每行数据
        def match_codes(row):
            names = row["客户允许的可用车型"].split('、')
            attrs = [row["温控类型"]]*len(names)
            codes = []
            for name, atr in zip(names, attrs):
                code = name_atr_to_code.get((name, atr))
                if code:
                    codes.append(code)
            return ','.join(codes)
        order_c_df["客户允许的可用车型编码"] = order_c_df.apply(match_codes, axis=1)
        order_c_df["客户允许卸货的时间窗口"] = order_c_df["客户允许卸货的时间窗口"].astype("str")
        order_c_df["最长送达时间(小时)"] = order_c_df["最长送达时间(小时)"].astype("float")
        order_c_df["卸货周期（星期几可以收货）"] = order_c_df["卸货周期（星期几可以收货）"].astype("str")

        orders_list = list()
        for index, orders_info in order_c_df.iterrows():
            order = dict()
            order["dispatchZoneCode"] = random.choice(self.dispatchZone)["dispatchZoneCode"]
            order["taskNo"] = orders_info["订单编号"]
            order["orderNo"] = orders_info["订单编号"]
            order["DC"] = random.choice(self.depots)["branchId"]
            order["createTime"] = orders_info["创建时间"]
            order["routeNoNext"] = ""
            order["offeringType"] = "汽运"
            order["temperatureClass"] = orders_info['温控类型']
            order["addressNo"] = orders_info['地址编码']
            order["address"] = orders_info['目的地省市区详细地址']
            for dispatchZone in self.dispatchZone: 
                if dispatchZone["dispatchZoneCode"] == order["dispatchZoneCode"]: 
                    for vehicleType in dispatchZone["vehicleType"]:
                        pass
            order["vehicleCategory"] = ','.join([vehicleType["vehicleTypeId"] 
                                                    for dispatchZone in self.dispatchZone 
                                                        if dispatchZone["dispatchZoneCode"] == order["dispatchZoneCode"] 
                                                            for vehicleType in dispatchZone["vehicleType"]])
            order["longitude"] = orders_info["经度"]
            order["latitude"] = orders_info["纬度"]
            order["consigneeId"] = orders_info["客户编号"]
            order["companyClass"] = ""
            order["availableVehicleType"] = orders_info["客户允许的可用车型编码"]
            order["vehicleCategoryCus"] = ','.join(set(order["vehicleCategory"].split(',')).intersection(set(order["availableVehicleType"].split(','))))
            order["unloadingTimeWindow"] = orders_info["客户允许卸货的时间窗口"]
            order["nonunloadingTimeWindow"] = self.__get_time_complement(order["unloadingTimeWindow"])
            order["leadTime"] = orders_info['最长送达时间(小时)']
            datedic = {'周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7}
            order["SDD"] = (','.join(str(i) for i in range(datedic[orders_info['卸货周期（星期几可以收货）'].split('-')[0]], 
                                                        datedic[orders_info['卸货周期（星期几可以收货）'].split('-')[1]] + 1)))
            order["qty"], order["weight"], order["cubic"], order["orderDetails"] = self.__order_detail_generate(order["orderNo"])
            self.orders.append(order)

def savejson(data,file_path):
    try:
        # 打开文件以写入模式
        with open(file_path, 'w', encoding='utf-8') as file:
            # 使用 json.dump() 方法将字典写入文件
            # indent=4 参数用于美化输出，使 JSON 文件更易读
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"字典已成功保存为 {file_path}")
    except Exception as e:
        print(f"保存文件时出现错误: {e}")

if __name__ == "__main__":
    excel_file = pd.ExcelFile('../input_xlsx/data_template_v1.2.xlsx')
    json_file_path = f'../input/test-{datetime.today()}.json'
    processor = ExcelDataProcessor(excel_file)
    processor.process_config()
    # print(processor.config)
    processor.process_depots()
    # print(processor.depots)
    processor.process_dispatch_zone()
    # print(processor.dispatchZone)
    processor.process_orders()
    data = dict()
    data["config"], data["depots"], data["dispatchZone"], data["orders"] = processor.config, processor.depots, processor.dispatchZone, processor.orders
    savejson(data,json_file_path)
