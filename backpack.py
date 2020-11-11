import numpy as np;
import time;
import matplotlib.pyplot as plt;
from LinkedList import *;

#Load the problem file and save all the questions into a list
#Return the list, which contains each question in each index with a format (name, capacity, items)
#filename: the name of the file which contains the problems
def loaddataset(filename):
    Backpack_contents = LinkedList();
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
                    Backpack_contents.add((problem_name,problem_capacity,problem_content));
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
    Backpack_contents.add((problem_name,problem_capacity,problem_content));

    dataset.close();
    return Backpack_contents;

#This function is the starting point of my thinking process
#It recursively approaches different probilities of including
#or not including the next element
#Returns the largest profit
#problem_content: a list of the items with value and weight in the problem
#currentindex: current position in the problem_content list
#capacity: the largest weight that the backpack in the question is allowed to hold
def Recursive(problem_content, currentindex, capacity):
    if capacity<= 0 or currentindex >= len(problem_content):
        return 0;

    profit1 = 0;

    if problem_content[currentindex][2] <= capacity:
        profit1 = problem_content[currentindex][1] + Recursive(problem_content, currentindex + 1,
        capacity - problem_content[currentindex][2]);

    profit2 = Recursive(problem_content, currentindex + 1, capacity);

    return max(profit1, profit2);

#Create a dynamic matrix which holds the best profits when adding each item at capacity c (0 <= c< = capacity)
#Return the dynamic matrix
#capacity: the largest weight that the backpack in the question is allowed to hold
#problem_content: a list of the items with value and weight in the problem
def CreateDynamicMatrix(capacity, problem_content):
    n = len(problem_content);
    matrix = np.zeros((n, capacity + 1));

    for c in range(capacity + 1):
        if problem_content[0][2] <= c:
            matrix[0][c] = problem_content[0][1];

    for i in range(1, n):
        for j in range(1, capacity+1):
            profit1 = 0;
            profit2 = 0;
            if problem_content[i][2] <= j:
                profit1 = problem_content[i][1] + matrix[i-1][j-problem_content[i][2]];
            profit2 = matrix[i-1][j];

            matrix[i][j] = max(profit1, profit2);
    return matrix;

#Get the selected items from the dynamic matrix
#Return the legal set of items which have the largest sum of profit
#capacity: the largest weight that the backpack in the question is allowed to hold
#problem_content: a list of the items with value and weight in the problem
#matrix: the dynamic matrix created by the function CreateDynamicMatrix
def GetSet(capacity, problem_content, matrix):
    resultset = []
    totalvalue = matrix[len(problem_content)-1][capacity];
    for currentrow in range(len(problem_content)-1, 0, -1):
        if matrix[currentrow-1][capacity] != totalvalue:
            resultset.append(problem_content[currentrow][0]);
            totalvalue -= problem_content[currentrow][1];
            capacity -= problem_content[currentrow][2];
    if totalvalue != 0:
        resultset.append(problem_content[0][0]);
    return resultset;

#Solve each question in a list of questions
#Return a list that holds the answer set for each of the problems in the problem list
#problem_list: the list of all the questions in the file which contains backpack problems
def solve(problem_list):
    answerset = []
    for i in range(problem_list.get_size()):
        matrix = CreateDynamicMatrix(problem_list.get(i)[1], problem_list.get(i)[2]);
        resultset = GetSet(problem_list.get(i)[1], problem_list.get(i)[2], matrix);
        resultset = sorted(resultset);
        answerset.append(resultset);
    return answerset;

def solveKnapsackFile(filename):
    Backpack_contents = loaddataset(filename);
    result = solve(Backpack_contents);
    return result;

def main():
    timing_test = [10,15,20,30,40,50,75,100,200,300,400,500,1000];
    result = []
    for timing in timing_test:
        t = str(timing);
        start_time = time.perf_counter();
        Backpack_contents = loaddataset("problems_size"+t+".txt");
        Solve(Backpack_contents);
        end_time = time.perf_counter();
        result.append(end_time - start_time);
    plt.xlabel("Input size");
    plt.ylabel("Running time");
    plt.plot(timing_test, result, 'r');
    plt.show();
