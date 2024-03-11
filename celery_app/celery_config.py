# from datetime import timedelta

# from celery.schedules import crontab


broker_connection_retry = False  # 確保這個設置為 False（這是默認值）
broker_connection_retry_on_startup = True  # 將這個設置為 True，以確保在啟動時重試連接到消息代理

# Timezone
timezone = "Asia/Taipei"

# import
imports = ("celery_app.tasks",)

# result
result_backend = "db+sqlite:///results.sqlite"

# # schedules
# beat_schedule = {
#     "every-2-seconds": {
#         "task": "celery_app.tasks.add",
#         "schedule": timedelta(seconds=2),
#         "args": (5, 8),
#     },
#     "specified-time": {
#         "task": "celery_app.tasks.add",
#         "schedule": crontab(hour="8", minute="50"),
#         "args": (50, 50),
#     },
# }
