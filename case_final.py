

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
			problems[-1].names_weights_values.append([name, weight, value])
		else:
			raise RunTimeError("Encountered an issue! Exiting.")

	return problems


# A class representing a single knapsack problem
class Problem:
	def __init__(self, title='Unnamed Problem'):
		self.title = title
		self.max_weight = 0
		self.names_weights_values = []

	def __repr__(self):
		to_str = ""
		to_str += self.title + "\n"
		to_str += str(self.max_weight) + "\n"
		for n, v, w in zip(self.names, self.values, self.weights):
			spacing = "\t" if len(n) < 8 else ""
			to_str += n + "\t" + spacing + v + "\t" + w + "\n"
		return to_str

	def brute_force(self):
		best_solution = None
		best_score = 0
		for subset in self.bruteforce_recurse([], len(self.names_weights_values)):
			score = sum([item[1] for item in subset])
			weight = sum([item[2] for item in subset])
			if weight <= self.max_weight and score > best_score:
				best_solution = subset
				best_score = score

		return best_solution

	def bruteforce_recurse(self, prev_subset, n_left):
		curr_subsets = [prev_subset + [nwv] for nwv in self.names_weights_values]

		if n_left == 0:
			return curr_subsets
		
		next_subsets = []
		for curr_subset in curr_subsets:
			for next_subset in self.bruteforce_recurse(curr_subset, n_left-1):
				next_subsets.append(next_subset)

		return next_subsets


if __name__ == "__main__":
	problems = read_problems("toy_problems.txt")
	to_solve = problems[1]
	bf_solve = to_solve.brute_force()
	print(bf_solve)
