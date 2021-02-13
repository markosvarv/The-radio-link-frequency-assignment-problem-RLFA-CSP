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
