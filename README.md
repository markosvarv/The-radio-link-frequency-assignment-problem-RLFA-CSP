# Artificial Intelligence RLFA CSP

### Markos Varvagiannis

### sdi1400017@di.uoa.gr

In this project I solve the RLFA CSP (Radio Link Frequency Assignment Constraint Satisfaction Problem) using the algorithms FC, MAC and FC-CBJ with a conflict-directed heuristic for variable ordering.

## Algorithms

- **Backtracking using Forward Checking (FC) and Maintain Arc Consistency (MAC)**: 
  These algorithms are implemented and used from the AIMA code. https://github.com/aimacode/aima-python/blob/master/csp.py
- **The dom/wdeg heuristic**
  It's a conflict-directed **variable ordering** heuristic: "Ιt avoids some trashing by first instantiating variables involved in the constraints that have frequently participated in dead-end situations. Such information is recorded by associating a weight with each constraint." More info in the following paper: http://www.frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf .
- **Forward Checking Conflict-directed Backjumping (FC-CBJ)**: This algorithm *jumps* to the variable that *caused the conflict* and not simply to the most (chronologically) recent variable. That reduces the time for difficult problems, as we will see below. When combined with Forward Checking especially, we have a very fast algorithm for large datasets. I use the below data structures:
  - **conflict_set**: it's a dictionary of sets that represents the conflict set of every variable of the problem, i.e. conflict_set[variableA] = {variableC, variableJ, variableL}
  - **checking**: it's a dictionary of sets that represents the checking set of every variable of the problem, meaning the variables whose values the Forward Checking wiped out from the domains. I use that sets in order to find the conflict set of every variable.


## RLFA

### Execution:
```
python rlfa.py
```

### Data structures: Dictionaries

- the **variables_dict** assigns domain numbers to variables, i.e. variables_dict[variable] = #domain
- the **domains_dict** assigns lists of variables to domain numbers, i.e. domains_dict[#domain] = [value1, value2, ..., valueN]
- the **variables_domain_dict** merges the previous two dictionaries and assigns a list of the exact domain values to variables, i.e. variables_domain_dict[variable] = [value1, value2, ..., valueN]
- the **neighbors_dict** assigns the neighbor variable of each variable in the constraints, i.e. neighbors_dict[variableA] = variableB
- the **constraints_dict** assigns the compare operator and the k constant to a tuple of variables, i.e. constraints_dict[(variableA, variableB)] = (\<operator>, k) where \<operator> is either '>' or '='

### Design options
- I assume that for every pair of variables (variableA, variableB) there is only one constraint. Otherwise, only the last constraint remains and a corresponding message informs the user.
- I have modified some AIMA algorithms in order to use them with dom/wdeg or cbj. These functions' names have a prefix of the corresponding algorithm.
- I have modified the min-conflicts algorithm, so that the variables are in a random order for every execution.

## Results


### Instance: 2-f24 (SAT)
| Algorithm (2-f24)   | Time     | Assigns number | Number of constraint checks |
|---------------------|----------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 0.05 sec | 207            | 19,561                      |
| BT + MAC + dom/wdeg | 0.17 sec | 200            | 163,547                     |
| CBJ + dom/wdeg      | 5.24 sec | 43095          | 580,721                     |
| FC-CBJ              | 0.38 sec | 6120           | 306,577                     |
| FC-CBJ + dom/wdeg   | 0.06 sec | 207            | 19,561                      |

### Instance: 2-f25 (UNSAT)
| Algorithm (2-f25)   | Time           | Assigns number | Number of constraint checks |
|---------------------|----------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 50.4 sec       | 50.4 sec       | 24,293,135                  |
| BT + MAC + dom/wdeg | 98.09 sec      | 32938          | 67,111,862                  |
| CBJ + dom/wdeg      | Timeout(>15min)| -              | -                           |
| FC-CBJ              | 116.5 sec      | 1765713        | 104,391,258                 |
| FC-CBJ + dom/wdeg   | 1.03 sec       | 2963           | 513,591                     |

The heuristic dom/wdeg was found essential, because, using the default variable ordering, the time was incredibly high (in most instances, the algorithm didn't even stop).


### Instance: 3-f10 (SAT)
| Algorithm (3-f10)   | Time      | Assigns number | Number of constraint checks |
|---------------------|-----------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 10.34 sec | 49377          | 5,583,778                   |
| BT + MAC + dom/wdeg | 1.64 sec  | 770            | 1,209,727                   |
| FC-CBJ + dom/wdeg   | 5.24 sec  | 21540          | 2,554,805                   |

### Instance: 3-f11 (UNSAT)

| Algorithm (3-f11)   | Time           | Assigns number | Number of constraint checks |
|---------------------|----------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 1080,03 sec    | 5965372        | 851,057,936                 |
| BT + MAC + dom/wdeg | 121.49 sec     | 22929          | 101,292,941                 |
| FC-CBJ + dom/wdeg   | 86.26 sec      | 309014         | 54,123,606                  |


### Instance: 7-w1-f5 (UNSAT)
| Algorithm (7-w1-f5) | Time             | Assigns number | Number of constraint checks |
|---------------------|------------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | Timeout(>15min)  | -              | -                           |
| BT + MAC + dom/wdeg | 31.45 sec        | 11683          | 47,767,900                  |
| FC-CBJ + dom/wdeg   | 0.62 sec         | 3608           | 245,557                     |

### Instance: 8-f10 (SAT)

| Algorithm (8-f10)   | Time             | Assigns number | Number of constraint checks |
|---------------------|------------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | Timeout(>15min)  | -              | -                           |
| BT + MAC + dom/wdeg | 58.8 sec         | 16759          | 29,534,016                  |
| FC-CBJ + dom/wdeg   | 25.15 sec        | 44901          | 6,091,607                   |

The BT + FC + dom/wdeg is very slow and it isn't effective in large datasets, or when the problem is UNSAT.

### Instance: 14-f27 (SAT)
| Algorithm (14-f27)  | Time             | Assigns number | Number of constraint checks |
|---------------------|------------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | Timeout( >15min) | -              | -                           |
| BT + MAC + dom/wdeg | 1433,74 sec      | 7461123        | 150,811,431                 |
| FC-CBJ + dom/wdeg   | 12.19 sec        | 14460          | 844,552                     |

The BT + MAC + dom/wdeg seems inadequate in the last large SAT instance.

### Min conflicts - Instance: 2-f24 (SAT)
| Max steps | SAT/UNSAT | Time       | Assigns number | Number of constraint checks |
|-----------|-----------|------------|----------------|-----------------------------|
| 50000     | UNSAT     | 102.4 sec  | 50200          | 139,593,786                 |
| 100000    | UNSAT     | 219.2 sec  | 100200         | 293,264,824                 |
| 100000    | UNSAT     | 212.3 sec  | 100200         | 285,221,656                 |
| 200000    | UNSAT     | 414.21 sec | 200200         | 597,276,944                 |

The min conflicts algorithm seems that it hasn't got a solution for even the smallest instance! (the results were similar for the other instances). The reason is that the solutions are not densely distributed in the state space and that we don't use a heuristic for variable ordering - we just use a random ordering that may cause a lot of conflicts if the initial assignment isn't good.

## Conclusion 
Consequently, using the FC-CBJ we have a result for every given instance of the problem in a logical time period. The backtracking algorithm using the dom/wdeg heuristic (preferably the MAC instead of FC) helps us in small instances and mostly in SAT problems. So, the best algorithm for the RLFA CSP is the FC-CBJ with the dom/wdeg heuristic for variable ordering.






