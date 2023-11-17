from dataclasses import asdict
import datetime
import hashlib
import sqlalchemy as database
from sqlalchemy.orm import Session
from .db import ADMIN, EVENT, INVITEDTO, PROVIDESFEEDBACK, STUDENT
from typing import Optional, List
from sqlalchemy import any_, or_

class DBException(Exception):
    pass

def get_engine():
    connection_url = "mysql+pymysql://root:CSD%40mysql-1872@localhost:3306/eventhosting"
    engine = database.create_engine(connection_url, echo=True)
    return engine

def insert_event(engine,
                 q_name: str,
                 q_date_from: datetime.datetime,
                 q_date_to: datetime.datetime,
                 q_e_type: str,
                 q_modality: str,
                 q_location: str,
                 q_E_AID: int,
                 q_description: Optional[str]) -> None:
      event = EVENT(NAME=q_name,
                    DATE_FROM=q_date_from,
                    DATE_TO=q_date_to,
                    EVENT_TYPE=q_e_type,
                    MODALITY=q_modality,
                    LOCATION=q_location,
                    E_AID=q_E_AID,
                    DESCRIPTION=q_description)
      #Session = sessionmaker(engine)
      with Session(engine) as session:
        try:
            session.add(event)
            session.commit()
        except Exception as e:
            raise DBException("Occured at event insert\n", e)
        


def insert_admin(engine,
                 q_name: str,
                 q_username: str,
                 q_password: str,
                 q_email: str) -> None:
    """hash_obj = hashlib.sha256()
    hash_obj.update(q_password.encode())
    q_password = hash_obj.hexdigest()"""
    admin = ADMIN(NAME = q_name,
                  USERNAME = q_username,
                  PASSWORD = q_password,
                  EMAIL = q_email)
    with Session(engine) as session:
        try:
            session.add(admin)
            session.commit()
        except Exception as e:
            raise DBException("Occured at admin insert\n", e)
        
def insert_student(engine,
                 q_name: str,
                 q_username: str,
                 q_password: str,
                 q_email: str,
                 q_race: Optional[str],
                 q_dept: Optional[str],
                 q_major: Optional[str],
                 q_citizenship: str,
                 q_year: Optional[str],
                 q_gender: str) -> None:
    """hash_obj = hashlib.sha256()
    hash_obj.update(q_password.encode())
    q_password = hash_obj.hexdigest()"""
    student = STUDENT(NAME = q_name,
                  USERNAME = q_username,
                  PASSWORD = q_password,
                  EMAIL = q_email,
                  RACE = q_race,
                  DEPARTMENT = q_dept,
                  MAJOR = q_major,
                  CITIZENSHIP = q_citizenship,
                  YEAR = q_year,
                  GENDER = q_gender)
    with Session(engine) as session:
        try:
            session.add(student)
            session.commit()
        except Exception as e:
            raise DBException("Occured at student insert\n", e)
    
def authenticate_admin(engine,
                       q_username: str,
                       q_password: str) -> bool:
    """hash_obj = hashlib.sha256()
    hash_obj.update(q_password.encode())
    q_password = hash_obj.hexdigest()"""
    query = database.select(ADMIN).where((ADMIN.USERNAME == q_username) & (ADMIN.PASSWORD == q_password))
    with Session(engine) as session:
        try:
            authenticated = True if len(session.scalars(query).all()) == 1 else False
        except Exception as e:
            raise DBException("Occured at admin authentication\n", e)
    return authenticated

def authenticate_student(engine,
                       q_username: str,
                       q_password: str) -> bool:
    """hash_obj = hashlib.sha256()
    hash_obj.update(q_password.encode())
    q_password = hash_obj.hexdigest()"""
    query = database.select(STUDENT).where((STUDENT.USERNAME == q_username) & (STUDENT.PASSWORD == q_password))
    with Session(engine) as session:
        try:
            authenticated = True if len(session.scalars(query).all()) == 1 else False
        except Exception as e:
            raise DBException("Occured at student authentication\n", e)
    return authenticated

# SELECT * FROM EVENT
# Returns a list of EVENT objects
def get_events(engine) -> List[EVENT]:
    query = database.select(EVENT)
    with Session(engine) as session:
        try:
            events = session.scalars(query).all()
        except Exception as e:
            raise DBException("Occured at get_events\n", e)
    return events

# SELECT * FROM STUDENT where MAJOR LIKE
# Returns a list of STUDENT objects
def get_students(engine, q_major: List[str] = ["%"], q_citizenship: List[str] = ["%"], q_race: List[str] = ["%"], q_gender: List[str] = ["%"]) -> List[STUDENT]:

    query = database.select(STUDENT).filter((or_(*[STUDENT.MAJOR.like(major) for major in q_major])) &
                                             (or_(*[STUDENT.CITIZENSHIP.like(citizenship) for citizenship in q_citizenship])) &
                                            (or_(*[STUDENT.RACE.like(race) for race in q_race])) & 
                                            (or_(*[STUDENT.GENDER.like(gender) for gender in q_gender])))
    with Session(engine) as session:
        try:
            students = session.scalars(query).all()
        except Exception as e:
            raise DBException("Occured at get_students\n", e)
    return students

