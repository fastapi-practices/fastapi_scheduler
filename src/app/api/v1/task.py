#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.common.task import async_scheduler
from app.tasks.print_demo import print_task

router = APIRouter()


@router.post('/', summary='Add a job')
async def add():
    async with async_scheduler as scheduler:
        await scheduler.add_job(print_task)
    return {'code': 200, 'msg': 'Success', 'data': None}
