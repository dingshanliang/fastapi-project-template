"""
    使用 消息队列实现，如： celery
    本文档用于定义需要异步执行的耗时任务，如：
    - 发邮件；
    - 发短信；
"""
from core.celery_app import celery_app

@celery_app.task(acks_late=True)
def example_task(word:str) -> str:
    return f"test task returns {word}"