

## 实现消息队列
- 启动redis
  - 启动 docker
  - 运行 `docker run -d -p 6379:6379 redis`
  - 安装 redis包 `pip install -U "celery[redis]"`
- 启动 celery
  - `celery -A tasks worker --loglevel=INFO`
- 在接口中访问任务接口

