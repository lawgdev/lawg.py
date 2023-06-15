from __future__ import annotations

from lawg.base.log import BaseLog
from lawg.typings import UNDEFINED, Undefined


class Log(BaseLog):
    def edit(self, title: str | Undefined | None = ..., description: str | Undefined | None = ..., emoji: str | Undefined | None = ..., color: str | Undefined | None = ...) -> None:
        return super().edit(title, description, emoji, color)
    
    def delete(self) -> None:
        return super().delete()
    
    
