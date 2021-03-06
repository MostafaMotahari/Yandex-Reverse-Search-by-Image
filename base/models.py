from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    BigInteger
)

from base_class import Base


class UserModel(Base):
    __tablename__ = "users"

    primary_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    total_searches = Column(Integer, unique=False, nullable=False, default=0)
    is_admin = Column(Boolean, unique=False, nullable=False, default=False)
    is_vrefied = Column(Boolean, unique=False, nullable=False, default=False)
    is_superuser = Column(Boolean, unique=False, nullable=False, default=False)
    is_banned = Column(Boolean, unique=False, nullable=False, default=False)
