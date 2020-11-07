Backpack_contents = [];
result_list = [];

def loaddataset(filename):
    dataset = open(filename, 'r');
    Promblem_instance_number = dataset.readline().split()[0];
    Promblem_instance_number = int(Promblem_instance_number);
    problem_content = [];
    problem_name = "";
    problem_capacity = 0;
    for line in dataset:
        line_element = line.split();
        if len(line_element) == 1:
            if "Problem" in line_element[0]:
                if len(problem_content) != 0:
                    Backpack_contents.append((problem_name,problem_capacity,problem_content));
                    problem_content = [];
                problem_name = line_element[0];
            else:
                capacity = int(line_element[0]);
                problem_capacity = capacity;
        else:
            item, value, weight = line.split();
            value = int(value);
            weight = int(weight);
            problem_content.append((item, value, weight));
    Backpack_contents.append((problem_name,problem_capacity,problem_content));

    dataset.close();

def Recursive(problem_content, currentindex, capacity):
    if capacity<= 0 or currentindex >= len(problem_content):
        return 0;

    profit1 = 0;

    if problem_content[currentindex][2] <= capacity:
        profit1 = problem_content[currentindex][1] + Recursive(problem_content, currentindex + 1,
        capacity - problem_content[currentindex][2]);

    profit2 = Recursive(problem_content, currentindex + 1, capacity);

    return max(profit1, profit2);




def main():
    loaddataset("Toy Problem.txt");
    test = Backpack_contents[1];
    print(test[2], test[1]);
    print(Recursive(test[2],0,test[1]));
