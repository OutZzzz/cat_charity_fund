from pydantic import Field

from .base import ProjectBase


class CharityProjectGet(ProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
