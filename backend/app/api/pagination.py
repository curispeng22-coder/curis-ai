"""分页信封（A5 契约）。

列表类接口统一返回 ``Page[T]``，包在 ``ApiResponse.data`` 内。
"""

from __future__ import annotations

from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T] = []
    total: int = 0
    page: int = 1
    page_size: int = 0
    pages: int = 0


def paginate(
    items: list[T],
    total: int,
    page: int,
    page_size: int,
) -> Page[T]:
    """构造分页信封；``pages`` 自动向上取整。"""
    pages = ceil(total / page_size) if page_size > 0 else 0
    return Page(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )
