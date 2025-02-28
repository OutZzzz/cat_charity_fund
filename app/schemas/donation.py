from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationUserDB(BaseModel):
    full_amount: int = Field(..., gt=0)
    id: int
    comment: Optional[str]
    create_date: datetime

    class Config:
        orm_mode = True


class DonationSuperUserDB(DonationUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]