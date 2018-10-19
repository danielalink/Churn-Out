import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify, render_template, request
import csv


# Create App
app = Flask(__name__)

# Connect to sqlite database
engine = create_engine("sqlite:///dataset/telemarker_db.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)


# Storing tables# Storing tables
Telemarker_db = Base.classes.telemarker_db
# Samples = Base.classes.samples
# Samples_Metadata = Base.classes.samples_metadata

# Returns the dashboard homepage
@app.route("/")
def home():
    return render_template("index.html")

# Returns a list of customer_ids in list format
@app.route("/customer_ids")
def customer_ids():

    # Empty list for sample ids
    customer_ids = []
    
    # Grab metadata table
    results = session.query(Telemarker_db.customerID)

    # Loop through query & grab ids
    for result in results:
        customer_ids.append(str(result[0]))

    return jsonify(customer_ids)


