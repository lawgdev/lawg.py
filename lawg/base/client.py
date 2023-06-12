from abc import ABC, abstractmethod

from marshmallow import Schema

from lawg.base.log import BaseLog
from lawg.base.rest import BaseRest
from lawg.schemas import ProjectNameSchema, ProjectNamespaceSchema


class BaseClient(ABC):
    rest: BaseRest

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token

    @abstractmethod
    def create(
        self,
        name: str,
        namespace: str,
    ) -> BaseLog:
        ...
        # schema = CreateProjectSchema()
        # schema.validate({"name": name, "namespace": namespace})

    def edit(
        self,
        id: str,
        name: str,
        namespace: str,
    ) -> BaseLog:
        ...
