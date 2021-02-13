from csp import *

def get_variables_dict(variables_str):
    variables = {}
    variables_list = variables_str.splitlines()
    variables_number = int(variables_list.pop(0))
    for x in range(variables_number):
        current_line = variables_list[x].split()
        current_line = list(map(int, current_line))  # convert the string list to int list
        variables[current_line[0]] = current_line[1]
    return variables

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

def get_constraint_list(containts_str):
    constraint_list = containts_str.splitlines()
    constraints_number = int(constraint_list.pop(0))
    if constraints_number != len(constraint_list):
        raise ValueError("Wrong lines input")

    splitted_constraints_list = []
    for node in constraint_list:
        #split the list into separate strings
        current_splitted_constraints_list = node.split()
        splitted_constraints_list.append(current_splitted_constraints_list)

    return splitted_constraints_list

def assign_domains_to_variables(variables_dict, domains_dict):
    variables_domain_dict = {}
    for variable, domain in variables_dict.items():
        variables_domain_dict[variable] = domains_dict[domain]
    return variables_domain_dict

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

        #assign the values
        neighbors_dict[x].append(y)
        neighbors_dict[y].append(x)

    return neighbors_dict

def get_constraints_dict(constraints_list):
    constraints_dict = {}
    for current_list in constraints_list:
        x = int(current_list[0])
        y = int(current_list[1])
        comp =  current_list[2]
        k = int(current_list[3])

        #assign the values
        if (x,y) in constraints_dict:
            print ("More than one constraints for the same variables. Only the last one will remain.")

        constraints_dict[(x,y)] = (comp, k)

    return constraints_dict

def constraints_function(A, a, B, b, constraints_dict):
    comp, k = constraints_dict[(A,B)]
    if comp == '>':
        return abs(a - b) > k
    elif comp == '=':
        return abs(a - b) == k
    else:
        raise ValueError("Wrong compare operator")

instance = "11"
domains_file = open("rlfap/dom" + instance + ".txt", "r")
variables_file = open("rlfap/var" + instance + ".txt", "r")
constraints_file = open("rlfap/ctr" + instance + ".txt", "r")

domains_dict = get_domains_dict(domains_file.read())
variables_dict = get_variables_dict(variables_file.read())
constraints_list = get_constraint_list(constraints_file.read())

variables_list = list(variables_dict.keys())
variables_domain_dict = assign_domains_to_variables(variables_dict, domains_dict)

neighbors_dict = get_neighbors_dict(constraints_list)

constraints_dict = get_constraints_dict(constraints_list)
# print(constraints_dict)

# constraints_function(260, 200, 261, 439, constraints_dict)




