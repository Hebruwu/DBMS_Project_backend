from dataclasses import dataclass
import datetime
from dataclasses_json import dataclass_json
from sqlalchemy import CHAR, Column, DateTime, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""


class ADMIN(Base):
    __tablename__ = 'ADMIN'

    AID: int = Column(Integer, primary_key=True)
    NAME: str = Column(String(250), nullable=False)
    USERNAME: str = Column(String(250), nullable=False, unique=True)
    PASSWORD: str = Column(String(1000), nullable=False)
    EMAIL: str = Column(String(250), nullable=False, unique=True)

    EVENT = relationship('EVENT', back_populates='ADMIN_')

class STUDENT(Base):
    __tablename__ = 'STUDENT'

    SID: int = Column(Integer, primary_key=True)
    GENDER: str = Column(CHAR(1), nullable=False)
    NAME: str = Column(String(250), nullable=False)
    USERNAME: str = Column(String(250), nullable=False, unique=True)
    PASSWORD: str = Column(String(1000), nullable=False)
    EMAIL: str = Column(String(250), nullable=False, unique=True)
    RACE: str = Column(String(250))
    DEPARTMENT: str = Column(String(250))
    MAJOR: str = Column(String(250))
    CITIZENSHIP: str = Column(String(250), nullable=False)
    YEAR: str = Column(String(250))

    INVITED_TO = relationship('INVITEDTO', back_populates='STUDENT_')
    PROVIDES_FEEDBACK = relationship('PROVIDESFEEDBACK', back_populates='STUDENT_')


class EVENT(Base):
    __tablename__ = 'EVENT'
    __table_args__ = (
        ForeignKeyConstraint(['E_AID'], ['ADMIN.AID'], name='EVENT_fk0'),
    )

    EID: int = Column(Integer, primary_key=True)
    NAME: str = Column(String(250), nullable=False)
    DATE_FROM: datetime.datetime = Column(DateTime, nullable=False)
    DATE_TO: datetime.datetime = Column(DateTime, nullable=False)
    EVENT_TYPE: str = Column(String(250), nullable=False)
    MODALITY: str = Column(String(250), nullable=False)
    LOCATION: str = Column(String(500), nullable=False)
    E_AID: int = Column(Integer, nullable=False, index=True)
    DESCRIPTION: str = Column(String(1000))

    ADMIN_ = relationship('ADMIN', back_populates='EVENT')
    INVITED_TO = relationship('INVITEDTO', back_populates='EVENT_')
    PROVIDES_FEEDBACK = relationship('PROVIDESFEEDBACK', back_populates='EVENT_')


class INVITEDTO(Base):
    __tablename__ = 'INVITED_TO'
    __table_args__ = (
        ForeignKeyConstraint(['I_EID'], ['EVENT.EID'], name='INVITED_TO_fk1'),
        ForeignKeyConstraint(['I_SID'], ['STUDENT.SID'], name='INVITED_TO_fk0')
    )

    I_SID: int = Column(Integer, primary_key=True, nullable=False)
    I_EID: int = Column(Integer, primary_key=True, nullable=False, index=True)
    ATTENDING: str = Column(String(3))

    EVENT_ = relationship('EVENT', back_populates='INVITED_TO')
    STUDENT_ = relationship('STUDENT', back_populates='INVITED_TO')


class PROVIDESFEEDBACK(Base):
    __tablename__ = 'PROVIDES_FEEDBACK'
    __table_args__ = (
        ForeignKeyConstraint(['P_EID'], ['EVENT.EID'], name='PROVIDES_FEEDBACK_fk1'),
        ForeignKeyConstraint(['P_SID'], ['STUDENT.SID'], name='PROVIDES_FEEDBACK_fk0')
    )

    P_SID: int = Column(Integer, primary_key=True, nullable=False)
    P_EID: int = Column(Integer, primary_key=True, nullable=False, index=True)
    FEEDBACK: str = Column(String(1000), nullable=False)

    EVENT_ = relationship('EVENT', back_populates='PROVIDES_FEEDBACK')
    STUDENT_ = relationship('STUDENT', back_populates='PROVIDES_FEEDBACK')
