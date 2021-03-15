import collections

# from csp import *
import time
from algorithm import *
from fc_cbj import *
import collections
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


# instance = "2-f24"
# instance = "11"
instance = "3-f10"

k = RLFA(instance)
constraints_dict = k.get_constraints_dict(k.constraints_list)

start_time = time.time()
# result = backtracking_search(k, select_unassigned_variable=mrv, inference=mac)

# result = backtracking_search(k, select_unassigned_variable=domwdeg_dynamic_variable, inference=my_mac)
# result = backtracking_search(k, inference=mac)

# result = backtracking_search(k, select_unassigned_variable=domwdeg_dynamic_variable)
#
result = conflict_directed_backjumping(k, select_unassigned_variable=domwdeg_dynamic_variable)
print(result)

# result = conflict_directed_backjumping(k)

# result = min_conflicts(k, 500000)


# australia_csp = MapColoringCSP(list('RBG'), """SA: WA NT Q NSW V; NT: WA Q; NSW: Q V; T: """)
# result = my_backtracking_search(australia_csp, inference=forward_checking)

# print(conflict_directed_backjumping(usa_csp))
print(conflict_directed_backjumping(australia_csp))


# myset = {}
# myset[100] = True
# myset[-100] = True
# myset[-200] = True
# myset[100000] = True



# for x in myset:
#     print (x)
# print(str(next(reversed(myset))))
#
# myset = collections.OrderedDict()
# myset[100] = "1"
# myset[-100] = "2"
# myset[-200] = "3"
# myset[100000] = "4"
# myset[150] = "5"
# #
# print("my set before: " + str(myset))
#
# myrange = False
# deleted_set = set()
# for key, value in myset.items():
#
#     if key == 100000:
#         myrange = True
#     if myrange:
#             deleted_set.add(key)
#     if key == 150:
#         myrange = False
#
#
# for x in deleted_set:
#     myset[x]=''

# print("deleted set = " + str(deleted_set))
# print("my set after: " + str(myset))




# print(myset)

print("Instance: " + instance + " | MRV + MAC Time: " + str(round(time.time() - start_time, 2)) + " sec. | Assigns number: " + str(k.nassigns) + " | Number of constraint checks: " + str(k.constraints_check_no))

