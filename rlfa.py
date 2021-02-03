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
    return constraint_list

def assign_domains_to_variables(variables_dict, domains_dict):
    variables_domain_dict = {}
    for variable, domain in variables_dict.items():
        variables_domain_dict[variable] = domains_dict[domain]
    return variables_domain_dict



instance = "11"
domains_file = open("rlfap/dom" + instance + ".txt", "r")
variables_file = open("rlfap/var" + instance + ".txt", "r")
constraints_file = open("rlfap/ctr" + instance + ".txt", "r")

domains_dict = get_domains_dict(domains_file.read())
variables_dict = get_variables_dict(variables_file.read())
constraints_list = get_constraint_list(constraints_file.read())

print(constraints_list)

variables_list = list(variables_dict.keys())
variables_domain_dict = assign_domains_to_variables(variables_dict, domains_dict)



