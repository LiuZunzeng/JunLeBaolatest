# 第一阶段：构建阶段
FROM python:3.10-slim as build

# 安装必要的工具
RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 安装 pyvrp
COPY pyvrp-0.9.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .
RUN pip install --no-cache-dir pyvrp-0.9.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# 第二阶段：运行阶段
FROM python:3.10-slim

# 暴露端口
EXPOSE 5000

# 复制构建阶段的依赖和应用程序
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /work

# 配置环境变量和工作目录
ENV PYTHONPATH=/work
WORKDIR /work

# 启动 Flask 应用
CMD ["python3", "src/vrp_flask.py"]
