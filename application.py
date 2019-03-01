from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, State, Month, RaceCat, RaceItem


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///ultramarathons.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Make queries likely needed for every route
months = session.query(Month).order_by(Month.id)
states = session.query(State).order_by(State.id)
racecats = session.query(RaceCat).order_by(RaceCat.name)


@app.route('/')
def HomePage():
    return render_template('distances.html', months=months, states=states, racecats=racecats)

@app.route('/racecat/<int:racecat_id>')
def RaceCatList(racecat_id):
    races = session.query(RaceItem).order_by(RaceItem.name)
    racecat = session.query(RaceCat).filter_by(id=racecat_id).one()
    return render_template('races.html', months=months, states=states, racecats=racecats, races=races, racecat=racecat)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
