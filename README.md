## 演示不规范的celery项目目录结构的celery的使用：

<pre style="color: greenyellow;background-color: #0c1119; font-size: x-large;">
文章结尾第五章放出大杀器 funboost 自动化操作celery demo例子
</pre>



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

## 0. 如果学会了这个不规则celery项目目录的demo，则掌握celery 60%

如果学会了这个demo，则celery已近掌握了60%至少，大部分人是要celery会遇到任务不执行不动，或这行报错。

所以网上的celery博客教程虽然很多，但是并不能学会使用，因为要运行起来需要以下6个方面都掌握好，博客文字很难表达清楚或者没有写全面以下6个方面。
celery消费任务不执行或者报错NotRegistered，与很多方面有关系，如果要别人排错，至少要发以下6方面的截图


```
1) 整个项目目录结构,celery的目录结构和任务函数位置，有很大影响
   
2) @task入参 ,用户有没有主动设置装饰器的入参 name,设置了和没设置有很大不同，建议主动设置这个名字对函数名字和所处位置依赖减小
   
3) celery的配置，task_queues 和task_routes 

4) celery的配置 include 或者 imports  或者 app.autodiscover_tasks的入参

5) cmd命令行启动参数 --queues=  的值
   
6) 用户在启动cmd命令行时候，用户所在的文件夹。
   (如果不精通这个demo的，使用cmd命令行启动时候，用户必须cd切换到当前python项目的根目录，
   如果精通主动自己设置PYTHONPATH和精通此demo，可以在任何目录下启动celery命令行或者不使用celery命令行而是调用app.worker_main 用python脚本启动。
```

## 1.演示完全故意命名和文件夹层级不规则的项目下，使用celery。

<pre style="color: #006400;font-size: medium">
不标准文件夹结构下，解决老是问celery怎么不执行任务了

不标准文件夹结构下，解决恼人的 celery.exceptions.NotRegistered

celery除了性能很差以外，celery做的最差劲的方面无疑就是他的门槛太高，
多少人没小心翼翼按照严格标准的项目目录结构调用celery，卡在celery不运行任务或者报错NotRegistered在第一步就劝退了。

分布式函数调度框架对比celery有19个提升，其中之一就是随意目录层级 随意文件夹 文件命名。
</pre>

```
只要学会了这个demo的文件夹，celery 70%以上的使用问题就能掌握了，

只有掌握这种不规则的文件夹结构，而不是靠不断的改文件夹名字，不断的移动py文件位置，不断地测试，完全靠瞎猜测来使用celery。

```

<pre style="color: greenyellow;background-color: #0c1119; font-size: medium;">
如果想不依赖特定项目结构，同时也不需要复杂配置的指定 include 或 autodiscover_tasks ，怎么玩转分布式任务调度呢，

这就需要使用分布式函数调度框架。 
https://github.com/ydf0509/funboost
pip install funboost 
</pre>

## 2.演示两种运行celery消费的方式

1).使用python xxx.py的方式启动消费

2).使用celery 命令的方式启动消费

## 3.1演示三种发布任务方式

delay

apply_async

send_task

## 3.2 演示4种函数注册成celery消费任务的方式

app.task装饰器 + include

app.task装饰器 + autodiscover_tasks

app._task_from_fun 非装饰器方式， 用法类似于flask框架的@app.route 和app.add_url_route的关系。

@shared_task装饰器，这个不需要@app.task的app，所以可以在app实例化所在模块直接导入任务函数，不会出现互相导入的纠结。

## 4 主代码

```
包含了三种方式找到消费函数,
```

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
        '测试自动关联使用已存在celery app 实例': {'queue': 'queue_test_auto_share_celeryapp'}
    }


celery_app = celery.Celery()

celery_app.config_from_object(Config1)

celery_app.autodiscover_tasks(['dddd.f', ], 'taskf')  # 第二种方式找到消费函数。
"""
特别要需要说明一下这个 autodiscover_tasks 方法，表面意思是自动发现任务，那意思是不是这很流弊，暴击第一种配置include的用法呢，
这个方法仍然是需要很多个传参的，你理解的自动发现好像是神仙级别的智能的，啥参数都不需要传，自动就能发现任务。
喂，快醒醒吧，要是对于任意层级和命名的py文件，autodiscover_tasks方法啥参数都不需要传，就能自动发现，
那官方早就把 autodiscover_tasks 弄成框架内部自动替你运行了，还会需要用暴露成公有方法需要户去手动调用吗,
用脑子想想就知道官方不可能这么傻非要麻烦用户的。写代码就怕一味地望文生义，宁愿乱猜测自己瞎意淫，也不愿意跳转到源码面稍微看看入参有哪些。

autodiscover_tasks 的 两个重要入参有 packages=None,related_name='tasks'，这两个入参有默认值，
啥参数都不传就能自动发现，前提是你的消费函数写在了一个叫tasks.py的文件中，同时 tasks.py和celery的app实例是在同一个文件夹层级里面。
如果你把被 @app.task 装饰的函数写在了一个 叫 job666.py的文件中，你就发现消费运行时候，报错 celery.exceptions.NotRegistered
"""

celery_app._task_from_fun(funj, '功能j')  # 非装饰器方式注册消费任务函数，第三种方式找到消费函数

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


## 5 funboost 自动化操作celery

funboost自动化操作celery,用户无需处理celery配置,funboost自动搞定这些

[https://github.com/ydf0509/celery_demo](https://github.com/ydf0509/celery_demo)