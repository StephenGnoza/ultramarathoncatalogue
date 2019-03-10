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


# add months
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

# add months
states = [
    State(name="Alabama"),
    State(name="Alaska"),
    State(name="Arizona"),
    State(name="Arkansas"),
    State(name="California"),
    State(name="Colorado"),
    State(name="Connceticut"),
    State(name="Delaware"),
    State(name="Florida"),
    State(name="Georgia"),
    State(name="Hawaii"),
    State(name="Idaho"),
    State(name="Illinois"),
    State(name="Indiana"),
    State(name="Iowa"),
    State(name="Kansas"),
    State(name="Kentucky"),
    State(name="Louisiana"),
    State(name="Maine"),
    State(name="Maryland"),
    State(name="Massachusetts"),
    State(name="Michigan"),
    State(name="Minnesota"),
    State(name="Mississippi"),
    State(name="Missouri"),
    State(name="Montana"),
    State(name="Nebraska"),
    State(name="Nevada"),
    State(name="New Hampshire"),
    State(name="New Jersey"),
    State(name="New York"),
    State(name="North Carolina"),
    State(name="North Dakota"),
    State(name="Ohio"),
    State(name="Oklahoma"),
    State(name="Oregon"),
    State(name="Pennsylvania"),
    State(name="Rhode Island"),
    State(name="South Carolina"),
    State(name="South Dakota"),
    State(name="Tennessee"),
    State(name="Texas"),
    State(name="Utah"),
    State(name="Vermont"),
    State(name="Virginia"),
    State(name="Washington"),
    State(name="West Virginia"),
    State(name="Wisconsin"),
    State(name="Wyoming")
]
session.bulk_save_objects(states)
session.commit()

# add Race Categories
RaceCat = [
    RaceCat(name="50K - Trail", units="km", distance="50", terrain="trail"),
    RaceCat(name="60K - Trail", units="km", distance="60", terrain="trail"),
    RaceCat(name="100K - Trail", units="km", distance="100", terrain="trail"),
    RaceCat(name="50mi - Trail", units="mi", distance="50", terrain="trail"),
    RaceCat(name="100mi - Trail", units="mi", distance="100", terrain="trail"),
    RaceCat(name="50K - Road", units="km", distance="50", terrain="road"),
    RaceCat(name="60K - Road", units="km", distance="60", terrain="road"),
    RaceCat(name="100K - Road", units="km", distance="100", terrain="road"),
    RaceCat(name="50mi - Road", units="mi", distance="50", terrain="road"),
    RaceCat(name="100mi - Road", units="mi", distance="100", terrain="road")
]
session.bulk_save_objects(RaceCat)
session.commit()
