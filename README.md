# Minimum Vertex Cover

The Minimum Vertex cover (MVC) problem is a well known NP-complete problem with numerous applications. 
This project solve the problem uses four different algorithms including Branch-and-Bound, Approximation, FastVC, Simulated Annealing and evaluates their theoretical and experimental complexities on real world datasets.

# Prerequisites and Dependencies
You will need the following packages to run the code. To install the packages used in this project, run the following command.
```
$ pip install networkx
$ pip install deap
```
Our code is based on python version 3.7

# Running the code

To test and run this code, you will need the following:
```
python -inst <filename> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
```
or a script
```
$ ./exec.sh
```

# Directory layout

    .
    ├── code                   # Algorithms
    └── output                 # Solution & Solution trace files:
