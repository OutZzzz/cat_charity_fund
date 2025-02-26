from sqlalchemy import (
    Column, Text, Integer, ForeignKey)

from app.models.base import BaseDonationModel


class Donation(BaseDonationModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
