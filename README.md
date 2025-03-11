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


# Git代码管理

注：代码运行系统为Linux，每次拉取和上传代码都先上传到develop分支，然后申请一个`pull requsts`，管理员审核后再把代码合并到main分支上

## 克隆仓库代码

```bash
git clone git@github.com:LiuZunzeng/JunLeBaolatest.git
```


## 每次进行本地代码开发前需要做：
1. 本地切换分支

    ```bash
    git switch develop
    ```

2. 拉取代码

    ```bash
    git pull origin develop
    ```

## 开发后上传代码

```
git add .
git commit -m "提交信息"
git push -u origin develop
```