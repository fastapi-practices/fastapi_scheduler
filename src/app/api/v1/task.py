#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fastapi import APIRouter

from app.common.task import scheduler
from app.schemas.response import ResponseModel
from app.schemas.task import CronJob, IntervalJob, DateJob, GetTask
from app.utils.get_functions import get_task_functions

router = APIRouter()


@router.get('', summary='获取任务列表')
async def get_all_tasks() -> ResponseModel:
    tasks = []
    for job in scheduler.get_jobs():
        tasks.append(
            GetTask(
                **{
                    'id': job.id,
                    'func_name': job.func_ref,
                    'trigger': str(job.trigger),
                    'executor': job.executor,
                    'name': job.name,
                    'misfire_grace_time': job.misfire_grace_time,
                    'coalesce': job.coalesce,
                    'max_instances': job.max_instances,
                    'next_run_time': job.next_run_time,
                }
            ).model_dump()
        )
    return ResponseModel(data=tasks)


@router.get('/functions', summary='获取所有可创建任务')
async def get_functions() -> ResponseModel:
    task_funcs = get_task_functions()
    return ResponseModel(data=task_funcs)


@router.get('/{job}', summary='获取任务详情')
async def get_task(job: str) -> ResponseModel:
    task = scheduler.get_job(job_id=job)
    if not task:
        return ResponseModel(msg=f'任务 {job} 不存在')
    task_info = GetTask(
        **{
            'id': task.id,
            'func_name': task.func_ref,
            'trigger': str(task.trigger),
            'executor': task.executor,
            'name': task.name,
            'misfire_grace_time': task.misfire_grace_time,
            'coalesce': task.coalesce,
            'max_instances': task.max_instances,
            'next_run_time': task.next_run_time,
        }
    )
    return ResponseModel(data=task_info)


@router.post('/cron/add', summary='添加 corn 任务')
async def add_cron_task(job: CronJob) -> ResponseModel:
    task = scheduler.add_job(**job.model_dump())
    return ResponseModel(data=task.id)


@router.post('/interval/add', summary='添加 interval 任务')
async def add_interval_task(job: IntervalJob) -> ResponseModel:
    task = scheduler.add_job(**job.model_dump())
    return ResponseModel(data=task.id)


@router.post('/date/add', summary='添加 date 任务')
async def add_date_task(job: DateJob) -> ResponseModel:
    task = scheduler.add_job(**job.model_dump())
    return ResponseModel(data=task.id)


@router.post('/{job}/run', summary='执行任务')
async def run_task(job: str) -> ResponseModel:
    task = scheduler.get_job(job_id=job)
    if not task:
        return ResponseModel(msg=f'任务 {job} 不存在')
    task = scheduler.modify_job(job_id=job, next_run_time=datetime.now())
    return ResponseModel(data=task.id)


@router.post('/{job}/pause', summary='暂停任务')
async def pause_task(job: str) -> ResponseModel:
    task = scheduler.get_job(job_id=job)
    if not task:
        return ResponseModel(msg=f'任务 {job} 不存在')
    scheduler.pause_job(job_id=job)
    return ResponseModel(data=task.id)


@router.post('/{job}/resume', summary='恢复任务')
async def resume_task(job: str) -> ResponseModel:
    task = scheduler.get_job(job_id=job)
    if not task:
        return ResponseModel(msg=f'任务 {job} 不存在')
    scheduler.resume_job(job_id=job)
    return ResponseModel(data=job)


@router.post('/{job}/stop', summary='删除任务')
async def delete_task(job: str) -> ResponseModel:
    task = scheduler.get_job(job_id=job)
    if not task:
        return ResponseModel(msg=f'任务 {job} 不存在')
    scheduler.remove_job(job_id=job)
    return ResponseModel(data=job)
