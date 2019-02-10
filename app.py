from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcptn = {
        'date' : prcp
        for date, prcp in precipitation
    } 
    return jsonify(prcptn)


@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    all_stations = list(np.ravel(station_list))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def temperature():
    yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperatures = session.query(Measurement.tobs).\
    filter(Measurement.date >= yr_ago).all()
    all_temperatures_yrago = list(np.ravel(temperatures))
    return jsonify(all_temperatures_yrago)

if __name__ == '__main__':
    app.run(debug=True)
