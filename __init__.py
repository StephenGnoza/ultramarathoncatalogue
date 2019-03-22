# import for basic webpage, database
from flask import Flask, render_template, request, redirect, url_for, jsonify,\
    make_response, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, State, Month, RaceCat, RaceItem
# import for login
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import session as login_session
import httplib2
import random
import string
# import for json
import json
import requests

app = Flask(__name__)

# CLIENT_ID = json.loads(
#    open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Ultra Marathon Catalogue"

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:catalog@localhost/ultramarathons')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON API
# all races
@app.route('/races/JSON')
def RacesJSON():
    races = session.query(RaceItem).all()
    return jsonify(RaceItem=[i.serialize for i in races])


# particular race
@app.route('/race/<int:race_id>/JSON')
def RaceJSON(race_id):
    races = session.query(RaceItem).filter_by(id=race_id).all()
    return jsonify(RaceItem=[i.serialize for i in races])


# particular category
@app.route('/racecat/<int:race_cat_id>/JSON')
def RaceCatJSON(race_cat_id):
    races = session.query(RaceItem).filter_by(race_cat_id=race_cat_id).all()
    return jsonify(RaceItem=[i.serialize for i in races])


# Make queries likely needed for every route
months = session.query(Month).order_by(Month.id)
states = session.query(State).order_by(State.id)
racecats = session.query(RaceCat).order_by(RaceCat.name)


# Login Page
@app.route('/login')
def LoginPage():
    # create token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', months=months, states=states,
                           racecats=racecats, STATE=state)


# validate and get info from Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
                                            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)

    login_session['username'] = data['email']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    user = session.query(User).filter_by(email=email).one()
    return user.id


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/logout')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        races = session.query(RaceItem).all()
        return redirect(url_for('HomePage'))
    else:
        response = make_response(json.dumps('Failed to revoke token \
                                 for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        return response


# default page
@app.route('/')
def HomePage():
    races = session.query(RaceItem).all()
    return render_template('races_all.html', months=months, states=states,
                           racecats=racecats, races=races)


# list races by category
@app.route('/racecat/<int:race_cat_id>')
def RaceCatList(race_cat_id):
    races = session.query(RaceItem).filter_by(race_cat_id=race_cat_id)
    racecat = session.query(RaceCat).filter_by(id=race_cat_id).one_or_none()
    if racecat is None:
        error_msg = "No such category"
        return render_template('races_all.html', months=months, states=states,
                               racecats=racecats, races=races,
                               error_msg=error_msg)
    else:
        return render_template('races.html', months=months, states=states,
                               racecats=racecats, races=races, racecat=racecat,
                               race_cat_id=race_cat_id)


# race page
@app.route('/race/<int:race_id>')
def RacePage(race_id):
    race = session.query(RaceItem).filter_by(id=race_id).one_or_none()
    if race is None:
        error_msg = "Race not found."
        return render_template('races_all.html', months=months, states=states,
                               racecats=racecats, error_msg=error_msg)
    else:
        return render_template('race.html', months=months, states=states,
                               racecats=racecats, race=race)


# add race
@app.route('/race/add', methods=['GET', 'POST'])
def addRacePage():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        error = False

        # make sure that the race has a name
        if request.form['race_add_name'] == "":
            error = True
            error_msg = "You must enter a race name"
            return render_template('race_add.html', months=months,
                                   states=states, racecats=racecats,
                                   error_msg=error_msg)

        # make sure that this name hasnt already been used
        name_check = request.form['race_add_name']
        race_names = session.query(RaceItem).filter_by(name=name_check).all()
        for race_name in race_names:
            if race_name.name == name_check:
                error = False
                error_msg = "There is already a race with this name"
                return render_template('race_add.html', months=months,
                                       states=states, racecats=racecats,
                                       error_msg=error_msg)

        # proceed if no errors
        if error is False:
            newItem = RaceItem(name=request.form['race_add_name'],
                               race_cat_id=request.form['race_add_racecat'],
                               race_website=request.form['race_add_race_web'],
                               description=request.form['race_add_desc'],
                               utmb_points=request.form['race_add_utmbpoints'],
                               wser_qualifier=request.form['race_add_wser'],
                               month_id=request.form['race_add_month'],
                               state_id=request.form['race_add_state'],
                               user_id=login_session['user_id'])
            session.add(newItem)
            session.commit()
            return redirect(url_for('RaceCatList',
                            race_cat_id=request.form['race_add_racecat']))
    else:
        return render_template('race_add.html', months=months, states=states,
                               racecats=racecats)


# edit race
@app.route('/race/edit/<int:race_id>', methods=['GET', 'POST'])
def editRacePage(race_id):
    race = session.query(RaceItem).filter_by(id=race_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != race.user_id:
        return redirect(url_for('RacePage', race_id=race_id,
                        error="edit_error"))
    if request.method == 'POST':
        error = False

        # make sure that the race has a name
        if request.form['race_edit_name'] == "":
            error = True
            error_msg = "You must enter a race name"
            return render_template('race_edit.html', months=months,
                                   states=states, racecats=racecats,
                                   race=race, error_msg=error_msg)

        # make sure that this name hasnt already been used by another race ID
        name_check = request.form['race_edit_name']
        race_names = session.query(RaceItem).\
            filter_by(name=name_check).all()
        for race_name in race_names:

            # error if race name is in use, but by another race ID
            if race_name.name == name_check and race_name.id != race_id:
                error = False
                error_msg = "There is already a race with this name"
                return render_template('race_edit.html', months=months,
                                       states=states, racecats=racecats,
                                       race=race, error_msg=error_msg)

        # proceed if no errors
        if error is False:
            editRace = session.query(RaceItem).filter_by(id=race_id).one()
            editRace.name = request.form['race_edit_name']
            editRace.race_cat_id = request.form['race_edit_racecat']
            editRace.race_website = request.form['race_edit_race_web']
            editRace.description = request.form['race_edit_desc']
            editRace.utmb_points = request.form['race_edit_utmbpoints']
            editRace.wser_qualifier = request.form['race_edit_wser']
            editRace.month_id = request.form['race_edit_month']
            editRace.state_id = request.form['race_edit_state']
            session.add(editRace)
            session.commit()
            return redirect(url_for('RacePage', race_id=race_id))
    else:
        return render_template('race_edit.html', months=months,
                               states=states, racecats=racecats, race=race)


# delete race
@app.route('/race/delete/<int:race_id>', methods=['GET', 'POST'])
def deleteRacePage(race_id):
    race = session.query(RaceItem).filter_by(id=race_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if login_session['user_id'] != race.user_id:
        return redirect(url_for('RaceCatList', race_cat_id=race.race_cat_id,
                        error="delete_error"))
    if request.method == 'POST':
        deleteRace = session.query(RaceItem).filter_by(id=race_id).one()
        session.delete(deleteRace)
        session.commit()
        return redirect(url_for('RaceCatList', race_cat_id=race.race_cat_id))
    else:
        return render_template('race_delete.html', months=months,
                               states=states, racecats=racecats, race=race)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run()
