#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.v1.task import router as task_router

from app.core.conf import settings

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(task_router, prefix='/tasks', tags=['定时任务'])
