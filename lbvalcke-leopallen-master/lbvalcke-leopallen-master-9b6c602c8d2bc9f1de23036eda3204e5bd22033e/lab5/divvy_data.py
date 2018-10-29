import coordinates
import csv
import divvy_station
import divvy_trip
import sys
import time

class DivvyData(object):
    def __init__(self, station_filename, trip_filename):
        '''
        Constructor.
        Input: path to station file and path to trip file
        '''

        self.stations = self.read_stations_file(station_filename)
        self.trips = self.read_trips_file(trip_filename)


    def read_single_station(self, row):
        '''
        Create a DivvyStation object based on a line 
        from the stations CSV file
        '''

        if len(row) < 7:
            print("Error in parsing line: " + ",".join(row))
            return None

        try:
            station_id = int(row[0])
            name = row[1]

            latitude = float(row[2])
            longitude = float(row[3])

            coords = coordinates.Coordinates(latitude, longitude)

            dpcapacity = int(row[4])
            landmark = int(row[5])

            date = time.strptime(row[6], "%m/%d/%Y")
        except Exception as e:
            print("Error in parsing data: " + str(e))
            return None

        return divvy_station.DivvyStation(station_id, name, coords, dpcapacity, landmark, date)


    def read_stations_file(self, filename):
        '''
        Parse a Divvy stations file.

        Input: path to station file

        Result: 
            dictionary that maps station identifiers to DivvyStation
            objects
        '''
        stations = {}
        with open(filename) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                station = self.read_single_station(row)
                if station == None: 
                    print("Error reading station: " + ",".join(row))
                    sys.exit(0)
                else:
                    stations[station.get_ID()] = station

        return stations


    def read_single_trip(self, row):
        '''
        Create a DivvyTrip object based on a row
        from the trips CSV file
        '''

        try:
            trip_id = int(row[0])

            starttime = time.strptime(row[1], "%Y-%m-%d %H:%M")
            endtime = time.strptime(row[2], "%Y-%m-%d %H:%M")

            bikeid = int(row[3])
            tripduration = int(row[4])

            station_id = int(row[5])
            if station_id not in self.stations:
                print("Encountered unknown station: " + str(station_id))
                return None
            from_station = self.stations[station_id]
            # Skip the station name (row[6]). We do not use it.

            station_id = int(row[7])
            if station_id not in self.stations:
                print("Encountered unknown station: " + str(station_id))
                return None
            to_station = self.stations[station_id]
            # Skip the station name (row[8]). We do not use it.

            usertype = row[9]
            gender = None
            birthyear = 0

            if usertype == "Subscriber":
                gender = row[10]
                if gender != "" and gender != "Male" and gender != "Female":
                    print("Encountered unknown gender: " + gender)
                    return None

                if len(row[11]) > 0:
                    birthyear = int(row[11])
        except Exception as e:
            print("Error in parsing data: " + str(e))
            return None

        return divvy_trip.DivvyTrip(trip_id, starttime, endtime, bikeid, tripduration, from_station, to_station, usertype, gender, birthyear)


    def read_trips_file(self, filename):
        '''
        Parse a Divvy trips file.

        Input:  path to  trip data file
        
        Result:
            list of DivvyTrip objects
        '''
        trips = []
        with open(filename) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                trip = self.read_single_trip(row)
                if trip == None: 
                    print("Error reading trip: " + ",".join(row))
                    sys.exit(0)
                else:
                    trips.append(trip)

        return trips


    def get_number_stations(self):
        return len(self.stations)
    

    def get_number_trips(self):
        return len(self.trips)
    

    def get_total_distance(self):
        '''
        Computes the total distance of all the Divvy trips
        '''
        # Your code here 
        # Replace the 0.0 with an appropriate return value
        return 0.0


    def get_total_duration(self):
        '''
        Computes the total duration, in seconds, of all the
        Divvy trips        
        '''
        # YOUR CODE HERE
        # Replace the 0.0 with an appropriate return value
        return 0.0
