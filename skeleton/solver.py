import networkx as nx
import os

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
    num_satisfied_groups = 0
    def cost(buses):
        for b in buses:
            for c in constraints:
              num_satisfied_groups += 1 - int(all(x in b for x in c))
        return num_constraints - num_satisfied_groups
        
    def acceptance_probability(cost_old, cost_new, temp):
        return min(1, Math.exp((cost_old - cost_new)/temp))
      
    def neighbors(buses, num_buses, size_bus):
        busOne = random.randint(1, num_buses)
        busTwo = random.randint(1, num_buses)
        while busOne == busTwo:
            busTwo = random.randint(1, num_buses)
        sOne = random.randint(1, size_bus)
        sTwo = random.randint(1, size_bus)
        while sOne == sTwo:
            sTwo = random.randint(1, size_bus)
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
                ap = acceptance_probability(old_cost, new_cost, T)
                if ap > random.random():
                    buses = new_buses
                    old_cost = new_cost
                i += 1
            T = T*alpha
        return buses

    students = random.shuffle(graph.nodes())
    initial_sol = []
    x = 0
    for i in range(num_buses):
        initial_sol.append(students[x:x+size_bus])
        x += size_bus
    final_sol = anneal(initial_sol)
    return final_sol

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    for size in size_categories:
        category_path = path_to_inputs + "/" + size
        output_category_path = path_to_outputs + "/" + size
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)

        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder) 
            graph, num_buses, size_bus, constraints = parse_input(category_path + "/" + input_name)
            solution = solve(graph, num_buses, size_bus, constraints)
            output_file = open(output_category_path + "/" + input_name + ".out", "w")

            #TODO: modify this to write your solution to your 
            #      file properly as it might not be correct to 
            #      just write the variable solution to a file
            output_file.write(solution)

            output_file.close()

if __name__ == '__main__':
    main()


