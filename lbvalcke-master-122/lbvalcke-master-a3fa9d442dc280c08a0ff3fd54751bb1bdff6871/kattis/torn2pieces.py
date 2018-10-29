import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/torn2pieces
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.


def solve(pieces, start, end):
    """
    Parameters:
     - pieces: List of lists of strings. Each list of strings represents a 
               piece of the map. For example, [["A","B"],["B","A","D"]] 
               represents two pieces, one for station "A" (which is connected
               to "B") and one for station "B" (which is connected to "A" and "D")
     - start, end: A starting and ending station.

    Returns: List of strings, or None.
             If a route exists between the starting and ending station, return
             a list with the stations in that route.
             If no such route exists, return None.
    """

    # Your code here.
    def create_dict(pieces):
        subway_dict = {}
        for piece in pieces:
            subway_dict[piece[0]] = piece[1:]

        orig_keys = subway_dict.keys()
        missing_connect = []
        complete_dict = dict(subway_dict)
        
        for key in subway_dict.keys():
            for connection in subway_dict[key]:
                if connection not in subway_dict.keys() and connection not in missing_connect:
                    complete_dict[connection] = []
                    missing_connect.append(connection)
        
        for connection in missing_connect:
            for key in orig_keys:
                if connection in subway_dict[key]:
                    complete_dict[connection].append(key)
        return complete_dict

    def options(start, end, past, attempts, subway_dict):
        if start in subway_dict.keys():
            for option in subway_dict[start]:
                past.append(option)
                if option not in attempts and option != end and end not in past:
                    attempts.append(option)
                    options(option, end, past, attempts, subway_dict)
                if option == end and end not in past:
                    past.append(option)
                    return past
                if end in past:
                    return past
                past.pop()
        else: 
            return None
    
    subway_dict = create_dict(pieces)
    past = [start]
    attempts = [start]

    past = options(start, end, past, attempts, subway_dict)
    # Replace "None" with a suitable return value.
    return past


### The following code handles the input and output tasks for
### this problem.  Do not modify it!

if __name__ == "__main__":
    npieces = int(sys.stdin.readline())

    pieces = []
    for i in range(npieces):
        piece = sys.stdin.readline().strip().split()
        pieces.append(piece)

    start, end = sys.stdin.readline().strip().split()

    route = solve(pieces, start, end)
    if route is None:
        print("no route found")
    else:
        print(" ".join(route))

