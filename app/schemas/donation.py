from typing import Optional

from .base import ProjectBase


class DonationBaseGetAll(ProjectBase):
    user_id: int
    comment: Optional[str]