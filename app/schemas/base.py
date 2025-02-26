from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime]