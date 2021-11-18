import numpy as np

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

#################################################
# Database Setup
#################################################


engine =create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect and existing database
Base = automap_base()
#Refelct the tables
Base.prepare(engine, reflect=True)

#Save the refrences to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
most_recent_date = ""

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def index():

    return (
        f"<h3> Available Routes for the Climate App</h3> <br>"
        
        f"<ul> <li> /api/v1.0/precipitation </li><br>"
        f"<li>/api/v1.0/stations</li> <br>"
        f"<li>/api/v1.0/tobs </li><br>"
        f"<li>/api/v1.0/start_temp</li> <br>"
        f"<li>/api/v1.0/start_temp/end_temp</li></ul> <br>"
    )

#################################################
# Flask Route to diplay the precepitation by date
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    #Get the most recent date
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    # Calculate the date one year from the last date in data set.
    #most_recent_date = dt.datetime.strptime(most_recent_date, '%y-%m-%d')
    query_dt = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precep_data = session.query(Measurement.prcp, Measurement.date).\
                filter(Measurement.date > query_dt).\
                order_by(Measurement.date.desc())

    session.close()

    #convert the results to a dictionary
    prcp_dict = {}
    for prcp, date in precep_data:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)
    stations  = session.query(Station.station).all()
    session.close()
    #convert list of tuples into normal list
    result = list(np.ravel(stations))
    return jsonify(result)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    count_ = func.count('*').label('count_rec')
    active_station = session.query(count_, Measurement.station).\
        filter(Measurement.station == Station.station).\
        group_by(Measurement.station).order_by(count_.desc()).first()

    most_active_station = active_station.station
    
    temperature_data = session.query( Measurement.tobs).\
                    filter(Measurement.station == most_active_station).\
                    filter(Measurement.date > most_recent_date).all()
    result = list(np.ravel(temperature_data))
    session.close()
    return jsonify(result)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)
    sel = [func.min(Measurement.tobs), func.min(Measurement.tobs)]
    session.query()
    session.close()
    return

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start,end):
    session = Session(engine)
    session.query()
    session.close()
    return



if __name__ == "__main__":
    app.run(debug=True)

