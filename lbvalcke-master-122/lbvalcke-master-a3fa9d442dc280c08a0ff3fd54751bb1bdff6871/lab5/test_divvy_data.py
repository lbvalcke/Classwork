import sys
import divvy_data

EPSILON=0.001

def helper(station_filename, trip_filename, expected_values):
    data = divvy_data.DivvyData(station_filename, trip_filename)

    assert(data.get_number_stations() == expected_values["num_stations"])
    assert(data.get_number_trips() == expected_values["num_trips"])

    assert(abs(data.get_total_duration() - expected_values["total_duration"]) < EPSILON)
    assert(abs(data.get_total_distance() - expected_values["total_distance"]) < EPSILON)

def test_0():
    ev = {"num_stations":300, 
          "num_trips":100, 
          "total_duration": 272307.00, 
          "total_distance":157653.091}
    helper("divvy_2013_stations.csv", "divvy_2013_trips_tiny.csv", ev)

def test_1():
    ev = {"num_stations":300, 
          "num_trips":10000, 
          "total_duration": 23812760.00,
          "total_distance":21089.453779*1000}
    helper("divvy_2013_stations.csv", "divvy_2013_trips_small.csv", ev)

def test_2():
    ev = {"num_stations":300, 
          "num_trips":50000, 
          "total_duration": 112128315.00,
          "total_distance":110524.789291*1000}
    helper("divvy_2013_stations.csv", "divvy_2013_trips_medium.csv", ev)
