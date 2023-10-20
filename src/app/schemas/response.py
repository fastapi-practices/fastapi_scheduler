#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core.conf import settings


class ResponseModel(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = 200
    msg: str = 'Success'
    data: Any | None = None
