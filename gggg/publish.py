# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2020/1/16 0016 9:55
from dddd.e.taske import add
from dddd.f.taskf import sub

from aaaa.b.c.celery_app_inatcance import celery_app
celery_app.send_task('求和',args=(100,200))


# [add.delay(i, 2 * i) for i in range(10)]
# [sub.apply_async(args=(i, 2 * i)) for i in range(10)]
celery_app.send_task('功能j', args=('哈哈',))
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
