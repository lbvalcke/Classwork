class DivvyStation(object):

    def __init__(self, stationID, name, coords,
                 dpcapacity, landmark, online_date):
        '''
        Constructor
        '''
        self.stationID = stationID
        self.name = name
        self.coords= coords

        # Number of total docks at each station as of 2/7/2014
        self.dpcapacity = dpcapacity

        # Undocumented attribute
        self.landmark = landmark

        # Date the station went live in the system
        self.online_date = online_date

    def get_ID(self):
        return self.stationID
