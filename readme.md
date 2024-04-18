# Logistics Lab - Task 1

Definition: "Jump" refers to a movement between machines that carries no payload

## How to run / where to find stuff

`validations.py` reads all files beginning with "schedule" and prints score.  
All relevant python files to create schedules are in `tests/`.  
Library with useful helper functions can be imported within that folder using `from utils import lib`, support for pypy can be reached by swapping to `from utils import libpypy as lib`.  
`write_history.py` can be used to print a history generated by the given algorithms into the format required by `validations.py`. The format used by the algorithms is concerned by moves: `(vehicle_id, start_pos, end_pos, carrying)` in which carrying is 1 if the vehicle is currently carrying a payload and 0 if it is jumping.

## 1 Vehicle

`lower_bound_test.py` calculates a lower bound for solutions.  
`longest_first.py` implements greedy algorithm that evaluates heuristic for current point.  
`full_depth_first.py` implements depth first search in which children nodes are sorted by the same heuristic.  
`full_depth_first_threading.py` and `full_depth_first_mp.py` implement multithreading and multiprocessing of the depth first search, multithreading seems to be more performant.  
`start_with_first_jump.py` assumes that a path is optimal up until first jump, as it only contains actually needed movements. The path after can be optimized quicker using a depth first search as the recursion depth is much lower. The algorithm requires a previous solution to build upon, which is found using `full_depth_first_threading.py` in the current case.

### Current solution

`full_depth_first_threading.py` finds solution with score 16200.6507 after 115 seconds  
taking solution, put history into file  
`start_with_first_jump.py` refines solution to score 16156.79 after 172 seconds  

Best solution after 287 seconds ≙ 4 minutes 47 seconds  

### lower bound

first approach:  
only sum up all transport jobs, value: 15049.49

second approach:  
also calculate how many jumps are needed, value: 1107.19  
Needed jumps are found by seeing which machines have more outgoing transport demands than incoming demands and the other way around. This way the shortest possibility to connect all machines with more incoming demands to the machines with more outgoing demands can be found using a depth first search.  
added to first approach: 16156.68
