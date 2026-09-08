# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Phat Tran Vu Hoa - RentCalc
"""Cấu hình Jinja2Templates chia sẻ cho các routers."""

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")