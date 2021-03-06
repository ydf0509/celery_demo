# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:40

"""
主要用用来测试深层文件夹，celery完全不按照特定目录结构写代码。
"""
import nb_log
import celery
from celery import platforms

from dddd.j.taskj import funj

platforms.C_FORCE_ROOT = True


class Config1:
    # broker_url = f'redis://'  # 使用redis
    broker_url = 'sqla+sqlite:////celerydb.sqlite'
    include = ['dddd.e.taske', ]  # 这行非常重要,第一种方式找到消费函数

    task_routes = {
        '求和': {"queue": "queue_add", },
        # 'd.e.taske.add': {"queue": "queue_add4", },
        'sub啊': {"queue": 'queue_sub'},
        '功能j': {"queue": 'queue_j'},
    }


celery_app = celery.Celery()

celery_app.config_from_object(Config1)

celery_app.autodiscover_tasks(['dddd.f',],'taskf')  #第二种方式找到消费函数

celery_app._task_from_fun(funj, '功能j')   # 非装饰器方式注册消费任务函数，第三种方式找到消费函数


if __name__ == '__main__':
    # celery_demo 项目在我的磁盘是 F:\coding2\celery_demo。

    # 第一种运行方式，直接运行此py脚本。如果在pycahrm中可以直接运行，
    # 如果控制台运行py脚本先设置PYTHONPATH=F:\coding2\celery_demo，再python celery_app_inatcance.py 运行。
    # 控制台运行py脚本，不需要设置PYTHONPATH方式，先进入到celery_demo的根目录下，再python -m aaaa.b.c.celery_app_inatcance
    # --queues=queue_add,queue_sub,queue_j
    celery_app.worker_main(
        argv=['worker', '--pool=gevent', '--concurrency=20', '-n', 'worker1@%h', '--loglevel=debug',
              '--queues=queue_j,queue_sub', '--detach', ])

    """
    第二种运行方式，使用官方介绍的流行的celery命令行运行
    
    F: & cd F:\coding2\celery_demo 
    
    celery   worker --app=aaaa.b.c.celery_app_inatcance:celery_app --pool=gevent --concurrency=5  --queues=queue_add,queue_sub
    """
