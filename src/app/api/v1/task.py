#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated

from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Query

from app.common.task import async_scheduler
from app.schemas.response import ResponseModel
from app.tasks.print_demo import print_task

router = APIRouter()


@router.get('', summary='Get jobs')
async def get_jobs() -> ResponseModel:
    tasks = []
    async with async_scheduler as scheduler:
        jobs = await scheduler.get_jobs()
        for job in jobs:
            tasks.append({'id': job.id, 'task_id': job.task_id})
    return ResponseModel(data=tasks)


@router.post('', summary='Add a job')
async def add_job() -> ResponseModel:
    async with async_scheduler as scheduler:
        job_id = await scheduler.add_job(print_task)
    return ResponseModel(data=job_id)


@router.post('/start', summary='Start a job')
async def start_job(job: Annotated[str, Query(description='Job task id')]) -> ResponseModel:
    async with async_scheduler as scheduler:
        await scheduler.add_schedule(job, IntervalTrigger(seconds=1))
    return ResponseModel()
