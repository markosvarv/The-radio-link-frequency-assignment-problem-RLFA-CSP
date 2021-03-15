import collections
from csp import *


def conflict_directed_backjumping(csp, select_unassigned_variable=first_unassigned_variable,
                                  order_domain_values=unordered_domain_values):
    conflict_set = {}
    assignment = collections.OrderedDict()
    checking = {}

    def CBJ():
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)

        conflict_set[var] = set()
        checking[var] = set()
        # print("var = " + str(var))

        # print("checking = " + str(checking))
        # removals = None
        for value in order_domain_values(var, assignment, csp):
            if 0 == cbj_nconflicts(csp, var, assignment, conflict_set[var], value):
                # print("kanw assign stin " + var + " to value " + value)
                csp.assign(var, value, assignment)

                removals = csp.suppose(var, value)
                if forward_checking_cbj(csp, var, value, assignment, removals, checking[var]):

                    # print("removals meta to if: " + str(removals))

                    # checking[var].add("markos")
                    # print("checking of " + str(var) + " = " + str(checking[var]))

                    result = CBJ()

                    # print("epestrepsa CBJ result " + str(result) + " value  = " + value)

                    if result != var:

                        # print("MPHKA STO ANADROMIKO")
                        # print("anadromiko removals gonna be restored = " + str(removals))

                        csp.restore(removals)
                        checking[var].clear()

                        # print("\n\ni am gonna DELETE checking of " + str(var) + " = " + str(checking[var]) + '\n\n')
                        # checking[var].clear()
                        # print("checking of " + str(var) + " = " + str(checking[var]))

                        if type(result) == type(var):
                            # print("tha kanw unassign to " + var + " val = " + value)
                            csp.unassign(var, assignment)
                        return result


                    # print("EINAI ISAAAAAA")

                # print("\n(false) checking of " + str(var) + " = " + str(checking[var]))
                # print("removals = " + str(removals))

                # print("BGIKA APO TO IF removals gonna be restored: " + str(removals))
                csp.restore(removals)
                checking[var].clear()

                # print("\n\ni am gonna DELETE checking of " + str(var) + " = " + str(checking[var]) + '\n\n')
                # checking[var].clear()
                # print("checking of " + str(var) + " = " + str(checking[var]))

        csp.unassign(var, assignment)

        for key_var, var_set in checking.items():
            if var in var_set:
                conflict_set[var].add(key_var)

        # print("conflict set of " + str(var) + " = " + str(conflict_set[var]))

        for k, v in ((k, assignment[k]) for k in reversed(assignment)):  # we want the most recent assigned var
            if k in conflict_set[var]:
                h = k
                conflict_set[var].remove(k)

                # print (conflict_set[var])
                # print(conflict_set[h])

                for x in conflict_set[var]:
                    conflict_set[h].add(x)  # merge(conf_set[h], conf_set[current])
                del conflict_set[var]
                # print("YAAAASSSS EPISTREFW H " + h + '\n')

                # delete_checking_range(checking, h, var)
                # print(checking)
                # print(removals)

                # csp.restore(removals)

                return h
        return None

    result = CBJ()
    assert result is None or csp.goal_test(result)
    return result


def delete_checking_range (checking, h, var):
    myrange = False
    deleted_set = set()
    for key in checking:
        if key == h:
            myrange = True
        if myrange:
            deleted_set.add(key)
        if key == var:
            myrange = False

    for x in deleted_set:
        checking[x].clear()

    # print("DELETED set = " + str(deleted_set))

def cbj_nconflicts(self, var, assignment, var_conflict_set, val):
    newest_neighbors = collections.OrderedDict()

    # first add all the newest neighbors
    for x in reversed(list(assignment)):
        if x in self.neighbors[var]:
            newest_neighbors[x] = True

    # then add all the neighbors that haven't assigned yet
    for n in self.neighbors[var]:
        newest_neighbors[n] = True

    conflict_num = 0
    for neighbor in newest_neighbors:
        conflicted = neighbor in assignment and not self.constraints(var, val, neighbor, assignment[neighbor])
        if conflicted:
            conflict_num += 1
            var_conflict_set.add(neighbor)

    return conflict_num


def forward_checking_cbj(csp, var, value, assignment, removals, var_checking):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
                    # print("THA VALW TO " + str(B))
                    var_checking.add(B)

            if not csp.curr_domains[B]:
                # var_conflict_set.add(B)  # add the conflicted variable in the current var conflict set
                # print('THA EPISTREPSW FALSE')
                return False
    return True



# def conflict_directed_backjumping(csp, select_unassigned_variable=first_unassigned_variable,
#                                   order_domain_values=unordered_domain_values):
#     conflict_set = {}
#     assignment = collections.OrderedDict()
#
#     def CBJ():
#         if len(assignment) == len(csp.variables):
#             return assignment
#         var = select_unassigned_variable(assignment, csp)
#
#         conflict_set[var] = set()
#
#         for value in order_domain_values(var, assignment, csp):
#             if 0 == cbj_nconflicts(csp, var, assignment, conflict_set[var], value):
#                 csp.assign(var, value, assignment)
#                 removals = csp.suppose(var, value)
#                 result = CBJ()
#
#                 if result != var:
#                     csp.restore(removals)
#                     if type(result) == type(var):
#                         csp.unassign(var, assignment)
#                     return result
#                 csp.restore(removals)
#         csp.unassign(var, assignment)
#
#         for k, v in ((k, assignment[k]) for k in reversed(assignment)):  # we want the most recent assigned var
#             if k in conflict_set[var]:
#                 h = k
#                 conflict_set[var].remove(k)
#                 for x in conflict_set[var]:
#                     conflict_set[h].add(x)  # merge(conf_set[h], conf_set[current])
#                 del conflict_set[var]
#                 return h
#         return None
#
#     result = CBJ()
#     assert result is None or csp.goal_test(result)
#     return result