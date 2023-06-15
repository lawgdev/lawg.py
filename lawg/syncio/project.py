from __future__ import annotations

import typing as t

from lawg.base.project import BaseProject
from lawg.typings import UNDEFINED

if t.TYPE_CHECKING:
    from lawg.syncio.client import Client
    from lawg.syncio.room import Room
    from lawg.syncio.log import Log
    from lawg.typings import Undefined


class Project(BaseProject["Client", "Room", "Log"]):
    # --- MANAGERS --- #

    def room(self, room_name: str):
        return self.client.room(project_namespace=self.namespace, room_name=room_name)

    # --- ROOMS --- #

    def create_room(self, room_name: str, description: str | None = None):
        return self.client.create_room(project_namespace=self.namespace, room_name=room_name, description=description)

    def edit_room(
        self,
        room_name: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ) -> Room:
        return self.client.edit_room(
            project_namespace=self.namespace, room_name=room_name, name=name, description=description, emoji=emoji
        )

    def delete_room(self, room_name: str) -> Room:
        return self.client.delete_room(project_namespace=self.namespace, room_name=room_name)

    patch_room = edit_room

    # --- LOGS --- #

    def create_log(
        self,
        room_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> Log:
        return self.client.create_log(
            project_namespace=self.namespace,
            room_name=room_name,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def fetch_log(self, room_name: str, log_id: str) -> Log:
        return self.client.fetch_log(project_namespace=self.namespace, room_name=room_name, log_id=log_id)

    def fetch_logs(self, room_name: str, limit: int | None = None, offset: int | None = None) -> list[Log]:
        return self.client.fetch_logs(
            project_namespace=self.namespace, room_name=room_name, limit=limit, offset=offset
        )

    def edit_log(
        self,
        room_name: str,
        log_id: str,
        title: str | Undefined | None = ...,
        description: str | Undefined | None = ...,
        emoji: str | Undefined | None = ...,
        color: str | Undefined | None = ...,
    ) -> Log:
        return self.client.edit_log(
            project_namespace=self.namespace,
            room_name=room_name,
            log_id=log_id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

    def delete_log(self, room_name: str, log_id: str) -> Log:
        return self.client.delete_log(
            project_namespace=self.namespace,
            room_name=room_name,
            log_id=log_id,
        )

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log
