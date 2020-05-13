# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:51
import time
from aaaa.b.c.celery_app_inatcance import celery_app

@celery_app.task(name='sub啊')
def sub(a,b):
    print(f'{a} - {b} = {a - b }')
    time.sleep(4)