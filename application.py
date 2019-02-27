from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)

@app.route('/')
def HelloWorld():
    return render_template('distances.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
