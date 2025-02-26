from datetime import datetime
from sqlalchemy import (
    Column, Integer, Boolean, DateTime)

from app.core.db import Base


class BaseDonationModel(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, nullable=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime, nullable=True)
