import networkx as nx
import os
import random
import math
import time
import copy

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "../all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "../outputs"

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(folder_name + "/graph.gml")
    parameters = open(folder_name + "/parameters.txt")
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []

    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def solve(graph, num_buses, size_bus, constraints):
    #TODO: Write this method as you like. We'd recommend changing the arguments here as well
    num_constraints = len(constraints)
    num_edges = len(graph.edges())
    def cost(buses):
        new_buses = [set(b) for b in buses]
        num_satisfied_groups = 0
        for c in constraints:
            for b in new_buses:
                if all(x in b for x in c):
                    num_satisfied_groups -= 1
                    break
            num_satisfied_groups += 1
        #TODO: calculate number of friendships broken
        num_friendships = 0
        for edge in list(graph.edges):
            for b in new_buses:
                if edge[0] in b and edge[1] in b:
                    num_friendships += 1
                    break
        return 2*(num_friendships)/(.1 + num_edges) + num_satisfied_groups/(0.1 + num_constraints)

    def acceptance_probability(cost_old, cost_new, temp):
        try:
            exp = math.exp((cost_old - cost_new)/temp)
        except OverflowError:
            exp = 1.0
        return exp

    def neighbors(buses, num_buses, size_bus):
        busOne = random.randint(0, num_buses - 1)
        busTwo = random.randint(0, num_buses - 1)
        while busOne == busTwo:
            busTwo = random.randint(0, num_buses - 1)
        #print(buses[busTwo])
        sOne = random.randint(0, len(buses[busOne]) - 1)
        sTwo = random.randint(0, len(buses[busTwo]) - 1)
        # while sOne == sTwo:
        #     sTwo = random.randint(1, len(buses[busTwo]) - 1)
        temp = buses[busOne][sOne]
        buses[busOne][sOne] = buses[busTwo][sTwo]
        buses[busTwo][sTwo] = temp
        return buses

    def anneal(buses):
        old_cost = cost(buses)
        best = cost(buses)
        min_sol = buses
        T = 1.0
        T_min = 0.00001
        alpha = 0.988
        while T > T_min:
            i = 1
            curr_time = time.time()
            if (curr_time - start)/60 >= 30.0:
                break
            while i <= 500:
                new_buses = neighbors(buses, num_buses, size_bus)
                new_cost = cost(new_buses)
                if new_cost - best >= 0.08:
                    best = new_cost
                    min_sol = copy.deepcopy(new_buses)
                ap = acceptance_probability(old_cost, new_cost, T)
                if ap > random.random():
                    buses = new_buses
                    old_cost = new_cost
                i += 1
            T = T*alpha
        if cost(buses) > best:
            return buses
        return min_sol

    students = list(graph.nodes())
    random.shuffle(students)
    # students = []
    # for e in graph.edges:
    #     if e[0] not in students:
    #         students.append(e[0].encode('ascii', 'ignore').decode("utf-8"))
    #     if e[1] not in students:
    #         students.append(e[1].encode('ascii', 'ignore').decode("utf-8"))
    # for s in graph.nodes():
    #     if s not in students:
    #         students.append(s.encode('ascii', 'ignore').decode("utf-8"))
    initial_sol = [[] for _ in range(num_buses)]
    x = 0
    # chunk = len(students)//num_buses
    # for i in range(num_buses):
    #     initial_sol[i] = students[x:x+chunk]
    #     x += chunk
    # i = 0 
    # if x < len(students):   
    #     rest = students[x:]
    #     for student in rest: 
    #         if i == num_buses:
    #             i = 0
    #         initial_sol[i] += [student]
    #         i += 1
    #print(initial_sol)
    #print(len(initial_sol))
    for s in students:
        if x == num_buses:
            x = 0
        initial_sol[x] += [s.encode('ascii', 'ignore').decode("utf-8")]
        x += 1
    start = time.time()
    return initial_sol
    #print(cost(initial_sol))
    # final_sol = anneal(initial_sol)
    # finish = time.time()
    # print("total minutes to find solution: ", (finish-start)/60.0)
    # print(cost(final_sol) - cost(initial_sol))
    # return final_sol

# def main():
#     '''
#         Main method which iterates over all inputs and calls `solve` on each.
#         The student should modify `solve` to return their solution and modify
#         the portion which writes it to a file to make sure their output is
#         formatted correctly.
#     '''
#     #size_categories = ["small", "medium", "large"]
#     size_categories = ["medium"]
#     if not os.path.isdir(path_to_outputs):
#         os.mkdir(path_to_outputs)

#     for size in size_categories:
#         category_path = path_to_inputs + "/" + size
#         output_category_path = path_to_outputs + "/" + size
#         category_dir = os.fsencode(category_path)

#         if not os.path.isdir(output_category_path):
#             os.mkdir(output_category_path)

#         for input_folder in os.listdir(category_dir):
#             input_name = os.fsdecode(input_folder)
#             if input_name == ".DS_Store": # or input_name in ["56", "21", "3"]:
#                 continue
#             graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
#             solution = solve(graph, num_buses, size_bus, constraints)
#             output_file = open(output_category_path + "/" + input_name + ".out", "w")

#             #TODO: modify this to write your solution to your
#             #      file properly as it might not be correct to
#             #      just write the variable solution to a file
#             with output_file as f:
#                 for bus in solution:
#                     f.write("%s\n" % bus)

#             output_file.close()

# if __name__ == '__main__':
#     main()

def test():
    for i in range(225, 331):
    # for i in inputs:
        if i in [231, 258, 273, 287, 302, 304, 312, 321, 322]:
            continue
        input_folder = "../all_inputs/medium/" + str(i)
        graph, num_buses, size_bus, constraints = parse_input(input_folder)
        solution = solve(graph, num_buses, size_bus, constraints)
        output_file = "medium2/" + str(i) + ".out"
        with open(output_file, "w") as f:
            for bus in solution:
                f.write("%s\n" % bus)
        #print(solution)
test()
