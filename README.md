## 1.演示完全故意命名和文件夹层级不规则的项目下，使用celery。

<pre style="color: aqua;font-size: medium">
不标准文件夹结构下，解决老是问celery怎么不执行任务了

不标准文件夹结构下，解决恼人的 celery.exceptions.NotRegistered

celery除了性能很差以外，celery做的最差劲的方面无疑就是他的门槛太高，
多少人没小心翼翼按照严格标准的项目目录结构调用celery，卡在celery不运行任务或者报错NotRegistered在第一步就劝退了。

分布式函数调度框架对比celery有19个提升，其中之一就是随意目录层级 随意文件夹 文件命名。
</pre>

```
只要学会了这个demo的文件夹，celery 70%以上的使用问题就能掌握了，

只有掌握这种不规则的文件夹结构，而不是靠不断的改文件夹名字，不断的移动py文件位置，不断地测试，完全靠瞎猜测来使用celery。

如果想不依赖特定项目结构，同时也不需要复杂配置的指定 include 或 autodiscover_tasks ，怎么玩转分布式任务调度呢，

这就需要使用分布式函数调度框架。 
https://github.com/ydf0509/distributed_framework
pip install function_scheduling_distributed_framework --upgrade
```


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

celery_app.autodiscover_tasks(['dddd.f',],'taskf')  #第二种方式找到消费函数。
"""
特别要需要说明一下这个 autodiscover_tasks 方法，表面意思是自动发现任务，那意思是不是这很流弊，暴击第一种配置include的用法呢，
这个方法仍然是需要很多个传参的，你理解的自动发现好像是神仙级别的智能的，啥参数都不需要传，自动就能发现任务。
喂，快醒醒吧，要是对于任意层级和命名的py文件，autodiscover_tasks方法啥参数都不需要传，就能自动发现，
那官方早就把 autodiscover_tasks 弄成框架内部自动替你运行了，还会需要用暴露成公有方法需要户去手动调用吗,
用脑子想想就知道官方不可能这么傻非要麻烦用户的。写代码就怕一味地望文生义，宁愿乱猜测自己瞎意淫，也不愿意跳转到源码面稍微看看入参有哪些。

autodiscover_tasks 的 两个重要入参有 packages=None,related_name='tasks'，这两个入参有默认值，
啥参数都不传就能自动发现，前提是你的消费函数写在了一个叫task.py的文件中，同时 task.py和celery的app实例是在同一个文件夹层级里面。
如果你把被 @app.task 装饰的函数写在了一个 叫 job666.py的文件中，你就发现消费运行时候，报错 celery.exceptions.NotRegistered
"""

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
    # 注意一下 --app后面接的值，这才是celery的本质。
    """

```
