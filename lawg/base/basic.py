from __future__ import annotations

from abc import ABC, abstractmethod
import typing as t

if t.TYPE_CHECKING:
    from lawg.asyncio.rest import AsyncRest
    from lawg.syncio.rest import Rest


class BaseBasicClient(ABC):
    def __init__(self, *, token: str, project: str | None = None) -> None:
        self._rest: Rest | AsyncRest
        self.token = token
        self.project = project
        print(f"{token=} {project=}")

    @abstractmethod
    def publish(
        self,
        *,
        project: str | None = None,
        channel: str,
        event: str,
        description: str | None = None,
        icon: str | None = None,
        tags: dict[str, str] | None = None,
        notify: bool = False,
    ) -> None:
        """
        Publish an event to a channel.
        Args:
            channel (str): name of channel (defined in project).
            event (str): name of event (custom).
            description (str | None, optional): description of event. Defaults to None.
            icon (str | None, optional): icon of event. Defaults to None.
            tags (dict[str, str] | None, optional): tag specifics of req. Defaults to None.
            notify (bool, optional): _description_. notify via mobile. Defaults to False.
        """
        # payload = {
        #     "project": project or self.project,
        #     "channel": channel,
        #     "event": event,
        #     "description": description,
        #     "icon": icon,
        #     "tags": tags,
        #     "notify": notify,
        # }
        # data = self._rest.request(method="POST", payload=payload)

    @abstractmethod
    def edit(
        self,
        *,
        event: str | None = None,
        description: str | None = None,
        icon: str | None = None,
        tags: dict[str, str] | None = None,
    ) -> None:
        """
        Edit an event.
        Args:
            event (str | None, optional): name of event. Defaults to None.
            description (str | None, optional): description of event. Defaults to None.
            icon (str | None, optional): icon of event. Defaults to None.
            tags (dict[str, str] | None, optional): tag specifics of req. Defaults to None.
        """
        # payload = {
        #     "event": event,
        #     "description": description,
        #     "icon": icon,
        #     "tags": tags,
        # }
        # data = self._rest.request(method="PATCH", payload=payload)

    @abstractmethod
    def delete(self, *, project: str | None, channel: str, id: str) -> None:
        """
        Delete an event.
        Args:
            id (str): id of event.
        """
        # payload = {"project": project or self.project, "channel": channel, "id": id}
        # data = self._rest.request(method="DELETE", payload=payload)

    @abstractmethod
    def get(self, *, project: str | None, channel: str, id: str) -> None:
        """
        Get an event.
        Args:
            id (str): id of event.
        """
        # payload = {"project": project or self.project, "channel": channel, "id": id}
        # data = self._rest.request(method="GET", payload=payload)
