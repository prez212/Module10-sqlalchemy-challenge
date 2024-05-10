# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# last 12 month variable
prev_year_date = '2016-08-23'

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to Module 10 Climate App<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipatation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

#Define route to retrieve stations
@app.route ("/api/v1.0/precipitation")
def precipitation():
    #Calculate the date  12 months from today
    todays_past = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #Queary to retrieve the last 365 days of precipitation data
    precipitation_data = session.query(Measurement.date, Measurement.prep).\
                        filter(Measurement.date >= todays_past).all()
    
    #Convert the query results into a dictionary
    precip_dict = {date: prep for date, prep in precipitation_data}

    return jsonify (precip_dict)

#Define route to retrieve stations
@app.route("/api/v1.0/stations")
def stations():
    #Query to retrieve stations
    stations = session.query(Station.station, Station.name).all()

    #Convert the query results into dictionary
    stat_dict = [{"station":station, "name":name} for station, name in stations]

    return jsonify(stat_dict)


# Return a JSON list of Temperature Observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    tobstobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.date >= prev_year_date).all()
    return jsonify(tobstobs)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<date>")
def only_start(date):
    date_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(date_temp)



# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/temp/start/end")
def start_end(start,end):
    temp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(temp_results)

if __name__ == "__main__":
    app.run(debug=True)