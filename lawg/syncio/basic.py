from lawg.base.basic import BaseBasicClient
from lawg.syncio.rest import Rest

__all__ = ("BasicClient",)


class BasicClient(BaseBasicClient):
    def __init__(self, *, token: str, project: str | None = None) -> None:
        super().__init__(token=token, project=project)
        self._rest = Rest(client=self)

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
        project = project or self.project
        if not project:
            raise ValueError("project is required")
        self._rest.request(
            method="POST",
            project=project,
            channel=channel,
            event=event,
            description=description,
            icon=icon,
            tags=tags,
            notify=notify,
        )

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

        data = self._rest.request(method="PATCH", event=event, description=description, icon=icon, tags=tags)
        print(f"{data=}")

    def delete(self, *, project: str | None, channel: str, id: str) -> None:
        # sourcery skip: class-extract-method
        """
        Delete an event.
        Args:
            id (str): id of event.
        """
        project = project or self.project
        if not project:
            raise ValueError("project is required")
        self._rest.request(method="DELETE", project=project, channel=channel, id=id)

    def get(self, *, project: str | None, channel: str, id: str) -> None:
        """
        Get an event.
        Args:
            id (str): id of event.
        """
        project = project or self.project
        if not project:
            raise ValueError("project is required")
        self._rest.request(method="GET", project=project, channel=channel, id=id)
