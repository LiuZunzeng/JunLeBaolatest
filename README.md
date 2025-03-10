# JunLeBao-云服务
### 项目简介：
&emsp;&emsp;本项目旨在解决车辆路径规划问题（Vehicle Routing Problem, VRP），通过给定的订单、车辆和仓库信息，计算出最优的配送路线。
### 运行flask应用
&emsp;&emsp;`python3 vrp_flask.py`
### 文件结构
JunLeBao-云服务/\
├── input/                   \
├── output/                  \
├── README.md                \
├── requirements.txt         \
└── src/                     \
&emsp;&emsp;├── vrp_flask.py       \
&emsp;&emsp;├── PyVRP.py             \
&emsp;&emsp;├── data.py               \
&emsp;&emsp;├── solution.py          \
&emsp;&emsp;└── main.py    

### 代码说明
&emsp;&emsp;Data 类：负责读取和处理输入数据，计算距离。\
&emsp;&emsp;Solution 类：负责计算 VRP 问题的解决方案，并可视化结果。\
&emsp;&emsp;PyVRP 类：封装了 PyVRP 求解器的接口，用于求解 VRP 问题。\
&emsp;&emsp;Solver 类：项目的主要流程。\
&emsp;&emsp;vrp_flask.py：Flask 应用的入口点，提供了一个 web 服务接口来接收请求并返回解决方案。
