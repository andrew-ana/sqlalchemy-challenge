import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dict of all precipitation data"""
    # Query all precipitation data
    results = dict(session.query(measurement.date, measurement.prcp).all())

    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all precipitation data
    results = session.query(station.name).group_by(station.name).all()

    result_list = list(np.ravel(results))

    session.close()
    
    return jsonify(result_list)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return most active station"""
    most_active_station = session.query(measurement.station, func.count(measurement.station)) \
        .group_by(measurement.station) \
        .order_by(func.count(measurement.station).desc()) \
        .all()[0]
    
    """Return a list of all tobs data from most active"""
    results = list(np.ravel(session.query(measurement.tobs).filter(measurement.station==most_active_station).all()))
    
    session.close()
    
    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)