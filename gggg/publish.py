# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:55




from aaaa.b.c.celery_app_inatcance import celery_app
celery_app.send_task('求和',args=(100,200)) # 第一种发布方式

from dddd.e.taske import add
[add.delay(i, 2 * i) for i in range(10)]  # 第二种发布方式

from dddd.f.taskf import sub
[sub.apply_async(args=(i, 2 * i)) for i in range(10)] # 第三种发布方式，这种入参更丰富可以添加任务控制参数。delay只能是函数本身的参数。

celery_app.send_task('功能j', args=('哈哈',))


from dddd.j.k.taskk import test_auto_share_celeryapp
for i in range(10):
    test_auto_share_celeryapp.delay(f'测试自动使用解释器中存在的 celery 实例 {i}')



"""
{
  "body": "W1sxLCAyXSwge30sIHsiY2FsbGJhY2tzIjogbnVsbCwgImVycmJhY2tzIjogbnVsbCwgImNoYWluIjogbnVsbCwgImNob3JkIjogbnVsbH1d",
   "content-encoding":  "utf-8",
   "content-type":  "application/json",
   "headers":  {
    "lang":  "py",
     "task":  "\u6c42\u548c",
     "id":  "8fb79089-fdb5-4b9d-b656-cf92181a7318",
     "shadow":  null,
     "eta":  null,
     "expires":  null,
     "group":  null,
     "retries":  0,
     "timelimit":  [
      null,
       null
    ],
     "root_id":  "8fb79089-fdb5-4b9d-b656-cf92181a7318",
     "parent_id":  null,
     "argsrepr":  "(1, 2)",
     "kwargsrepr":  "{}",
     "origin":  "gen46668@ydfe52678v3"
  },
   "properties":  {
    "correlation_id":  "8fb79089-fdb5-4b9d-b656-cf92181a7318",
     "reply_to":  "d42d6440-68c4-3ab7-bf3c-64aed4fe845f",
     "delivery_mode":  2,
     "delivery_info":  {
      "exchange":  "",
       "routing_key":  "queue_add"
    },
     "priority":  0,
     "body_encoding":  "base64",
     "delivery_tag":  "c4d9358d-c028-4c94-ad3b-fb7c456a08a9"
  }
}
"""
