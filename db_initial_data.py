from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, State, Month, RaceCat, RaceItem

engine = create_engine('sqlite:///ultramarathons.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#add months
months = [
    Month(name="January"),
    Month(name="February"),
    Month(name="March"),
    Month(name="April"),
    Month(name="May"),
    Month(name="June"),
    Month(name="July"),
    Month(name="August"),
    Month(name="September"),
    Month(name="October"),
    Month(name="November"),
    Month(name="December")
]
session.bulk_save_objects(months)
session.commit()

#add months
states = [
    State(name="Alabama"),
    State(name="Alaska"),
    State(name="Arizona"),
    State(name="Arkansas"),
    State(name="California"),
    State(name="Colorado"),
    State(name="Connceticut")
]
session.bulk_save_objects(states)
session.commit()

#add Race Categories
RaceCat = [
    RaceCat(name="50K - Trail", units="km", distance="50", terrain="trail" ),
    RaceCat(name="60K - Trail", units="km", distance="60", terrain="trail" ),
    RaceCat(name="100K - Trail", units="km", distance="100", terrain="trail" ),
    RaceCat(name="50mi - Trail", units="mi", distance="50", terrain="trail" ),
    RaceCat(name="100mi - Trail", units="mi", distance="100", terrain="trail" )
]
session.bulk_save_objects(RaceCat)
session.commit()
