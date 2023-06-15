from __future__ import annotations

from lawg.base.client import BaseClient
from lawg.syncio.project import Project
from lawg.syncio.rest import Rest

from lawg.syncio.feed import Feed
from lawg.syncio.log import Log
from lawg.typings import UNDEFINED, Undefined


class Client(BaseClient["Project", "Feed", "Log"]):
    """
    The syncio client for lawg.
    """

    def __init__(self, token: str) -> None:
        super().__init__(token)
        self.rest: Rest = Rest(self)

    # --- MANAGERS --- #

    def project(self, project_namespace: str):
        return super().project(project_namespace)

    def feed(self, project_namespace: str, feed_name: str):
        return super().feed(project_namespace, feed_name)

    # --- PROJECTS --- #

    def create_project(self, project_namespace: str, project_name: str):
        req_data = self._validate_project_create_request(
            project_namespace=project_namespace, project_name=project_name
        )

        resp = self.rest.request(
            path="/projects",
            method="POST",
            body=req_data,
        )
        project_data = self._validate_project_response(resp)
        return Project(self, namespace=project_data["namespace"])

    def fetch_project(self, project_namespace: str):
        self._validate_project_fetch_request(project_namespace=project_namespace)
        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}",
            method="GET",
        )
        project_data = self._validate_project_response(resp_data)
        return Project(self, namespace=project_data["namespace"])

    def edit_project(self, project_namespace: str, project_name: str):
        req_data = self._validate_edit_request(project_namespace=project_namespace, project_name=project_name)
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

    # --- FEEDS --- #

    def create_feed(
        self,
        project_namespace: str,
        feed_name: str,
        description: str | None = None,
        emoji: str | None = None,
    ):
        req_data = self._validate_feed_create_request(
            project_namespace=project_namespace, feed_name=feed_name, description=description, emoji=emoji
        )

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/feeds",
            method="POST",
            body=req_data,
        )

        feed_data = self._validate_feed_response(resp_data)
        return Feed(self, project_namespace=project_namespace, name=feed_data["name"])

    def edit_feed(
        self,
        project_namespace: str,
        feed_name: str,
        name: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
    ):
        req_data = self._validate_feed_edit_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            name=name,
            description=description,
            emoji=emoji,
        )
        req_data = self.rest.prepare_body(req_data)

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}",
            method="PATCH",
            body=req_data,
        )

        feed_data = self._validate_feed_response(resp_data)
        return Feed(self, project_namespace=project_namespace, name=feed_data["name"])

    def delete_feed(self, project_namespace: str, feed_name: str) -> None:
        self._validate_feed_delete_request(project_namespace=project_namespace, feed_name=feed_name)
        self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}",
            method="DELETE",
        )

    patch_feed = edit_feed

    # --- LOGS --- #

    def create_log(
        self,
        project_namespace: str,
        feed_name: str,
        title: str,
        description: str | None = None,
        emoji: str | None = None,
        color: str | None = None,
    ):
        req_data = self._validate_log_create_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}/logs",
            method="POST",
            body=req_data,
        )

        log_data = self._validate_log_response(resp_data)
        return Log(self, project_namespace=project_namespace, feed_name=feed_name, id=log_data["id"])

    def fetch_log(self, project_namespace: str, feed_name: str, log_id: str):
        self._validate_log_fetch_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            log_id=log_id,
        )

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}/logs/{log_id}",
            method="GET",
        )

        log_data = self._validate_log_response(resp_data)
        return Log(self, project_namespace=project_namespace, feed_name=feed_name, id=log_data["id"])

    def fetch_logs(
        self,
        project_namespace: str,
        feed_name: str,
        limit: int | None = None,
        offset: int | None = None,
    ):
        req_data = self._validate_log_fetches_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            limit=limit,
            offset=offset,
        )

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}/logs",
            method="GET",
            body=req_data,
        )

        # TODO: finish

    def edit_log(
        self,
        project_namespace: str,
        feed_name: str,
        log_id: str,
        title: str | Undefined | None = UNDEFINED,
        description: str | Undefined | None = UNDEFINED,
        emoji: str | Undefined | None = UNDEFINED,
        color: str | Undefined | None = UNDEFINED,
    ):
        req_data = self._validate_log_edit_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            log_id=log_id,
            title=title,
            description=description,
            emoji=emoji,
            color=color,
        )

        resp_data = self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}/logs/{log_id}",
            method="PATCH",
            body=req_data,
        )

        log_data = self._validate_log_response(resp_data)
        return Log(self, project_namespace=project_namespace, feed_name=feed_name, id=log_data["id"])

    def delete_log(self, project_namespace: str, feed_name: str, log_id: str):
        self._validate_log_delete_request(
            project_namespace=project_namespace,
            feed_name=feed_name,
            log_id=log_id,
        )

        self.rest.request(
            path=f"/projects/{project_namespace}/{feed_name}/logs/{log_id}",
            method="DELETE",
        )

    get_log = fetch_log
    get_logs = fetch_logs
    patch_log = edit_log


if __name__ == "__main__":
    import os

    token = os.getenv("LAWG_DEV_API_TOKEN")
    assert token is not None

    c = Client(token)

    project_namespace = "test"
    project_name = "test"
    feed_name = "123123"

    # proj = c.create_project(project_namespace, project_name)
    # feed = c.create_feed(project_namespace, feed_name)
    # print(c.edit_feed(project_namespace, feed.name, name="new_name", description="new_desc", emoji="💀"))

    # c.delete_project(project_namespace)
