import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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
        .all()[0][0]
    
    """Return a list of all tobs data from most active"""
    results = list(np.ravel(session.query(measurement.tobs).filter(measurement.station==most_active_station).all()))
    
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start):
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return temps after date"""
    temps_after_start = session.query(func.min(measurement.tobs), 
                                      func.avg(measurement.tobs), 
                                      func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    
    results = list(np.ravel(temps_after_start))
                   
    """Return a list of all tobs data from most active"""
    
    session.close()
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return temps after date"""
    temps_between = session.query(func.min(measurement.tobs), 
                                      func.avg(measurement.tobs), 
                                      func.max(measurement.tobs)
                                     ).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    results = list(np.ravel(temps_between))
                   
    """Return a list of all tobs data from most active"""
    
    session.close()
    
    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)