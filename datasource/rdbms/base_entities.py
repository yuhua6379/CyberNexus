from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import AbstractConcreteBase

Base = None


def set_base(base):
    global Base
    Base = base


class OrmBaseModel(AbstractConcreteBase):
    """抽象基类"""
    __tablename__ = None
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键')
    create_time = Column(DateTime, default=datetime.now, comment='创建时间')
    update_time = Column(DateTime, nullable=True, onupdate=datetime.now, comment='修改时间')
    deleted = Column(Boolean, nullable=False, default=False, comment="软删除标记")
