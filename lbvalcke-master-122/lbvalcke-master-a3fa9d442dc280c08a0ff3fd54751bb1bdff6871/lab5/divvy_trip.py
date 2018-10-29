class DivvyTrip(object): 

    '''
    There are two types of Divvy users: Customers and Subscribers.
    Customer" is a rider who purchased a 24-Hour Pass; 
    Subscriber" is a rider who purchased an Annual Membership.
    Subscriber trips include additional information, like year of birth, etc. 
    '''

    def __init__(self, trip_id, starttime, stoptime, bikeid,
                 tripduration, from_station, to_station, 
                 usertype, gender, birthyear):
        '''
        Constructor
        '''
        self.trip_id = trip_id
        self.starttime = starttime
        self.stoptime = stoptime
        self.bikeid = bikeid
        self.tripduration = tripduration
        self.from_station = from_station
        self.to_station = to_station
        self.usertype = usertype
        self.gender = gender
        self.birthyear = birthyear
    

    def get_trip_duration(self):
        return self.tripduration
    
    
    def get_distance(self):
        # Your code here
        # Replace 0.0 with an appropriate return value
        return 0.0
    


