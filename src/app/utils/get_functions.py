#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib.util
import inspect
from typing import List

from app.core.conf import settings


def get_task_functions() -> List[str]:
    """从文件中获取所有函数"""
    spec = importlib.util.spec_from_file_location('module_name', settings.TASK_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            functions.append(obj)

    function_names = []
    task_module = settings.TASK_FILE.split('.')[0]
    for func in functions:
        function_names.append(f'app.{task_module}:{func.__name__}')

    return function_names
