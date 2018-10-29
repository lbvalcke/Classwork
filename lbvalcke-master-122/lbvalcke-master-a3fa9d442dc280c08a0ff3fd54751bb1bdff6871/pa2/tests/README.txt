CS 121: Schelling's Model of Housing Segregation

The grid file format is simple. The first line contains the grid
size. Each subsequent line contains information for a single row,
starting with row 0. A "B" means that the corresponding location has a
blue homeowner, an "R" means that the corresponding location has a red
homeowner, and an "O" means that the location is open.  See the file
``tests/sample-grid.txt``, which contains the initial grid from the 
example discussed in the programming assignment.

grid-lone-blue-sea-of-red.txt: A grid in which all the homes are occupied
by red homeowners, except one open home and one home occupied by a
blue homeowner.

grid-no-neighbors.txt: A sparsely populated grid

Examples that use the sample grid from the assignment description:

  sample-grid.txt: original state

  sample-grid-1-51-0-final.txt: result of running simulation with threshold of 51
    and zero steps.

  sample-grid-1-49-2-final.txt: result of running simulation with a threshold of 49

  Files for step 1 in sample simulation in assignment description: (R-1 neighborhood with 0.51 threshold)
    sample-grid-1-51-1-init.txt: initial state at the start of step 1
    sample-grid-1-51-1-1.txt: after one move
    sample-grid-1-51-1-2.txt: after two moves
    sample-grid-1-51-1-3.txt: after three moves
    sample-grid-1-51-1-final.txt: state at the end of step 1 
      (same as sample-grid-1-51-1-3.txt)

  Files for step 2 in sample simulation in assignment description:
    (start from sample-grid-1-51-1-final.txt, if you wish to start your
     simulation at step 2.)
    sample-grid-1-51-2-init.txt: initial state at the start of step 2
      (same as sample-grid-1-51-1-3.txt)
    sample-grid-1-51-2-1.txt: after one move in step 2
    sample-grid-1-51-2-2.txt: after two moves in step 2
    sample-grid-1-51-2-final.txt: state at the end of step 2 
      (same as sample-grid-1-51-2-2.txt)

  Files for step 3 in sample simulation in assignment description:
    (start from sample-grid-1-51-2-final.txt, if you wish to start your
     simulation at step 3.)
    sample-grid-1-51-3-init.txt: initial state at the start of step 3
      (same as sample-grid-1-51-2-final.txt)
    sample-grid-1-51-3-1.txt: after one move in step 3
    sample-grid-1-51-3-2.txt: after two moves in step 3
    sample-grid-1-51-3-final.txt: state at the end of step 3
      (same as sample-grid-1-51-3-2.txt)

  File for step 4 in sample simulation in assignment description:
    sample-grid-1-51-4-init.txt: initial state at the start of step 3
    sample-grid-1-51-4-final.txt: state at the end of step 2 

  File for sample simulation with a maximum number of steps of 5.
    sample-grid-1-51-5-final.txt

  sample-grid-2-51-7-final.txt: Last step in a simulation of grid 4
    using an R-2 neighborhood, a threshold of 0.51, and up to 7 steps.
    
  sample-grid-3-51-5-final.txt: Last step in a simulation of grid 4 using an
    R-3 neighborhood and a threshold of 0.51.


Files for testing possible new location in homeowner's neighborhood:

  grid-lone-blue-sea-of-red-2.txt: Another grid in which all the homes
    are occupied by red homeowners, except one open home and one home
    occupied by a blue homeowner.

  grid-lone-blue-sea-of-red-2-1-40-2-final.txt: result of simulation
    with R of 1 and threshold of 0.40.  Homeowner does not move.


Large grid example:

  grid-150-40-40.txt: large grid initial state

  grid-150-40-40-3-51-100-final.txt: Result of simulation of R-3
    neighborhood w/ threshold of 0.51 and up to 100 steps.

