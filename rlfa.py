from csp import *
import time

from collections import OrderedDict



# constraints_dict = {}
constraints_check_no = 0

def constraints(A, a, B, b):
    comp, k, weight = constraints_dict[(A, B)]

    # constraints_check_no += 1

    if comp == '>':
        return abs(a - b) > k
    elif comp == '=':
        return abs(a - b) == k
    else:
        raise ValueError("Wrong compare operator")


class RLFA(CSP):

    @staticmethod
    def get_variables_dict(variables_str):
        variables = {}
        variables_list = variables_str.splitlines()
        variables_number = int(variables_list.pop(0))
        for x in range(variables_number):
            current_line = variables_list[x].split()
            current_line = list(map(int, current_line))  # convert the string list to int list
            variables[current_line[0]] = current_line[1]
        return variables

    @staticmethod
    def get_domains_dict(domains_str):
        domains = {}
        domain_list = domains_str.splitlines()
        domains_number = int(domain_list.pop(0))
        for x in range(domains_number):
            current_line = domain_list[x].split()
            current_line = list(map(int, current_line))  # convert the string list to int list
            current_domain_number = current_line.pop(0)
            values_num = current_line.pop(0)
            if values_num != len(current_line):
                raise ValueError("Wrong values number input")
            domains[current_domain_number] = current_line
        return domains

    @staticmethod
    def get_constraint_list(containts_str):
        constraint_list = containts_str.splitlines()
        constraints_number = int(constraint_list.pop(0))
        if constraints_number != len(constraint_list):
            raise ValueError("Wrong lines input")

        splitted_constraints_list = []
        for node in constraint_list:
            # split the list into separate strings
            current_splitted_constraints_list = node.split()
            splitted_constraints_list.append(current_splitted_constraints_list)

        return splitted_constraints_list

    @staticmethod
    def assign_domains_to_variables(variables_dict, domains_dict):
        variables_domain_dict = {}
        for variable, domain in variables_dict.items():
            variables_domain_dict[variable] = domains_dict[domain]
        return variables_domain_dict

    @staticmethod
    def get_neighbors_dict(constraints_list):
        neighbors_dict = {}
        for current_list in constraints_list:
            x = int(current_list[0])
            y = int(current_list[1])

            # initialize the variables lists for the current key if it does not exist in the dict
            if x not in neighbors_dict:
                neighbors_dict[x] = []
            if y not in neighbors_dict:
                neighbors_dict[y] = []

            # assign the values
            if y not in neighbors_dict[x]:
                neighbors_dict[x].append(y)
            if x not in neighbors_dict[y]:
                neighbors_dict[y].append(x)

        return neighbors_dict

    @staticmethod
    def get_constraints_dict(constraints_list):
        constraints_dict = {}
        for current_list in constraints_list:
            x = int(current_list[0])
            y = int(current_list[1])
            comp = current_list[2]
            k = int(current_list[3])

            # assign the values
            if (x, y) in constraints_dict:
                print("More than one constraints for the same variables. Only the last one will remain.")
            if (y, x) in constraints_dict:
                print("More than one constraints for the same variables. Only the last one will remain.")

            constraints_dict[(x, y)] = (comp, k, 1)
            constraints_dict[(y, x)] = (comp, k, 1)

        return constraints_dict

    def increase_constraint_weight (self, A, B):
        comp, k, weight = constraints_dict[(A,B)]
        # print("weight = " + str(weight))
        constraints_dict[(A,B)] = (comp, k , weight+1)
        constraints_dict[(B,A)] = (comp, k , weight+1)


    def get_constraint_weight (self, A, B):
        comp, k, weight = constraints_dict[(A,B)]
        # print("weight = " + str(weight))
        return weight

    def get_list(self):
        return self.constraints_list


    def __init__(self, instance):
        domains_file = open("rlfap/dom" + instance + ".txt", "r")
        variables_file = open("rlfap/var" + instance + ".txt", "r")
        constraints_file = open("rlfap/ctr" + instance + ".txt", "r")

        domains_dict = self.get_domains_dict(domains_file.read())
        variables_dict = self.get_variables_dict(variables_file.read())
        self.constraints_list = self.get_constraint_list(constraints_file.read())

        variables_list = list(variables_dict.keys())
        variables_domain_dict = self.assign_domains_to_variables(variables_dict, domains_dict)

        neighbors_dict = self.get_neighbors_dict(self.constraints_list)
        self.constraints_check_no = 0

        CSP.__init__(self, variables_list, variables_domain_dict, neighbors_dict, constraints)


def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable

def domwdeg_dynamic_variable(assignment, csp):
    """The dom/wdeg heuristic variable order."""

    uninstantiated_vars_number = len(csp.variables) - len(assignment)
    print("uninstantiated_vars_number = " + str(uninstantiated_vars_number))
    if csp.curr_domains is not None:
        # print('THA EPISTREPSW TO HEURISTIC')

        # for domain_list in csp.domains:
        #     print(domain_list)

        min_mpourda = 999999
        return_var = 999999

        for myvar in csp.variables:

            # print(len(domain_list))

            if myvar not in assignment:
                domain_list = csp.curr_domains[myvar]
                # print("var = " + str(var) + ' domain list = ' + str(domain_list))

                dom = len(domain_list)
                wdeg = 1
                neighbors = csp.neighbors[myvar]
                # print('neighbors = ' + str(neighbors))
                for neighbor_var in neighbors:
                    # if k.get_constraint_weight(myvar, neighbor_var)!=1:
                        # print (k.get_constraint_weight(myvar, neighbor_var))
                    if neighbor_var not in assignment:
                        wdeg += k.get_constraint_weight(myvar, neighbor_var)
                # print('wdeg = ' + str(wdeg))
                #
                h = dom/wdeg

                if h < min_mpourda:
                    min_mpourda = h
                    return_var = myvar

        # print("return var = " + str(return_var) + " weight = " + str(min_mpourda))
        # print(constraints_dict)
        return return_var

    else:
        print('THA EPISTREPSW STIN TYXI')
        return first([var for var in csp.variables if var not in assignment])

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

def nconflicts(self, var, val, assignment, var_conflict_set):
    """Return the number of conflicts var=val has with other variables."""

    # Subclasses may implement this more efficiently
    def conflict(var2):
        conflicted = var2 in assignment and not self.constraints(var, val, var2, assignment[var2])
        if conflicted:
            # print("CONFLICTEDDDDDDD var2 = " + str(var2))
            var_conflict_set.add(var2)
        return conflicted
        # return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

    return count(conflict(v) for v in self.neighbors[var])

def forward_checking(csp, var, value, assignment, removals, var_conflict_set):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                # var_conflict_set[B] = True #add the conflicted variable in the current var conflict set
                print('THA EPISTREPSW FALSE')
                return False
    return True

def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result


def conflict_directed_backjumping(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values):
    conflict_set = {}
    assignment = OrderedDict()
    def CBJ():
        if len(assignment) == len(csp.variables):
            return assignment

        var = select_unassigned_variable(assignment, csp)
        print ("var = " + str(var))

        # if var not in conflict_set:
        conflict_set[var] = set()

        for value in order_domain_values(var, assignment, csp):
            if 0 == nconflicts(csp, var, value, assignment, conflict_set[var]):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                # if forward_checking(csp, var, value, assignment, removals, conflict_set[var]):
                result = CBJ()
                print('eimai prin to return result = ' + str(result) + ' var = ' + str(var))
                if result!=var and result is not None:
                    return result
                csp.restore(removals)
            print("conflict dict of " + str(var) + " = " + str(conflict_set[var]))

        csp.unassign(var, assignment)


        if conflict_set[var]:
            # print(conflict_set[var])
            # h = next(reversed(conflict_set[var]))

            print(assignment)

            for k, v in ((k, assignment[k]) for k in reversed(assignment)):
                print (k,v)
                if k in conflict_set[var]:
                    h = k
                    conflict_set[var].remove(h)
                    for x in conflict_set[var]:
                        conflict_set[h].add(x) # merge(conf_set[h], conf_set[current])
                    del conflict_set[var]
                    print('EPISTREFW H ' + str(h))
                    return h


            # if h not in conflict_set:
            #     print()
            #     conflict_set[h] = OrderedDict()

        # else:
            # print('EPISTREFW NONEEEEEEEEEEEEEEE')
        # print('EPISTREFW NONEEEEEEEEEEEEEEE')
        return None


    result = CBJ()
    print('EIMAI PRIN TO RESULT result = ' + str(result))
    assert result is None or csp.goal_test(result)
    return result



def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):

        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True


    if not csp.curr_domains[Xi][:]:
        # print('THA AUKSISW TO WEIGHT ' + str(Xi) + ' ' + str(Xj))

        k.increase_constraint_weight(Xi,Xj)
        # print('weight meta = ' + str(k.get_constraint_weight(Xi,Xj)))


    # elif not csp.curr_domains[Xj][:]:
    #     k.increase_constraint_weight(Xi,Xj)
    #
    #     print('MPHKA STO DEUTERO IF')
    #     # csp.
    return revised, checks


instance = "2-f24"
# instance = "11"
# instance = "3-f10"

k = RLFA(instance)
constraints_dict = k.get_constraints_dict(k.constraints_list)

start_time = time.time()
# result = backtracking_search(k, select_unassigned_variable=mrv, inference=mac)
# result = backtracking_search(k, select_unassigned_variable=domwdeg_dynamic_variable, inference=mac)

result = conflict_directed_backjumping(k, select_unassigned_variable=domwdeg_dynamic_variable)
print (result)

# myset = set()
# myset.add(100)
# myset.add(-100)
# myset.add(-200)
# myset.add(100000)

# for x in myset:
#     print (x)
# print(str(next(reversed(myset))))

# myset = OrderedDict()
# myset[100] = "1"
# myset[-100] = "2"
# myset[-200] = "3"
# myset[100000] = "4"

# for k, v in ((k, myset[k]) for k in reversed(myset)):
#     print(k)
#     print(v)


# print(myset)

print("Instance: " + instance + " | MRV + MAC Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(k.nassigns) + " | Number of constraint checks: " + str(k.constraints_check_no))

