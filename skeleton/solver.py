import networkx as nx
import os
import random
import math

###########################################
# Change this variable to the path to
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = "./all_inputs"

###########################################
# Change this variable if you want
# your outputs to be put in a
# different folder
###########################################
path_to_outputs = "./outputs"

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
    def cost(buses):
        num_satisfied_groups = 0
        for c in constraints:
            for b in buses:
                if all(x in b for x in c):
                    num_satisfied_groups -= 1
                    break
            num_satisfied_groups += 1
        #TODO: calculate number of friendships broken
        num_friendships = 0
        for edge in list(graph.edges):
            for b in buses:
                if edge[0] in b and edge[1] in b:
                    num_friendships += 1
                    break
        return (num_constraints - num_satisfied_groups) - 5*num_friendships

    def acceptance_probability(cost_old, cost_new, temp):
        try:
            exp = math.exp((cost_old - cost_new)/temp)
        except OverflowError:
            exp = 1.0
        return exp
        #return min(1, math.exp((cost_old - cost_new)/temp))

    def neighbors(buses, num_buses, size_bus):
        busOne = random.randint(0, num_buses - 1)
        busTwo = random.randint(0, num_buses - 1)
        while busOne == busTwo:
            busTwo = random.randint(0, num_buses - 1)
        #print(buses[busTwo])
        sOne = random.randint(0, len(buses[busOne]) - 1)
        sTwo = random.randint(0, len(buses[busTwo]) - 1)
        while sOne == sTwo:
            sTwo = random.randint(1, len(buses[busTwo]) - 1)
        temp = buses[busOne][sOne]
        buses[busOne][sOne] = buses[busTwo][sTwo]
        buses[busTwo][sTwo] = temp
        return buses

    def anneal(buses):
        old_cost = cost(buses)
        T = 1.0
        T_min = 0.00001
        alpha = 0.98
        while T > T_min:
            i = 1
            while i <= 100:
                new_buses = neighbors(buses, num_buses, size_bus)
                new_cost = cost(new_buses)
                # if new_cost == 0:
                #     return buses
                ap = acceptance_probability(old_cost, new_cost, T)
                if ap > random.random():
                    buses = new_buses
                    old_cost = new_cost
                i += 1
            T = T*alpha
        return buses

    students = graph.nodes()
    initial_sol = [[] for _ in range(num_buses)]
    x = 0
    for s in students:
        if x == num_buses:
            x = 0
        initial_sol[x] += [s.encode('ascii', 'ignore').decode("utf-8")]
        x += 1
    final_sol = anneal(initial_sol)
    return final_sol

# def main():
#     '''
#         Main method which iterates over all inputs and calls `solve` on each.
#         The student should modify `solve` to return their solution and modify
#         the portion which writes it to a file to make sure their output is
#         formatted correctly.
#     '''
#     size_categories = ["small", "medium", "large"]
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
#             graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
#             solution = solve(graph, num_buses, size_bus, constraints)
#             output_file = open(output_category_path + "/" + input_name + ".out", "w")

#             #TODO: modify this to write your solution to your
#             #      file properly as it might not be correct to
#             #      just write the variable solution to a file
#             output_file.write(solution)

#             output_file.close()

# if __name__ == '__main__':
#     main()

def test():
    input_folder = "../inputs/small"
    graph, num_buses, size_bus, constraints = parse_input(input_folder)
    solution = solve(graph, num_buses, size_bus, constraints)
    #output_file = open("../x.out", "w")
    with open("output.out", "w") as f:
        for bus in solution:
            f.write("%s\n" % bus)
    print(solution)
test()
