from csp import *


def domwdeg_dynamic_variable(assignment, csp):
    """The dom/wdeg heuristic variable order."""

    uninstantiated_vars_number = len(csp.variables) - len(assignment)
    print("Uninstantiated variables number = " + str(uninstantiated_vars_number))
    if csp.curr_domains is not None:
        my_min = 999999
        return_var = 999999

        for myvar in csp.variables:
            if myvar not in assignment:
                domain_list = csp.curr_domains[myvar]

                dom = len(domain_list)
                wdeg = 1
                neighbors = csp.neighbors[myvar]
                for neighbor_var in neighbors:
                    if neighbor_var not in assignment:
                        wdeg += csp.get_constraint_weight(myvar, neighbor_var)
                h = dom/wdeg

                if h < my_min:
                    my_min = h
                    return_var = myvar
        return return_var

    else:
        return first([var for var in csp.variables if var not in assignment])


def domwdeg_revise(csp, Xi, Xj, removals, checks=0):
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
        csp.increase_constraint_weight(Xi, Xj)  # increase weight for the domwdeg

    return revised, checks


def domwdeg_AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = domwdeg_revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable


def domwdeg_forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                csp.increase_constraint_weight(var, B)  # increase weight for the domwdeg
                return False
    return True


def domwdeg_mac(csp, var, value, assignment, removals, constraint_propagation=domwdeg_AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)