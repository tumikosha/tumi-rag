import uuid
from typing import List

from pydantic import BaseModel, Field


class PutQuery(BaseModel):
    """  Put new record to DB """

    url: str = Field(
        default=None, title="", max_length=300,
        description="Любая строка уникальная для пользователя"
    )

    article: str = Field(
        default=None, title="", max_length=16000,
        description="text for embeddings"
    )

    tags: list[str] = Field(
        default=[], title="", max_length=300,
        description="text for embeddings"
    )

    workspace: str | None = Field(
        default=None, title="", max_length=30,
        description="text for embeddings"
    )

    ip: str | None = Field(
        default="0.0.0.0", max_length=40,
        description="ip4 or ip6"
    )
