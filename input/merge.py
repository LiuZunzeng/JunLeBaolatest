# -*- coding:utf-8 -*-
"""
@Time:2024/11/12
@Auth:Liu Zunzeng
@File:merge.py
"""
import pandas as pd

# 指定Excel文件路径
excel_file = '智能排线测算1101(3).xlsx'  # 替换为你的Excel文件路径

# 使用pandas的ExcelFile类来读取Excel文件
xls = pd.ExcelFile(excel_file)

# 假设你要合并的工作表名为'Sheet1'和'Sheet2'
sheet1_name = '客户资料'
sheet2_name = '11月2日单据'

# 读取两个工作表
df1 = pd.read_excel(xls, sheet_name=sheet1_name)
df2 = pd.read_excel(xls, sheet_name=sheet2_name)

# 合并两个DataFrame
# 如果你想将它们垂直堆叠，使用concat函数
#df_combined = pd.concat([df1, df2], ignore_index=True)

# 或者，如果你想将它们水平合并（基于共同的列），使用merge函数
df_combined = pd.merge(df2, df1, on='客户名称', how='outer')

# 打印合并后的DataFrame
print(df_combined)

# 如果需要，可以将合并后的DataFrame保存为新的Excel文件
df_combined.to_excel('combined_excel.xlsx', index=False)