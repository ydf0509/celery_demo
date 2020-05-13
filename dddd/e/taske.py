# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:5
import time
from aaaa.b.c.celery_app_inatcance import celery_app


# @celery_app.task
@celery_app.task(name='求和')
def add(x,y):
    time.sleep(3)
    print(f'{x} + {y} = {x + y}')
    time.sleep(3)