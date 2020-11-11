import time
import sys

# Reads a list of problems from a properly-formatted text file
# and returns an array of Problem objects with matching properties
def read_problems(fname):
	with open(fname, 'r') as pfile:
		lines = pfile.readlines()

	problems = []
	for line in lines[1:]:
		line_arr = line.strip().split()

		if len(line_arr) == 1:
			try:
				problems[-1].max_weight = int(line_arr[0])
			except ValueError:
				problems.append(Problem(line_arr[0]))
		elif len(line_arr) == 3:
			name = line_arr[0]
			weight = int(line_arr[1])
			value = int(line_arr[2])
			problems[-1].names_values_weights.append([name, weight, value])
		else:
			raise RuntimeError("Encountered an issue! Exiting.")

	return problems


# A class representing a single knapsack problem
class Problem:
	def __init__(self, title='Unnamed Problem'):
		self.title = title
		self.max_weight = 0
		self.names_values_weights = []

	def __repr__(self):
		to_str = ""
		to_str += self.title + "\n"
		to_str += str(self.max_weight) + "\n"
		for nvw in self.names_values_weights:
			spacing = "\t" if len(nvw[0]) < 8 else ""
			to_str += nvw[0] + "\t" + spacing + str(nvw[1]) + "\t" + str(nvw[2]) + "\n"
		return to_str

def bruteforce_solve(max_weight, nvw):
	if len(nvw) == 0 or max_weight == 0:
		return []

	nvw_next = [item for item in nvw[:-1]]
	if not nvw_next or nvw_next[-1][2] > max_weight:
		return bruteforce_solve(max_weight, nvw_next)

	else:
		nvw1 = bruteforce_solve(max_weight-nvw_next[-1][2], nvw_next)
		nvw1.append(nvw[-1])
		nvw2 = bruteforce_solve(max_weight, nvw_next)

		if sum([item[1] for item in nvw1]) > sum([item[1] for item in nvw2]):
			return nvw1
		else:
			return nvw2

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Please supply exactly one argument with the path of the problems file")
		exit(1)

	problems = read_problems(sys.argv[1])
	total_time = 0
	for problem in problems:
		start = time.time()
		solution = bruteforce_solve(problem.max_weight, problem.names_values_weights)
		func_time = time.time()-start
		total_time += func_time
		print("\nSolution for %s:" % problem.title)
		print("[")
		for item in solution:
			print("  %s" % item[0])
		print("] time: %fs" % func_time)
	print("\nCompleted %d problems in %fs" % (len(problems), total_time))
