## 1.演示完全故意命名和文件夹层级不规则的项目下，使用celery。

只要学会了这个demo，celery 90%的使用问题就能掌握了。

## 2.演示两种运行celery消费的方式

 1).使用python xxx.py的方式启动消费
 
 2).使用celery 命令的方式启动消费

## 3.1演示三种发布任务方式

delay

apply_async

send_task

## 3.2 演示三种函数注册成celery消费任务的方式

app.task装饰器 + include

app.task装饰器 + autodiscover_tasks

app._task_from_fun 非装饰器方式， 用法类似于flask框架的@app.route 和app.add_url_route的关系。

## 4 .项目目录结构是：
```

文件夹 PATH 列表
卷序列号为 927B-F991
celery_demo:.
        │  .gitignore
        │  nb_log_config.py
        │  README.md
        │  
        │          
        ├─aaaa
        │  └─b
        │      └─c
        │          │  celery_app_inatcance.py
        │                  
        ├─dddd
        │  ├─e
        │  │    │  taske.py
        │  │          
        │  └─f
        │  |    │  taskf.py
        |  │            
        │  └─j
        │       │  taskj.py
        │              
        ├─gggg
        │     | publish.py
        │      

        
```

## 主代码
```python
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


```
