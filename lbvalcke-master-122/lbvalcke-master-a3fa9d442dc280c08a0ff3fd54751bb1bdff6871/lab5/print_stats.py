import sys
import divvy_data

def go(station_filename, trip_filename):
    '''
    Print some statistics about the Divvy files.
    '''
    data = divvy_data.DivvyData(station_filename, trip_filename)

    # Number of stations and trips
    print("# of stations: " + str(data.get_number_stations()))
    print("# of trips: " + str(data.get_number_trips()))

    print();
        
    # Average duration of trip
    print("The total duration of a Divvy trip in 2013 was {:f}s".format(data.get_total_duration()))

    print("The average duration of a Divvy trip in 2013 was " + 
          str(data.get_total_duration() / data.get_number_trips()) + "s.");

    print();

    # Total and average distance
    s ="The total distance travelled by all the Divvy bikes in 2013 was {:f} km."
    print(s.format(data.get_total_distance()/1000.0))

    s = "The average distance travelled in a single trip in 2013 was {:f} m."
    print(s.format(data.get_total_distance()/data.get_number_trips()))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        station_filename = sys.argv[1]
        trip_filename = sys.argv[2]
    else:
        print("usage: python {} <stationFile> <tripFile>".format(sys.argv[0]))
        sys.exit(0)

    go(station_filename, trip_filename)
