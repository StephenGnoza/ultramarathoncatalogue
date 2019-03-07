# Project 2 - catalogue

## Overview
This website crates a catalogue for US Ultramarathons.  Functionality includes:
<ul>
<li>User accounts are created and authenticated via Google</li>
<li>Registered users may add a race to predetermined categories.</li>
<li>Registered users may edit their own races.</li>
<li>Registered users may delete their own races.</li>
<li>Races may be filtered by predetermined categories.</li>
<li>Race data may be accessed by a JSON API</li>
</ul>

## Installation


### Clone Repository
Clone this repo to your local machine using

```
https://github.com/stephengnoza/ultramarathoncatalogue
```

### Install Dependecies
You'll need to install Flask, sqlalchemy, and oauth2client.

```
pip install Flask
```

```
pip install sqlalchemy
```

```
pip install oauth2client
```

## Program design

The website is built using Python and a SQL database.

## How to Run the program

First, register a project on Google Cloud and follow all instructions for setting up OAuth 2.0 Client ID and configure the OAuth consent screen.  Download the clients_secret.json file to the root of the program.
(for Udacity review purposes, client_secrets.json included)

Second, run database_setup.py to create the SQL database.

```sh
python database_setup.py
```

Third, run db_initial_data.py to load the database with race distances and a list of US States.

```sh
python db_initial_data.py
```

Finally, to run the program itself, run application.py:

```sh
python application.py
```

and navigate to http://localhost:5000/ to visit the website.

## JSON API

List of all races:

```sh
http://localhost:5000/races/JSON
```

List of races within a category:

```sh
http://localhost:5000/racecat/<int:race_cat_id>/JSON
```

A particular race:

```sh
http://localhost:5000/race/<int:race_id>/JSON
```

## Author

Stephen Gnoza
stephen.gnoza@gmail.com
