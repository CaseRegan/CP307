

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

	def display_solution(self, subset):
		weight = sum([item[2] for item in subset])
		score = sum([item[1] for item in subset])

		to_str = ""
		to_str += "The following solution was found:\n"
		to_str += "[\n"
		for item in subset:
			to_str += "  %s (%d, %d),\n" % (item[0], item[1], item[2])
		to_str += "]\n"
		to_str += "with a weight of %d/%d and a score of %d.\n" \
		  % (weight, self.max_weight, score)
		to_str += "(items are formatted as: name (value, weight))"

		print(to_str)

	def best_solution(self, generator):
		subsets = generator()
		best_solution = None
		best_score = 0
		for subset in subsets:
			score = sum([item[1] for item in subset])
			weight = sum([item[2] for item in subset])
			if score > best_score:
				best_solution = subset
				best_score = score

		return best_solution

	def gen_all_subsets(self, options=None, prev_subset=[]):
		if not options:
			options = self.names_values_weights

		weight = sum([item[2] for item in prev_subset])
		if weight > self.max_weight:
			return []
		elif weight == self.max_weight:
			return [prev_subset]

		subsets = []
		for option in options:
			next_options = options.copy()
			next_subset = prev_subset.copy()
			next_options.remove(option)
			next_subset.append(option)
			generated = self.gen_all_subsets(next_options, next_subset)
			for subset in generated:
				subsets.append(subset)

		if subsets:
			return subsets
		else:
			return [prev_subset]

if __name__ == "__main__":
	problems = read_problems("problem_sets/10_items.txt")
	for problem in problems:
		solution = problem.best_solution(problem.gen_all_subsets)
		problem.display_solution(solution)
