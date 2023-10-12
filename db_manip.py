from typing import List, Optional
from sqlalchemy import (ForeignKey,
                        String,
                        create_engine,
                        select
)
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship,
                            Session
)
from datetime import date, time
import os

class Base (DeclarativeBase):
    pass

class User (Base):
    __tablename__="user_account"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(10))
    fpath:Mapped[str] = mapped_column(String)
    fullname: Mapped[Optional[str]]
    audio_fn: Mapped[List["Audio_Files"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    text_fn: Mapped[List["Text_Files"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, name={self.name!r}, fpath={self.fpath!r}, fullname={self.fullname!r})"
    
class Audio_Files (Base):
    __tablename__="audio_files"
    
    audio_id: Mapped[int] = mapped_column(primary_key=True)
    audio_date: Mapped[int]
    audio_time: Mapped[int]
    audio_fname: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_id"))
    user: Mapped["User"] = relationship(back_populates="audio_fn")
    
    def __repr__(self) -> str:
        return f"Audio_Files(audio_id={self.audio_id!r}, date={str(self.audio_date)[:4]+'-'+str(self.audio_date)[4:6]+'-'+str(self.audio_date)[6:]!r}, time={str(self.audio_time)[:2]+':'+str(self.audio_time)[2:4]+':'+str(self.audio_time)[4:]!r}, file_name={self.audio_fname!r}, user={self.user!r} )"
    
class Text_Files (Base):
    __tablename__="text_files"
    
    text_id: Mapped[int] = mapped_column(primary_key=True)
    text_date: Mapped[int]
    text_time: Mapped[int]
    text_fname: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_id"))
    user: Mapped["User"] = relationship(back_populates="text_fn")
    
    def __repr__(self) -> str:
        return f"Text_Files(text_id={self.text_id!r}, date={str(self.text_date)[:4]+'-'+str(self.text_date)[4:64]+'-'+str(self.text_date)[6:]!r}, time={str(self.text_time)[:2]+':'+str(self.text_time)[2:4]+':'+str(self.text_time)[4:]!r}, file_name={self.text_fname!r}, user={self.user!r} )"

def initdb():
    engine = create_engine("sqlite:///assistant_dbase.db", echo=True)
    if os.path.exists("assistant_dbase.db"):
        print ("DB already exists")
    else:
        print("Creating Database")
        Base.metadata.create_all(engine)
    return engine

def add_user (newuser, fulln=""):
    engine=initdb()
    with Session(engine) as session:
        if fulln != "" :
            nuser=User(
                name=newuser,
                fpath=os.path.join(os.getcwd(),"sounds",newuser),
                fullname=fulln,
                )
        else:
            nuser=User(
            name=newuser,
            fpath=os.path.join(os.getcwd(),"sounds",newuser),
            )

        session.add(nuser)
        session.commit()
        
def add_audiofile (fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.audio_fn.append(Audio_Files(
            audio_date=fname[1],
            audio_time=fname[2],
            audio_fname=fname[3]+".flac",
        ))
        session.commit()


def del_audiofile(fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=(
            select(Audio_Files)
            .join(Audio_Files.user)
            .where(User.name==fname[4])
            .where(Audio_Files.audio_date==fname[1])
        )
        user1_af=session.scalars(stmt).one()
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.audio_fn.remove(user1_af)
        session.flush()
        session.commit()

def get_users(withfiles=False):
    engine=initdb()
    userlist=list()
    with Session(engine) as session:
        users_list = select(User)
        for user in session.scalars(users_list):
            if not withfiles :
                userlist.append(user.name)
            else:
                audios_user=(
                    select(Audio_Files)
                    .join(Audio_Files.user)
                    .where(User.name == user.name)
                    )
                if session.scalars(audios_user).first()!=None :
                    userlist.append(user.name)
            
        session.commit()
    print(userlist)
    return userlist

def get_audiodates(username):
    engine=initdb()
    files_list=list()
    with Session(engine) as session:
        audios_user=(
                select(Audio_Files)
                .join(Audio_Files.user)
                .where(User.name == username)
                )
        for audio_fn in session.scalars(audios_user):
            #elem=[date(int(str(audio_fn.audio_date)[:4]), int(str(audio_fn.audio_date)[4:6]), int(str(audio_fn.audio_date)[6:])),
            #      time(int(str(audio_fn.audio_time)[:2]), int(str(audio_fn.audio_time)[2:4]), int(str(audio_fn.audio_time)[4:]))]
            #print(date(int(str(audio_fn.audio_date)[:4]), int(str(audio_fn.audio_date)[4:6]), int(str(audio_fn.audio_date)[6:])))
            files_list.append([date(int(str(audio_fn.audio_date)[:4]), int(str(audio_fn.audio_date)[4:6]), int(str(audio_fn.audio_date)[6:])),
                               time(int(str(audio_fn.audio_time)[:2]), int(str(audio_fn.audio_time)[2:4]), int(str(audio_fn.audio_time)[4:]))])
        session.commit()
    #print(type(files_list[0][0]))
    return files_list
    
#get_audiofiles("Père")

""" 
#session=Session(engine)


    
#audios_user1= (
#    select(Audio_Files)
#    .join(Audio_Files.user)
#    .where(User.name == "Père")
#)

#for audio_fn in session.scalars(audios_user1):
#    print (date(int(str(audio_fn.audio_date)[:4]), 
#                int(str(audio_fn.audio_date)[4:6]),
#                int(str(audio_fn.audio_date)[6:]))
#           )








stmt=select(User).where(User.name=="Père")#fname[4])
user1=session.scalars(stmt).one()
print (user1.user_id)

"""