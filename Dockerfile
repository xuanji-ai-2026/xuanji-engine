# 构建阶段
FROM python:3.12-slim

# 安装git和系统依赖
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv pydantic httpx aiofiles aiohttp sqlalchemy

# 工作目录
WORKDIR /app

# 复制源代码
COPY src/ ./src/

# 暴露端口
EXPOSE 8888

# 启动命令
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8888"]
