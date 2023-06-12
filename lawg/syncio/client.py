from __future__ import annotations

from lawg.base.client import BaseClient
from lawg.base.log import BaseLog
from lawg.base.project import BaseProject
from lawg.base.room import BaseRoom
from lawg.syncio.project import Project
from lawg.syncio.rest import Rest

from lawg.schemas import ProjectCreateSchema
from lawg.typings import STR_DICT, UNDEFINED, Undefined


class Client(BaseClient):
    """
    The syncio client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.rest: Rest = Rest(self)

    # --- MANAGERS --- #

    def project(self, project_namespace: str) -> BaseProject:
        return super().project(project_namespace)

    def room(self, project_namespace: str, room_name: str) -> BaseRoom:
        return super().room(project_namespace, room_name)

    # --- PROJECTS --- #

    def create_project(self, project_name: str, project_namespace: str) -> Project:
        schema = ProjectCreateSchema()
        data = schema.load(
            {
                "name": project_name,
                "namespace": project_namespace,
            }
        )

        resp = self.rest.request(
            path="/projects",
            method="POST",
            body=data,
        )

    def fetch_project(self, project_namespace: str) -> BaseProject:
        return super().fetch_project(project_namespace)

    def edit_project(self, project_name: str, project_namespace: str) -> BaseProject:
        return super().edit_project(project_name, project_namespace)

    def delete_project(self, project_namespace: str) -> BaseProject:
        return super().delete_project(project_namespace)

    patch_project = edit_project
    get_project = fetch_project

    # --- ROOMS --- #

    def create_room(self, project_namespace: str, room_name: str, description: str | None = None) -> BaseRoom:
        return super().create_room(project_namespace, room_name, description)

    def edit_room(
        self,
        project_namespace: str,
        room_name: str,
        name: str | Undefined | None = ...,
        description: str | Undefined | None = ...,
        emoji: str | Undefined | None = ...,
    ) -> BaseRoom:
        return super().edit_room(project_namespace, room_name, name, description, emoji)

    def delete_room(self, project_namespace: str, room_name: str) -> BaseRoom:
        return super().delete_room(project_namespace, room_name)

    patch_room = edit_room

    # --- LOGS --- #

    def create_log(
        self,
        project_namespace: str,
        room_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ) -> BaseLog:
        return super().create_log(project_namespace, room_name, title, description, emoji, color)

    def fetch_log(self, project_namespace: str, room_name: str, log_id: str) -> BaseLog:
        return super().fetch_log(project_namespace, room_name, log_id)

    def fetch_logs(
        self, project_namespace: str, room_name: str, limit: int | None = None, offset: int | None = None
    ) -> list[BaseLog]:
        return super().fetch_logs(project_namespace, room_name, limit, offset)

    def edit_log(
        self,
        project_namespace: str,
        room_name: str,
        log_id: str,
        title: str | Undefined | None = ...,
        description: str | Undefined | None = ...,
        emoji: str | Undefined | None = ...,
        color: str | Undefined | None = ...,
    ) -> BaseLog:
        return super().edit_log(project_namespace, room_name, log_id, title, description, emoji, color)

    def delete_log(self, project_namespace: str, room_name: str, log_id: str) -> BaseLog:
        return super().delete_log(project_namespace, room_name, log_id)

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log

if __name__ == "__main__":
    import os

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None

    c = Client(token)

    c.create_project("test", "test")
