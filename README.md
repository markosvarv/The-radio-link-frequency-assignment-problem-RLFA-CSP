# Artificial Intelligence RLFA CSP

### Markos Varvagiannis

### sdi1400017@di.uoa.gr


This project is a RLFA CSP (Radio Link Frequency Assignment Problem CSP) using algorithms FC, MAC and FC-CBJ.

## Data structures - dictionaries

- the **variables_dict** assigns domain numbers to variables, i.e. variables_dict[variable] = #domain
- the **domains_dict** assigns lists of variables to domain numbers, i.e. domains_dict[#domain] = [value1, value2, ..., valueN]
- the **variables_domain_dict** merges the previous two dictionaries and assigns a list of the exact domain values to variables, i.e. variables_domain_dict[variable] = [value1, value2, ..., valueN]
- the **neighbors_dict** assigns the neighbor variable of each variable in the constraints, i.e. neighbors_dict[variableA] = variableB
- the **constraints_dict** assighs the compare operator and the k constant to a tuple of variables, i.e. constraints_dict[(variableA, variableB)] = (\<operator>, k) where \<operator> is either '>' or '='

## Design options
- We assume that for every pair of variables (variableA, variableB) there is only one constraint. Otherwise, only the last constraint remains and a corresponding message informs the user.

## Results

Notes: 


### Instance: 2-f24 (SAT)
| Algorithm (2-f24)   | Time     | Assigns number | Number of constraint checks |
|---------------------|----------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 0.05 sec | 207            | 19,561                      |
| BT + MAC + dom/wdeg | 0.17 sec | 200            | 163,547                     |
| CBJ + dom/wdeg      | 5.24 sec | 43095          | 580,721                     |
| FC-CBJ              | 0.38 sec | 6120           | 306,577                     |
| FC-CBJ + dom/wdeg   | 0.06 sec | 207            | 19,561                      |

### Instance: 3-f25 (UNSAT)
| Algorithm (2-f25)   | Time      | Assigns number | Number of constraint checks |
|---------------------|-----------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 34.12 sec | 49377          | 5,583,778                   |
| BT + MAC + dom/wdeg | 5.57 sec  | 826            | 1,218,585                   |
| CBJ + dom/wdeg      | Timeout   | -              | -                           |
| FC-CBJ              | 116.5 sec | 1765713        | 104,391,258                 |
| FC-CBJ + dom/wdeg   | 1.03 sec  | 2963           | 513,591                     |

The heuristic dom/wdeg was found essential, because, using the default variable ordering, the time were incredibly high (in the most instances, the algorithm didn't even stop).


### Instance: 3-f10 (SAT)
| Algorithm (3-f10)   | Time      | Assigns number | Number of constraint checks |
|---------------------|-----------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | 10.34 sec | 49377          | 5,583,778                   |
| BT + MAC + dom/wdeg | 1.64 sec  | 770            | 1,209,727                   |
| FC-CBJ + dom/wdeg   | 5.24 sec  | 21540          | 2,554,805                   |

### Instance: 3-f11 (UNSAT)

| Algorithm (3-f11)   | Time       | Assigns number | Number of constraint checks |
|---------------------|------------|----------------|-----------------------------|
| BT + FC + dom/wdeg  | Timeout    | -              | -                           |
| BT + MAC + dom/wdeg | 121.49 sec | 22929          | 101,292,941                 |
| FC-CBJ + dom/wdeg   | 86.26 sec  | 309014         | 54,123,606                  |

We notice that the BT + MAC + dom/wdeg is generally faster in SAT problems. However, the backjumping algorithm helps us more in the unsatisfiable problems, because it determinates faster that the problem has not a solution. The BT + FC + dom/wdeg is very slow and it isn't effective in either circumstances.

### Instance: 14-f27 (SAT)


### Instance: 14-f28 (UNSAT)