def get_student(engine, q_username: str) -> STUDENT:
    student_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            student = session.scalars(student_query).one()
        except Exception as e:
            raise DBException("Occured at get_student\n", e)
    return student

def get_admin(engine, q_username: str) -> ADMIN:
    admin_query = database.select(ADMIN).where(ADMIN.USERNAME == q_username)
    with Session(engine) as session:
        try:
            admin = session.scalars(admin_query).one()
        except Exception as e:
            raise DBException("Occured at get_admin\n", e)
    return admin


    
def insert_invite(engine,
                  q_username: Optional[str],
                  q_eid: int, q_sid: int = -1) -> None:
    student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            if q_sid == -1:
                student_id = session.scalars(student_id_query).all()
                student_id = student_id[0].SID
            else:
                student_id = q_sid
            invited_to = INVITEDTO(I_SID = student_id,
                      I_EID = q_eid,
                      ATTENDING = None)
            session.add(invited_to)
            session.commit()

        except Exception as e:
            raise DBException("Occured at insert_invite\n", e)

def update_invite(engine,
                  q_username: str,
                  q_eid: int,
                  attending: str) -> None:
    student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            student_id = session.scalars(student_id_query).one()
            student_id = asdict(student_id)
            student_id = student_id["SID"]
            invite_query = database.select(INVITEDTO).where(
                (INVITEDTO.I_SID == student_id) &
                (INVITEDTO.I_EID == q_eid)
            )
            invite = session.execute(invite_query).scalar_one()
            invite.ATTENDING = attending
            session.commit()


        except Exception as e:
            raise DBException("Occured at update_invite\n", e)
def insert_feedback(engine,
                    q_username: str,
                    q_eid: int,
                    feedback: str) -> None:
    student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            student_id = session.scalars(student_id_query).one()
            student_id = asdict(student_id)
            student_id = student_id["SID"]
            feedback = PROVIDESFEEDBACK(P_SID = student_id,
                      P_EID = q_eid,
                      FEEDBACK = feedback)
            session.add(feedback)
            session.commit()

        except Exception as e:
            raise DBException("Occured at insert_feedback\n", e)

def update_feedback(engine,
                  q_username: str,
                  q_eid: int,
                  feedback: str) -> None:
    student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            student_id = session.scalars(student_id_query).all()
            student_id = student_id[0].SID
            feedback_query = database.select(PROVIDESFEEDBACK).where(
                (PROVIDESFEEDBACK.P_SID == student_id) &
                (PROVIDESFEEDBACK.P_EID == q_eid)
            )
            feedback_obj = session.execute(feedback_query).scalar_one()
            feedback_obj.FEEDBACK = feedback
            session.commit()
        except Exception as e:
            raise DBException("Occured at insert_feedback\n", e)
        
def delete_event(engine,
                 q_eid: int) -> None:
    event_query = database.select(EVENT).where(
                EVENT.EID == q_eid
            )
    with Session(engine) as session:
        try:
            event = session.execute(event_query).scalar_one()
            session.delete(event)
            session.commit()
        except Exception as e:
            raise DBException("Occured at delete_event\n", e)
        
def delete_invite(engine,
                  q_username: str,
                  q_eid: int,
                  attending: str, q_sid = -1) -> None:
    student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
    with Session(engine) as session:
        try:
            if q_sid == -1:
                student_id = session.scalars(student_id_query).all()
                student_id = student_id[0].SID
            else:
                student_id = q_sid
            invite_query = database.select(INVITEDTO).where(
                (INVITEDTO.I_SID == student_id) &
                (INVITEDTO.I_EID == q_eid)
            )
            invite = session.execute(invite_query).scalar_one()
            session.delete(invite)
            session.commit()


        except Exception as e:
            raise DBException("Occured at update_invite\n", e)
def get_invites(engine,
                q_username: Optional[str] = None) -> any:
    invite_query = None
    
    with Session(engine) as session:
        invites = None
        try:
            if q_username is not None:
                student_id_query = database.select(STUDENT).where(STUDENT.USERNAME == q_username)
                student_id = session.scalars(student_id_query).one()
                student_id = asdict(student_id)
                student_id = student_id["SID"]
                invite_query = database.select(INVITEDTO, EVENT).where(INVITEDTO.I_SID == student_id).join(EVENT, EVENT.EID == INVITEDTO.I_EID)
                invites = session.execute(invite_query).all()
            else:
                invites = session.scalars(database.select(INVITEDTO)).all()
        except Exception as e:
            raise DBException("Occured at get_invite\n", e)
        return invites[0]
def get_feedback(engine,
                q_eid: Optional[int] = None) -> any:
    feedback_query = None
    
    with Session(engine) as session:
        feedback_objs = None
        try:
            if q_eid is not None:
                feedback_query = database.select(PROVIDESFEEDBACK, STUDENT).where(
                PROVIDESFEEDBACK.P_EID == q_eid
            ).join(STUDENT, STUDENT.SID == PROVIDESFEEDBACK.P_SID)
                feedback_objs = session.execute(feedback_query).all()
            else:
                feedback_objs = session.scalars(database.select(PROVIDESFEEDBACK)).all()
        except Exception as e:
            raise DBException("Occured at get_feedback\n", e)
        return feedback_objs[0]


        

def main():
    engine = get_engine()
    get_events(engine)
if __name__ == "__main__":
    main()
    

