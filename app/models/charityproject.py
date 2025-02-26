from sqlalchemy import Column, Text, String

from app.models.base import BaseDonationModel


""" class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False)
    fully_invested = Column(Boolean, nullable=False)
    create_date = Column(DateTime, nullable=False)
    close_date = Column(DateTime, nullable=True) """


class CharityProject(BaseDonationModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
