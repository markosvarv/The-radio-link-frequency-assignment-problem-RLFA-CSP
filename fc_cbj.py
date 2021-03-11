import collections
from csp import *


def conflict_directed_backjumping(csp, select_unassigned_variable=first_unassigned_variable,
                                  order_domain_values=unordered_domain_values):
    conflict_set = {}
    assignment = collections.OrderedDict()

    def CBJ():
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)

        conflict_set[var] = set()

        for value in order_domain_values(var, assignment, csp):
            if 0 == cbj_nconflicts(csp, var, assignment, conflict_set[var], value):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if forward_checking_cbj(csp, var, value, assignment, removals, conflict_set[var]):
                    result = CBJ()

                    if result != var:
                        csp.restore(removals)
                        if type(result) == type(var):
                            csp.unassign(var, assignment)
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)

        if conflict_set[var]:
            for k, v in ((k, assignment[k]) for k in reversed(assignment)):  # we want the most recent assigned var
                if k in conflict_set[var]:
                    h = k
                    conflict_set[var].remove(k)
                    for x in conflict_set[var]:
                        conflict_set[h].add(x)  # merge(conf_set[h], conf_set[current])
                    del conflict_set[var]
                    return h
        return None

    result = CBJ()
    assert result is None or csp.goal_test(result)
    return result


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


def forward_checking_cbj(csp, var, value, assignment, removals, var_conflict_set):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                var_conflict_set.add(B)  # add the conflicted variable in the current var conflict set
                # print('THA EPISTREPSW FALSE')
                return False
    return True