# 使用官方 Python 3 基础镜像
FROM python:3.10.17-slim

# 设置工作目录
WORKDIR /app

# 升级 pip 工具
RUN pip install --upgrade pip setuptools wheel -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制 requirements 文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 5001

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
