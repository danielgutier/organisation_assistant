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
from datetime import datetime, date, time
import os
import locale
# Linux based system
#locale.setlocale(locale.LC_TIME,'fr_CH.utf8')
# Windows based system
locale.setlocale(locale.LC_TIME,'fr_FR')

class Base (DeclarativeBase):
    pass

# Users Table
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

# Audio table
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

# Text table
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

# ORM Engine initialisation
def initdb():
    dbname="db_assistant.db"
    engine = create_engine("sqlite:///"+dbname, echo=True)
    if os.path.exists(dbname):
        print ("DB already exists")
    else:
        print("Creating Database")
        Base.metadata.create_all(engine)
    return engine

# Add user to the database function
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
        
# Delete user of the database function
def del_user (deluser):
    engine=initdb()
    with Session(engine) as session:
        stmt=select(User).where(User.name==deluser)
        user1=session.scalars(stmt).one()
        session.delete(user1)
        session.commit()

# Get user(s) function : withfiles can be an audio filename(single user)
# or a boolean flag if we need users with files
def get_users(withfiles=False):
    engine=initdb()
    userlist=list()
    
    with Session(engine) as session:
        users_list = select(User)
        print (users_list)
        for user in session.scalars(users_list):
            audios_user=(
                select(Audio_Files)
                .join(Audio_Files.user)
                .where(User.name == user.name)
                )
            if isinstance(withfiles, str) :
                for audiof in session.scalars(audios_user).all():
                    if audiof.audio_fname == withfiles :
                        userlist=user.name
            elif not withfiles :
                userlist.append(user.name)
            elif session.scalars(audios_user).first()!=None :
                userlist.append(user.name)

    session.commit()
    print(userlist)
    return userlist

# Add audiofile to the database
def add_audiofile (fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.audio_fn.append(Audio_Files(
            audio_date=fname[1],
            audio_time=fname[2],
            audio_fname=fname[3]+".mp3",
        ))
        session.commit()
        
# Remove audiofile of the database
def del_audiofile(fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=(
            select(Audio_Files)
            .join(Audio_Files.user)
            .where(User.name==fname[4])
            .where(Audio_Files.audio_date==fname[1])
            .where(Audio_Files.audio_time==fname[2])
        )
        user1_af=session.scalars(stmt).one()
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.audio_fn.remove(user1_af)
        session.flush()
        session.commit()
        
# Remove Text file from the database
def del_textfile(fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=(
            select(Text_Files)
            .join(Text_Files.user)
            .where(User.name==fname[4])
            .where(Text_Files.text_date==fname[1])
            .where(Text_Files.text_time==fname[2])
        )
        user1_tf=session.scalars(stmt).one()
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.text_fn.remove(user1_tf)
        session.flush()
        session.commit()

# Retreive dates and times of a user's audio files
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
            # tests if time database 00h00m00s
            if not str(audio_fn.audio_time)[:-4]:
                h=0
            else:
                h=int(str(audio_fn.audio_time)[:-4])
                
            if not str(audio_fn.audio_time)[-4:-2]:
                m=0
            else:
                m=int(str(audio_fn.audio_time)[-4:-2])
                
            if not str(audio_fn.audio_time)[-2:]:
                s=0
            else:
                s=int(str(audio_fn.audio_time)[-2:])
            files_list.append([date(int(str(audio_fn.audio_date)[:4]), int(str(audio_fn.audio_date)[4:6]), int(str(audio_fn.audio_date)[6:])),
                               time(h, m, s)])
        session.commit()
    return files_list

# Retreive file liste beyond a date
def get_audiof_date(limit_date):
    engine=initdb()
    files_list=list()
    with Session(engine) as session:
        audios=(
                select(Audio_Files)
                .where(Audio_Files.audio_date <= limit_date)
        )
        for audio_fn in session.scalars(audios):
            files_list.append(audio_fn.audio_fname)
        session.commit()
    return files_list

# Retreive audio file name from a date item of the menu
def get_audiofile_name(menu_item):
    datetime_obj=datetime.strptime(str(menu_item), "%A %d %B %Y à %H:%M:%S")
    engine=initdb()
    with Session(engine) as session:
        audio_file=(
            select(Audio_Files)
            .where(Audio_Files.audio_date==datetime_obj.strftime("%Y%m%d"))
            .where(Audio_Files.audio_time==datetime_obj.strftime("%H%M%S"))
        )
        audio_fn=session.scalars(audio_file).one().audio_fname
        session.commit()
    return audio_fn

# Add a text file to the database
def add_textfile (fname):
    engine=initdb()
    with Session(engine) as session:
        stmt=select(User).where(User.name==fname[4])
        user1=session.scalars(stmt).one()
        user1.text_fn.append(Text_Files(
            text_date=fname[1],
            text_time=fname[2],
            text_fname=fname[3]+".txt",
        ))
        session.commit()

# Retreive dates and times of a user's text files
def get_textdates(username):
    engine=initdb()
    files_list=list()
    with Session(engine) as session:
        texts_user=(
                select(Text_Files)
                .join(Text_Files.user)
                .where(User.name == username)
                )
        for text_fn in session.scalars(texts_user):
            # tests if time database 00h00m00s
            if not str(text_fn.text_time)[:-4]:
                h=0
            else:
                h=int(str(text_fn.text_time)[:-4])
                
            if not str(text_fn.text_time)[-4:-2]:
                m=0
            else:
                m=int(str(text_fn.text_time)[-4:-2])
                
            if not str(text_fn.text_time)[-2:]:
                s=0
            else:
                s=int(str(text_fn.text_time)[-2:])
            files_list.append([date(int(str(text_fn.text_date)[:4]), int(str(text_fn.text_date)[4:6]), int(str(text_fn.text_date)[6:])),
                               time(h, m, s)])
        session.commit()
    return files_list

# Retreive text file name from date menu item
def get_textfile_name(menu_item):
    datetime_obj=datetime.strptime(str(menu_item), "%A %d %B %Y à %H:%M:%S")
    engine=initdb()
    with Session(engine) as session:
        text_file=(
            select(Text_Files)
            .where(Text_Files.text_date==datetime_obj.strftime("%Y%m%d"))
            .where(Text_Files.text_time==datetime_obj.strftime("%H%M%S"))
        )
        text_fn=session.scalars(text_file).one().text_fname
        session.commit()
    return text_fn
