import time
from domwdeg import *
from fc_cbj import *
from my_min_conflicts import *


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

    def get_constraints_dict(self, constraints_list):
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

    def increase_constraint_weight(self, A, B):
        comp, k, weight = self.constraints_dict[(A, B)]
        self.constraints_dict[(A, B)] = (comp, k, weight+1)
        self.constraints_dict[(B, A)] = (comp, k, weight+1)

    def get_constraint_weight(self, A, B):
        comp, k, weight = self.constraints_dict[(A, B)]
        return weight

    def get_list(self):
        return self.constraints_list

    def constraints(self, A, a, B, b):
        comp, k, weight = self.constraints_dict[(A, B)]

        self.constraints_check_no += 1

        if comp == '>':
            return abs(a - b) > k
        elif comp == '=':
            return abs(a - b) == k
        else:
            raise ValueError("Wrong compare operator")

    def __init__(self, instance):
        domains_file = open("rlfap/dom" + instance + ".txt", "r")
        variables_file = open("rlfap/var" + instance + ".txt", "r")
        constraints_file = open("rlfap/ctr" + instance + ".txt", "r")

        domains_dict = self.get_domains_dict(domains_file.read())
        variables_dict = self.get_variables_dict(variables_file.read())
        self.constraints_list = self.get_constraint_list(constraints_file.read())

        variables_list = list(variables_dict.keys())
        variables_domain_dict = self.assign_domains_to_variables(variables_dict, domains_dict)
        self.constraints_dict = self.get_constraints_dict(self.constraints_list)

        neighbors_dict = self.get_neighbors_dict(self.constraints_list)
        self.constraints_check_no = 0

        CSP.__init__(self, variables_list, variables_domain_dict, neighbors_dict, self.constraints)


instance_list = ["2-f24", "2-f25", "3-f10", "3-f11", "6-w2", "7-w1-f4", "7-w1-f5", "11", "8-f10", "8-f11", "14-f27", "14-f28"]


for instance in instance_list:
    """BACKTRACKING"""
    rlfa_csp = RLFA(instance)
    start_time = time.time()
    result_bt_fc = backtracking_search(rlfa_csp, select_unassigned_variable=domwdeg_dynamic_variable, inference=domwdeg_forward_checking)
    print(result_bt_fc)
    print("\nInstance: " + instance + " | BT + FC + dom/wdeg Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(rlfa_csp.nassigns) + " | Number of constraint checks: " + "{:,}".format(rlfa_csp.constraints_check_no))
    print("\n---------------------------------------------------------------------------\n\n")
    rlfa_csp = None
    
    rlfa_csp = RLFA(instance)
    start_time = time.time()
    result_bt_mac = backtracking_search(rlfa_csp, select_unassigned_variable=domwdeg_dynamic_variable, inference=domwdeg_mac)
    print(result_bt_mac)
    print("\nInstance: " + instance + " | BT + MAC + dom/wdeg Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(rlfa_csp.nassigns) + " | Number of constraint checks: " + "{:,}".format(rlfa_csp.constraints_check_no))
    print("\n---------------------------------------------------------------------------\n\n")
    rlfa_csp = None

    # result = backtracking_search(rlfa_csp)
    # result = backtracking_search(rlfa_csp, inference=mac)
    # result = backtracking_search(rlfa_csp, select_unassigned_variable=domwdeg_dynamic_variable)

    """CONFLICT DIRECTED BACKJUMPING"""

    rlfa_csp = RLFA(instance)
    start_time = time.time()
    result_fc_cbj = conflict_directed_backjumping(rlfa_csp, select_unassigned_variable=domwdeg_dynamic_variable, inference=cbj_forward_checking)
    print(result_fc_cbj)
    print("\nInstance: " + instance + " | FC-CBJ + dom/wdeg Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(rlfa_csp.nassigns) + " | Number of constraint checks: " + "{:,}".format(rlfa_csp.constraints_check_no))
    print("\n---------------------------------------------------------------------------\n\n")
    rlfa_csp = None
    # result = conflict_directed_backjumping(rlfa_csp)
    # result = conflict_directed_backjumping(rlfa_csp, select_unassigned_variable=domwdeg_dynamic_variable)
    # result = conflict_directed_backjumping(rlfa_csp, inference=cbj_forward_checking)


"""MIN CONFLICTS"""
# for instance in instance_list:
#     # result = min_conflicts(k, 500000)
#     rlfa_csp = RLFA(instance)
#     start_time = time.time()
#     result = my_min_conflicts(rlfa_csp, 10000)
#
#     print(result)
#     print("Instance: " + instance + " | Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(rlfa_csp.nassigns) + " | Number of constraint checks: " + "{:,}".format(rlfa_csp.constraints_check_no))
#     rlfa_csp = None


"""OTHER PROBLEMS"""
# result = conflict_directed_backjumping(australia_csp, inference=forward_checking_cbj)
# result = conflict_directed_backjumping(usa_csp)