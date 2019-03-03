from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#table to store user information
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

#table to store list of US States
class State(Base):
    __tablename__ = 'state'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

#table to store list of months
class Month(Base):
    __tablename__ = 'month'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

#table to store race categories
class RaceCat(Base):
    __tablename__ = 'race_cat'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    units = Column(String(2))
    distance = Column(Float)
    terrain = Column(String(250))

    #JSON setup
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'distance': self.distance,
            'units': self.units,
            'terrain': self.terrain
        }

#table to store individual races
class RaceItem(Base):
    __tablename__ = 'race_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    utmb_points = Column(String(5))
    wser_qualifier = Column(String(5))
    race_cat_id = Column(Integer, ForeignKey('race_cat.id'))
    race_cat = relationship(RaceCat)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    state_id = Column(Integer, ForeignKey('state.name'))
    state = relationship(State)
    month_id = Column(Integer, ForeignKey('month.name'))
    month = relationship(Month)
    race_website = Column(String(250))

    #JSON
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'distance': self.distance,
            'units': self.units,
            'race_cat': self.race_cat,
            'utmb_points': self.utmb_points,
            'wser_qualifier': self.wser_qualifier,
            'race_website': self.race_website,
            'state': self.state,
            'month': self.month
        }

#create db
engine = create_engine('sqlite:///ultramarathons.db')


Base.metadata.create_all(engine)
