import coordinates
import pytest

TOLERANCE = 10

def helper(c1, c2, expected):
    if expected > 1000.0:
        unit = "km"
        scale = 1000.0
    else:
        unit = "m"
        scale = 1.0

    d = c1.distance_to(c2)
    if abs(d-expected) >= TOLERANCE:
        s = "WRONG: Expected distance between {} and {} to be {:.2f} {} but got {:.2f} {}"
        pytest.fail(s.format(c1, c2, expected/scale, unit, d/scale, unit))


def test_1():
    cChicago =     coordinates.Coordinates( 41.8337329, -87.7321555)
    cNewYork =     coordinates.Coordinates( 40.7056308, -73.9780035)
    helper(cChicago, cNewYork, 1155076.772338)

def test_2():
    cChicago =     coordinates.Coordinates( 41.8337329, -87.7321555)
    cLondon =      coordinates.Coordinates( 51.5286416,  -0.1015987)
    helper(cChicago, cLondon,       6363076.446747)

def test_3():
    cChicago =     coordinates.Coordinates( 41.8337329, -87.7321555)
    cBuenosAires = coordinates.Coordinates(-34.6158527, -58.4332985)        
    helper(cChicago, cBuenosAires,  9010486.474634)

def test_4():
    cChicago =     coordinates.Coordinates( 41.8337329, -87.7321555)
    cSydney =      coordinates.Coordinates(-33.856898,  151.215281)
    helper(cChicago, cSydney,      14865550.217648)

def test_5():
    cChicago =     coordinates.Coordinates( 41.8337329, -87.7321555)
    cNairobi=      coordinates.Coordinates(-1.3048036,   36.8473969)
    helper(cChicago, cNairobi,     12895627.486686)

def test_6():
    cRegenstein = coordinates.Coordinates( 41.79218,   -87.599934)
    cRyerson =    coordinates.Coordinates( 41.7902836, -87.5991959)
    helper(cRegenstein, cRyerson,   219.569166)

def test_7():
    cRegenstein = coordinates.Coordinates( 41.79218,   -87.599934)
    cSnitchock =  coordinates.Coordinates( 41.791218,  -87.601026)
    helper(cRegenstein, cSnitchock, 140.136890)

def test_8():
    cRegenstein = coordinates.Coordinates( 41.79218,   -87.599934)
    cHarper    =  coordinates.Coordinates( 41.787965,  -87.599642)
    helper(cRegenstein, cHarper,    469.311408)

def test_9():
    cRyerson =    coordinates.Coordinates( 41.7902836, -87.5991959)
    cSnitchock =  coordinates.Coordinates( 41.791218,  -87.601026)
    helper(cRyerson,    cSnitchock, 183.890430)

def test_10():
    cRyerson =    coordinates.Coordinates( 41.7902836, -87.5991959)
    cHarper    =  coordinates.Coordinates( 41.787965,  -87.599642)
    helper(cRyerson,    cHarper,    260.455871)

def test_11():
    cSnitchock =  coordinates.Coordinates( 41.791218,  -87.601026)
    cHarper    =  coordinates.Coordinates( 41.787965,  -87.599642)        
    helper(cSnitchock,  cHarper,    379.480114)        


    


