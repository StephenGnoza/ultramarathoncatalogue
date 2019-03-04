# Project 2 - catalogue

This website creates a catalogue for US Ultra marathons.  Users are authenticated by Google.  Registered users may add a race to a fixed set of categories and provide some information about those races.

# Program design

The website is built using Python and a SQL database.

# How to Run the program

First, register a project on Google Cloud and create a client_secrets.json file.  Upload this to the project root.  Be sure to follow all instructions for setting up OATH2 on Google Cloud.

Second, run database_setup.py to create the SQL database.

```sh
python database.py
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

# Author

Stephen Gnoza
stephen.gnoza@gmail.com
