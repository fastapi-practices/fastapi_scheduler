# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.common.log import log
from app.core.conf import settings

_scheduler_conf: dict = {
    'jobstores': {
        'default': RedisJobStore(
            **{
                'host': settings.REDIS_HOST,
                'port': settings.REDIS_PORT,
                'password': settings.REDIS_PASSWORD,
                'db': settings.REDIS_DATABASE,
                'socket_timeout': settings.REDIS_TIMEOUT,
            }
        )
    },
    'executors': {
        'default': AsyncIOExecutor(),
    },
    'job_defaults': {
        'coalesce': settings.APS_COALESCE,
        'max_instances': settings.APS_MAX_INSTANCES,
        'misfire_grace_time': settings.APS_MISFIRE_GRACE_TIME,
    },
    'timezone': settings.DATETIME_TIMEZONE,
}


class Scheduler(AsyncIOScheduler):
    def start(self, paused: bool = False):
        """
        启动调度任务

        :param paused:
        :return:
        """
        try:
            super().start(paused)
        except Exception as e:
            log.error(f'❌ 任务 scheduler 启动失败: {e}')

    def shutdown(self, wait: bool = True):
        """
        关闭调度任务

        :param wait:
        :return:
        """
        try:
            super().shutdown(wait)
        except Exception as e:
            log.error(f'❌ 任务 scheduler 关闭失败: {e}')


# 调度器
scheduler = Scheduler(**_scheduler_conf)
