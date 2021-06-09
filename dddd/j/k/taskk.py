from celery import shared_task

"""
用shared_task的 好处是无需提前导入一个celery_app,然后celery_app.task，能够非常好的解决，如果不使用include 动态延迟导入的方式时候，
celery_app实例所在python文件导入任务函数，任务函数所在python文件导入celery_app这种互相导入的矛盾。

shared_task装饰器自动使用当前python解释器的最后的Celery类型的对象，所以最好是确保启动python后，当前解释器只有一个Celery类型的对象。
这里说的是不能在同一次启动有两个celery对象， app1 = Celery(broker="redis://")  下一行写app2=Celery(broker="amqp://") ，
那么shared task会使用rabbitmq，因为自动指向了最后一次的Celery类型的实例。为了避免意想不到的混乱，不要一次启动时候实例化了多个Celery对象，
一般实例化多个celery类型实例的场景也很少。

shared_task来开发第三方包很好，因为那个包里面的任务能自动的使用用户自己的celery实例。

"""

@shared_task(name='测试自动关联使用已存在celery app 实例')
def test_auto_share_celeryapp(x):
    print(x)