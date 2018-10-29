from math import sin

def is_power_of_two(n):
    # replace the pass statement with your code
    if n == 1:
      return True
    elif n % 2 == 0: 
      return is_power_of_two(n / 2)
    else: 
      return False


def fib(n):
    # replace the pass statement with your code
    if n == 0 or n == 1:
        return 1
    elif n >= 2: 
      return fib(n - 1) + fib(n - 2)

def find_root_sqrt2(epsilon, a, b):
    # replace the pass statement with your code
    start_pt = (a) ** 2 - 2
    end_pt = (b) ** 2 - 2
    if start_pt < epsilon and start_pt > -1 * epsilon:
      return start_pt
    elif end_pt < epsilon and end_pt > -1 * epsilon:
      return end_pt 
    elif start_pt <= 0 and end_pt >= 0: 
      c = (a + b) / 2
      mid_pt = c ** 2 - 2
      if mid_pt < epsilon and mid_pt > -1 * epsilon:
          return c
      elif start_pt < 0 and mid_pt > 0:
          return find_root_sqrt2(epsilon, a, c)
      elif mid_pt < 0 and end_pt > 0: 
          return find_root_sqrt2(epsilon, c, b)
    else:   
        print("Invalid Inputs")

def find_root(func, epsilon, a, b):
    # replace the pass statement with your code
    start_pt = func(a)
    end_pt = func(b)
    if start_pt < epsilon and start_pt > -1 * epsilon:
      return start_pt
    elif end_pt < epsilon and end_pt > -1 * epsilon:
      return end_pt 
    elif start_pt <= 0 and end_pt >= 0: 
      c = (a + b) / 2
      mid_pt = func(c)
      if mid_pt < epsilon and mid_pt > -1 * epsilon:
          return c
      elif start_pt < 0 and mid_pt > 0:
          return find_root(func, epsilon, a, c)
      elif mid_pt < 0 and end_pt > 0: 
          return find_root(func, epsilon, c, b)
    else:   
        print("Invalid Inputs")

def sinpoint5(x):
    return sin(x) - 0.5

def root2(x): 
    return x ** 2 - 2 


t0 = {"key":"node0",
      "val":27,
      "children":[]}

t1 = {"key":"node0",
      "val":1,
      "children":[{"key":"node0",
                   "val":2,
                   "children":[{"key":"node0",
                                "val":3,
                                "children":[]}]},
                  {"key":"node0",
                   "val":4,
                   "children":[]},
                  {"key":"node0",
                   "val":5,
                   "children":[]}]}


def count_leaves(t):
    '''
    Count the number of leaves in the tree rooted at t
    
    Inputs: (dictionary) a tree
    
    Returns: (integer) number of leaves in t
    '''
    assert t is not None

    if not t["children"]:
        return 1

    num_leaves = 0
    for kid in t["children"]:
        num_leaves += count_leaves(kid)

    return num_leaves


def add_values(t):
    # replace the pass statement with your code
    assert t is not None

    if not t["children"]:
        return t["val"]

    values = 0
    values += t["val"]
    for kid in t["children"]:
        values += add_values(kid)

    return values    
