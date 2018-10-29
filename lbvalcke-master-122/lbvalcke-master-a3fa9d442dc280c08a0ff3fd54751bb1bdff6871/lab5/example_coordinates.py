import coordinates

if __name__ == "__main__":
    # We create two Coordinates objects, one representing the
    # location of Chicago, and one representing the location
    # of New York
    cChicago = coordinates.Coordinates( 41.8337329, -87.7321555)
    cNewYork = coordinates.Coordinates( 40.7056308, -73.9780035)

    # We print out the coordinates
    print("The coordinates of Chicago are " + str(cChicago))
    print("The coordinates of New York are " + str(cNewYork))
        
    # We compute the distance between them
    distance = cChicago.distance_to(cNewYork)
        
    # Note that we could have also done the following:
    #
    #  distance = cNewYork.distance_to(cChicago)
        
    # We print the distance
    s = "The distance between Chicago and New York is {:.2f}km"
    print(s.format(distance/1000.0))
