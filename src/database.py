from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
from uuid import uuid4

engine = create_engine(environ.get('CONN_STRING'))
metadata = MetaData()
base = declarative_base()


class Link(base):
    __tablename__ = 'links'
    id = Column('id', String(37), primary_key=True),
    link = Column('link', String(100), nullable=False),
    status_code = Column('status', Integer),
    parent = Column('parent', String(100)),
    error = Column('error', String(100))


metadata.create_all(engine, checkfirst=True)


def save_url(current_url, status_code, parent_url, error=None):
    maker = sessionmaker(bind=engine)
    session = maker()
    new_link = Link(id=str(uuid4()), link=current_url,status_code=status_code, parent_url=parent_url, error=error)
    session.add(new_link)
    session.commit()


def get_my_node(current_url):
    maker = sessionmaker(bind=engine)
    session = maker()
    return session.query(Link).filter(Link.link == current_url).first()


def was_crawled(current_url):
    maker = sessionmaker(bind=engine)
    session = maker()
    return session.query(Link).filter(Link.link == current_url).count() > 0
