# 使用说明
## 初始化以Django的服务。
1. 创建工程
2. 创建数据库
3. 配置启动参数
4. 试运行





## 使用创建 `dailynews` 作为示例说明:
###  基本内容
1. 创建app: Startapp
2. 注册该 app
3. 创建定时任务脚本。
4. 配置该定时任务的执行时间。
5. 试运行。


#### 1. 创建该app。
Use django command to create a app.

```
monitors# django-admin startapp dailynews
```

#### 2. 注册该 app

在monitors/settings.py的INSTALLED_APPS中增加dailynews.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dailynews',
]
```
#### 3. 创建定时任务脚本

在dailynews创建定时任务函数：

```
from __future__ import absolute_import
from celery import shared_task

@shared_task
def CheckDailyNews():
    print("It's a trail")
    return True
```
#### 4. 配置该定时任务的执行时间
在monitors/monitors/celery.py 设置定时
```
# schedules tasks
app.conf.update(CELERYBEAT_SCHEDULE={
    'task': {
        'task': 'dailynews.tasks.CheckDailyNews',
        'schedule': timedelta(seconds=20),
        'args': ()
    }
})
```
#### 5. 试运行
参考Monitors/scripts下脚本， 依次分别启动Django(后台服务), celery-worker（任务消费者）, celery-beat(任务生产者), flower（任务收集展示）

```
monitors# python manage.py runserver 0.0.0.0:9000
monitors# celery -A monitors worker -l debug
monitors# celery -A monitors beat -l debug
monitors# celery -A monitors flower --port=5555 -l debug
```
然后就可以在flower查看任务的执行情况了



