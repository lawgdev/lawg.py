from __future__ import annotations

from lawg.base.client import BaseClient
from lawg.base.log import BaseLog
from lawg.base.room import BaseRoom
from lawg.syncio.project import Project
from lawg.syncio.rest import Rest

from lawg.schemas import APISuccessSchema, ProjectCreateSchema, ProjectGetSchema, ProjectSchema
from lawg.syncio.room import Room
from lawg.syncio.log import Log
from lawg.typings import STR_DICT, UNDEFINED, Undefined


class Client(BaseClient[Project, Room, Log]):
    """
    The syncio client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.rest: Rest = Rest(self)

    # --- MANAGERS --- #

    def project(self, project_namespace: str):
        return super().project(project_namespace)

    def room(self, project_namespace: str, room_name: str):
        return super().room(project_namespace, room_name)

    # --- PROJECTS --- #

    def create_project(self, project_name: str, project_namespace: str):
        req_data = self._validate_create_request(project_name=project_name, project_namespace=project_namespace)
        resp = self.rest.request(
            path="/projects",
            method="POST",
            body=req_data,
        )
        project_data = self._validate_project_response(resp)
        return Project(self, namespace=project_data["namespace"])

    def fetch_project(self, project_namespace: str):
        self._validate_fetch_request(project_namespace=project_namespace)
        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}",
            method="GET",
        )
        project_data = self._validate_project_response(resp_data)
        return Project(self, namespace=project_data["namespace"])

    def edit_project(self, project_name: str, project_namespace: str):
        req_data = self._validate_edit_request(project_name=project_name, project_namespace=project_namespace)
        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}",
            method="PATCH",
            body=req_data,
        )
        project_data = self._validate_project_response(resp_data)
        return Project(self, namespace=project_data["namespace"])

    def delete_project(self, project_namespace: str) -> None:
        self._validate_delete_request(project_namespace=project_namespace)
        self.rest.request(
            path=f"/projects/{project_namespace}",
            method="DELETE",
        )

    patch_project = edit_project
    get_project = fetch_project

    # --- ROOMS --- #

    def create_room(self, project_namespace: str, room_name: str, description: str | None = None):
        return super().create_room(project_namespace, room_name, description)

    def edit_room(
        self,
        project_namespace: str,
        room_name: str,
        name: str | Undefined | None = ...,
        description: str | Undefined | None = ...,
        emoji: str | Undefined | None = ...,
    ):
        return super().edit_room(project_namespace, room_name, name, description, emoji)

    def delete_room(self, project_namespace: str, room_name: str):
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
    ):
        return super().create_log(project_namespace, room_name, title, description, emoji, color)

    def fetch_log(self, project_namespace: str, room_name: str, log_id: str):
        return super().fetch_log(project_namespace, room_name, log_id)

    def fetch_logs(self, project_namespace: str, room_name: str, limit: int | None = None, offset: int | None = None):
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
    ):
        return super().edit_log(project_namespace, room_name, log_id, title, description, emoji, color)

    def delete_log(self, project_namespace: str, room_name: str, log_id: str):
        return super().delete_log(project_namespace, room_name, log_id)

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log


if __name__ == "__main__":
    import os

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None

    c = Client(token)
    proj = c.create_project("test", "test")

    print(proj)
