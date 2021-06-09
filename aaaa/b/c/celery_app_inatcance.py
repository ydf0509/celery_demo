# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:40

"""
主要用用来测试深层文件夹，celery完全不按照特定目录结构写代码。
"""
import nb_log
import celery
from celery import platforms

platforms.C_FORCE_ROOT = True

celery_app = celery.Celery()

class Config1:
    # broker_url = f'redis://'  # 使用redis
    broker_url = 'sqla+sqlite:////celerydb.sqlite'
    include = ['dddd.e.taske', ]  # 第一种方式找到消费函数,这行非常重要,

    task_routes = {
        '求和': {"queue": "queue_add", },
        # 'd.e.taske.add': {"queue": "queue_add4", },
        'sub啊': {"queue": 'queue_sub'},
        '功能j': {"queue": 'queue_j'},
        '测试自动关联使用已存在celery app 实例':{'queue':'queue_test_auto_share_celeryapp'}
    }



celery_app.config_from_object(Config1)

celery_app.autodiscover_tasks(['dddd.f',],'taskf')  #第二种方式找到消费函数


from dddd.j.taskj import funj
celery_app._task_from_fun(funj, '功能j')   # 第三种方式找到消费函数,非装饰器方式注册原本没被@celery_app.task装饰的消费任务函数，


# 第四种方式找到消费函数，如果include或者autodiscover_tasks都没指定导入这个脚本的任务函数，
# 同时也不使用celery_app._task_from_fun来注册一个没有被装饰器装饰的函数
# 那么使用 @celery.shared_task来装饰 test_auto_share_celeryapp是非常好的推荐的做法，
# 因为脚本中无需导入此文件的celery_app实例，方便此文件导入test_auto_share_celeryapp函数，不会发生互相导入。
# include来配置字符串从而导入模块，真的太差了，pycahrm不能自省，
# pycahrm不能自动检查模块名字有没有写错，特别是把任务函数放在10层级文件夹下的python文件下面，include 很容易打错字。
from dddd.j.k.taskk import test_auto_share_celeryapp  # 如果没有写include 模块路径字符串，就导入函数就行，自动使用当前celery_app实例，


if __name__ == '__main__':
    # celery_demo 项目在我的磁盘是 F:\coding2\celery_demo。

    # 第一种运行方式，直接运行此py脚本。如果在pycahrm中可以直接运行，
    # 如果控制台运行py脚本先设置PYTHONPATH=F:\coding2\celery_demo，再python celery_app_inatcance.py 运行。
    # 控制台运行py脚本，不需要设置PYTHONPATH方式，先进入到celery_demo的根目录下，再python -m aaaa.b.c.celery_app_inatcance
    # --queues=queue_add,queue_sub,queue_j
    celery_app.worker_main(
        argv=['worker', '--pool=gevent', '--concurrency=20', '-n', 'worker1@%h', '--loglevel=debug',
              '--queues=queue_j,queue_sub,queue_test_auto_share_celeryapp', '--detach', ])

    """
    第二种运行方式，使用官方介绍的流行的celery命令行运行
    
    F: & cd F:\coding2\celery_demo 
    
    celery   worker --app=aaaa.b.c.celery_app_inatcance:celery_app --pool=gevent --concurrency=5  --queues=queue_add,queue_sub
    """
