from csp import *


def my_AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = my_revise(csp, Xi, Xj, removals, checks)
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


def my_mac(csp, var, value, assignment, removals, constraint_propagation=my_AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)


def my_backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def my_backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)

        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = my_backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = my_backtrack({})
    assert result is None or csp.goal_test(result)
    return result


def my_revise(csp, Xi, Xj, removals, checks=0):
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
        csp.increase_constraint_weight(Xi,Xj)

    return revised, checks