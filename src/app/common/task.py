# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from apscheduler import AsyncScheduler
from apscheduler.eventbrokers.redis import RedisEventBroker

from app.common.log import log
from app.common.redis import redis_client

# 调度器
async_scheduler = AsyncScheduler(
    **{
        'event_broker': RedisEventBroker(client=redis_client),
    }
)


async def async_scheduler_start():
    try:
        async with async_scheduler as scheduler:
            await scheduler.start_in_background()
    except Exception as e:
        log.error(f'❌ 任务 scheduler 启动失败: {e}')
        sys.exit()


async def async_scheduler_shutdown(wait: bool = False):
    try:
        async with async_scheduler as scheduler:
            if not wait:
                await scheduler.stop()
            else:
                await scheduler.wait_until_stopped()
    except Exception as e:
        log.error(f'❌ 任务 scheduler 关闭失败: {e}')
