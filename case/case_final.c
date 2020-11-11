#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SMALL_BAG 125
#define LARGE_BAG 200

/* An item to be considered in a knapsack problem,
   represented in a problem file by a line of text
   (ex: "cmbucrvcoz	30	46") */
typedef struct {
	char name[16];
	int value;
	int weight;
} Item;

typedef struct
{
	int size;
	Item items[SMALL_BAG];
} Bag;

typedef struct
{
	int size;
	Item items[LARGE_BAG];
} BigBag;

/* A knapsack problem with a title, maximum capacity, 
   and a list of items to be arranged in potential bags */
typedef struct
{
	char title[16];
	int capacity;
	Bag bag;
} Problem;

int max(int a, int b) { return (a > b) ? a : b; }
void put_bag(Bag *bag, Item item) { (*bag).items[(*bag).size] = item; (*bag).size++; }
int weigh_bag(Bag bag)
{ 
	int weight = 0; 
	for (int i = 0; i < bag.size; i++) 
		weight += bag.items[i].weight;
	return weight;
}
int score_bag(Bag bag)
{
	int score = 0;
	for (int i = 0; i < bag.size; i++)
		score += bag.items[i].value;
	return score;
}

int read_num_problems(char* fname)
{
	FILE* fp;
	char* line;
	size_t len = 0;
	ssize_t read;
	int n = 1;

	fp = fopen(fname, "r");

	read = getline(&line, &len, fp);
	n = strtol(line, NULL, 10);

	fclose(fp);
	if (line)
		free(line);

	return n;
}

/* A function which reads a properly formatted (be
   careful since little checking is done to ensure
   the format is proper and errors or strange behavior 
   may occur if you deviate from it) problems file 
   into a Problem struct */
void read_problems_file(char* fname, Problem *plist)
{
	FILE* fp;
	char* line;
	size_t len = 0;
	ssize_t read;

	int lnum = 0;
	int loff = 0;
	int pnum = 0;

	fp = fopen(fname, "r");
	while ((read = getline(&line, &len, fp)) != -1)
	{
	READLINES:
		if (lnum == 0) 
		{
			/* It's important that you run read_num_problems before
			   read_problems_file so this function doesn't have to 
			   dynamically allocate memory for the main function */
		} 
		else if (lnum-loff == 1) 
		{
			line[strlen(line)-1] = 0;
			strcpy(plist[pnum].title, line);
		} 
		else if (lnum-loff == 2)
		{
			plist[pnum].capacity = strtol(line, NULL, 10);
			plist[pnum].bag.size = 0;
		} 
		else 
		{
			Item next_item;
			char value_str[8];
			char weight_str[8];
			int i = 0;
			int o1, o2;

			// Parse name from line
			while (1)
			{
				if (line[i] == '\0')
				{
					pnum++;
					loff = lnum-1;
					goto READLINES; // YEAH BABYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
				}

				if (line[i] == '\t')
				{
					next_item.name[i] = '\0';
					break;
				}
				next_item.name[i] = line[i];
				i++;
			}

			i++;
			o1 = i;

			// Parse value from line
			while (1)
			{
				if (line[i] == '\t') 
				{
					value_str[i-o1] = '\0';
					next_item.value = strtol(value_str, NULL, 10);
					break;
				}
				value_str[i-o1] = line[i];

				i++;
			}

			i++;
			o2 = i;

			// Parse weight from line
			while (1)
			{
				if (line[i] == '\0') 
				{
					weight_str[i-o2] = '\0';
					next_item.weight = strtol(weight_str, NULL, 10);
					break;
				}
				weight_str[i-o2] = line[i];

				i++;
			}

			put_bag(&plist[pnum].bag, next_item);
		}

		lnum++;
	}

	fclose(fp);
	if (line)
		free(line);
}

Bag bruteforce_solve(int capacity, Bag bag) 
{
	if (bag.size == 0 || capacity == 0)
	{
		// tmp will return a score of 0 when scored
		Bag tmp;
		tmp.size = 0;
		return tmp;
	}

	bag.size--;
	if (bag.items[bag.size].weight > capacity)
		return bruteforce_solve(capacity, bag);
	else
	{
		Bag b1 = bruteforce_solve(capacity-bag.items[bag.size].weight, bag);
		put_bag(&b1, bag.items[bag.size]);
		Bag b2 = bruteforce_solve(capacity, bag);

		if (score_bag(b1) > score_bag(b2))
			return b1;
		else 
			return b2;
	}
}

Bag dynamic_solve(int capacity, Bag bag, Bag **table)
{
	/*Bag (**T) = (Bag**) malloc((bag.size+1)*sizeof(Bag*));
	for (int i = 0; i < bag.size+1; i++)
		T[i] = (Bag*) malloc((capacity+1)*sizeof(Bag));*/
	int i, w;

	for (i = 0; i <= bag.size; i++)
	{
		for (w = 0; w <= capacity; w++)
		{
			if (i == 0 || w == 0)
			{
				Bag tmp;
				tmp.size = 0;
				table[i][w] = tmp;
			}
			else if (bag.items[i-1].weight <= w)
			{
				Bag b1 = table[i-1][(w-bag.items[i-1].weight)];
				put_bag(&b1, bag.items[i-1]);

				if (score_bag(b1) > score_bag(table[i-1][w]))
					table[i][w] = b1;
				else
					table[i][w] = table[i-1][w];
			}
			else
				table[i][w] = table[i-1][w];
		}
	}

	return table[bag.size][capacity];
}

int main(int argc, char *argv[]) 
{
	if (argc != 2)
	{
		printf("Please supply exactly one argument with the path of the problems file.\n");
		return 1;
	}

	char* fname = argv[1];

	Problem* p;
	int n;

	n = read_num_problems(fname);
	p = (Problem*) malloc(n*sizeof(Problem));

	Bag (**table) = (Bag**) malloc((LARGE_BAG)*sizeof(Bag*));
	for (int i = 0; i < LARGE_BAG; i++)
		table[i] = (Bag*) malloc((10000)*sizeof(Bag));

	read_problems_file(fname, p);

	double total_time = 0;
	for (int i = 0; i < n; i++)
	{
		Bag b;
		clock_t t;
		t = clock();

		// Use comments to decide which function you want to run
		//b = bruteforce_solve(p[i].capacity, p[i].bag);
		b = dynamic_solve(p[i].capacity, p[i].bag, table);

		t = clock() - t;
		double func_time = ((double)t)/CLOCKS_PER_SEC;
		total_time += func_time;

		printf("\nSolution for %s:\n", p[i].title);
		printf("[\n");
		for (int j = 0; j < b.size; j++)
		{
			printf("  %s\n", b.items[j]);
		}
		printf("] time: %fs \n", func_time);
	}

	printf("\nCompleted %d problems in %fs\n", n, total_time);
	free(p);

	return 0;
}