"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import part1
import pandas as pd
import os
import matplotlib.pyplot as plt
# Make sure the 'data' folder exists
os.makedirs("data", exist_ok=True)



"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""

# Number of times to run each pipeline in the following results.
# You may modify this as you go through the file if you like, but make sure
# you set it back to 10 at the end before you submit.
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        """
        Add a pipeline to the helper.
        """
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)

    def compare_throughput(self):
        # Measure the throughput of all pipelines
        # and store it in a list in self.throughputs.
        # Make sure to use the NUM_RUNS variable.
        # Also, return the resulting list of throughputs,
        # in **number of items per second.**
        """
        Run each pipeline NUM_RUNS times and calculate throughput
        in items per second. Store result in self.throughputs and return it.
        """
        import time
        self.throughputs = []

        for i, func in enumerate(self.pipelines):
            size = self.sizes[i]
            total_time = 0.0
            for _ in range(NUM_RUNS):
                start = time.time()
                func()
                end = time.time()
                total_time += (end - start)
            avg_time = total_time / NUM_RUNS
            # Throughput: items per second
            tp = size / avg_time
            self.throughputs.append(tp)
        return self.throughputs

    def generate_plot(self, filename):
        # Generate a plot for throughput using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8,5))
        plt.bar(self.names, self.throughputs, color='blue')
        plt.ylabel("Throughput (items/sec)")
        plt.xlabel("Pipeline")
        plt.title("Pipeline Throughput Comparison")
        plt.savefig(filename)
        plt.close()

"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    # Return plot method (as a string) from matplotlib
    return "boxplot"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = [10] * 100_000_000

def add_list(l):
    # TODO
    # Please use a for loop (not a built-in)
    total = 0
    for x in l:
        total += x
    return total

def q2a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    # Add the 3 pipelines.
    # (You will need to create a pipeline for each one.)
    # Pipeline names: small, medium, large
    # Generate a plot.
    # Save the plot as 'output/part2-q2a.png'.
    # TODO
    # Finally, return the throughputs as a list.
    import os
    import matplotlib.pyplot as plt
    os.makedirs("output", exist_ok=True)

    # Create helper
    h = ThroughputHelper()

    # Define three pipelines as functions
    def pipeline_small():
        add_list(LIST_SMALL)

    def pipeline_medium():
        add_list(LIST_MEDIUM)

    def pipeline_large():
        add_list(LIST_LARGE)

    # Add pipelines to helper
    h.add_pipeline("small", len(LIST_SMALL), pipeline_small)
    h.add_pipeline("medium", len(LIST_MEDIUM), pipeline_medium)
    h.add_pipeline("large", len(LIST_LARGE), pipeline_large)

    # Measure throughputs
    throughputs = h.compare_throughput()

    # Generate plot
    h.generate_plot("output/part2-q2a.png")

    return throughputs


"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===
The large list pipeline has the highest throughput according to the measured values just like I expected
Throughput is measured in items per second and since the large list has many items, the item processing time is averaged over a huge number of items, giving a higher throughput. 
The small list runs very quickly overall but has fewer items, so the measured throughput is lower in comparison.

=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)

    def compare_latency(self):
        # Measure the latency of all pipelines
        # and store it in a list in self.latencies.
        # Also, return the resulting list of latencies,
        # in **milliseconds.**
        import time
        self.latencies = []

        for func in self.pipelines:
            total_time = 0.0
            for _ in range(NUM_RUNS):
                start = time.time()
                func()
                end = time.time()
                total_time += (end - start)
            avg_time = total_time / NUM_RUNS
            self.latencies.append(avg_time * 1000)  # convert to ms
        return self.latencies

    def generate_plot(self, filename):
        # Generate a plot for latency using matplotlib.
        # You can use any plot you like, but a bar chart probably makes
        # the most sense.
        # Make sure you include a legend.
        # Save the result in the filename provided.
        import matplotlib.pyplot as plt
        plt.figure(figsize=(8,5))
        plt.bar(self.names, self.latencies, color='lightgreen')
        plt.ylabel("Latency (ms)")
        plt.xlabel("Pipeline")
        plt.title("Pipeline Latency Comparison")
        plt.savefig(filename)
        plt.close()

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    # Return the number of input items in each dataset,
    # for the latency helper to run correctly.
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    # Create a LatencyHelper object
    h = LatencyHelper()
    # Add the single pipeline three times.
    def single_item_pipeline():
        add_list(LIST_SINGLE_ITEM)
    h.add_pipeline("copy1", single_item_pipeline)
    h.add_pipeline("copy2", single_item_pipeline)
    h.add_pipeline("copy3", single_item_pipeline)

    # Measure latencies
    latencies = h.compare_latency()
    # Generate a plot.
    h.generate_plot("output/part2-q4a.png")
    # Save the plot as 'output/part2-q4a.png'.
    # Finally, return the latencies as a list.
    return latencies


"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===
The latency results: [0.000286102294921875, 0.00021457672119140625, 0.00030994415283203125]. 
I thought it would vary much more but the difference is only a miniscule amount.

=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

def q5a():
    # Return the throughput of the pipeline in part 1.
    import part1
    data = part1.load_input()
    h = ThroughputHelper()
    # PART_1_PIPELINE takes no arguments, so we just call it
    h.add_pipeline("part1_pipeline", len(data), lambda: part1.PART_1_PIPELINE())

    throughputs = h.compare_throughput()
    return throughputs[0]  # only one pipeline

def q5b():
    # Return the latency of the pipeline in part 1.
    import part1
    h = LatencyHelper()
    # PART_1_PIPELINE takes no arguments, so we just call it
    h.add_pipeline("part1_pipeline_latency", lambda: part1.PART_1_PIPELINE())

    latencies = h.compare_latency()
    return latencies[0]

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

def load_input(filename):
    # Return a dataframe containing the population data
    # **Clean the data here**
    # Load CSV
    df = pd.read_csv(filename)
    
    # Remove world and continents
    df = df[df['Code'] != 'OWID_WRL']  # drop world
    continents = ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
    df = df[~df['Entity'].isin(continents)]
    
    # Keep only necessary columns
    df = df[['Entity', 'Year', 'Population (historical)']]
    
    return df
    
def population_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    # Group by country to get min and max year
    grouped = df.groupby("Entity").agg(
        min_year=("Year", "min"),
        max_year=("Year", "max")
    )

    # Population at earliest year
    min_pop = df.loc[df.groupby("Entity")["Year"].idxmin(), ["Entity", "Population (historical)"]].set_index("Entity")
    grouped = grouped.join(min_pop.rename(columns={"Population (historical)": "min_pop"}))

    # Population at latest year
    max_pop = df.loc[df.groupby("Entity")["Year"].idxmax(), ["Entity", "Population (historical)"]].set_index("Entity")
    grouped = grouped.join(max_pop.rename(columns={"Population (historical)": "max_pop"}))

    # Keep only countries with multiple years
    grouped["years_diff"] = grouped["max_year"] - grouped["min_year"]
    grouped = grouped[grouped["years_diff"] > 0]

    # Compute yearly population growth
    grouped["pop_increase_per_year"] = (grouped["max_pop"] - grouped["min_pop"]) / grouped["years_diff"]

    # Compute summary statistics explicitly
    min_val = grouped["pop_increase_per_year"].min()
    median_val = grouped["pop_increase_per_year"].median()
    max_val = grouped["pop_increase_per_year"].max()
    mean_val = grouped["pop_increase_per_year"].mean()
    std_val = grouped["pop_increase_per_year"].std()

    return [min_val, median_val, max_val, mean_val, std_val]

def q6():
    # As your answer to this part,
    # call load_input() and then population_pipeline()
    # Return a list of min, median, max, mean, and standard deviation
    df = load_input("data/population.csv")
    return population_pipeline(df)

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

# Load full dataset
df = pd.read_csv("data/population.csv")

# Make sure the files exist and include headers
df.head(600).to_csv("data/population-small.csv", index=False)
df.head(6000).to_csv("data/population-medium.csv", index=False)
df.head(1).to_csv("data/population-single-row.csv", index=False)

def load_input_small():
    # Return a cleaned dataframe for the small dataset (600 rows)
    df = load_input("data/population-small.csv")
    return df

def load_input_medium():
    # Return a cleaned dataframe for the medium dataset (6000 rows)
    df = load_input("data/population-medium.csv")
    return df


def load_input_large():
    # Return a cleaned dataframe for the large dataset (full file)
    df = load_input("data/population.csv")
    return df

def load_input_single_row():
    # This is the pipeline we will use for latency.
    df = load_input("data/population-single-row.csv")
    return df

def q7():
    # Don't modify this part
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    # Run the population pipeline on the small dataset
    df = load_input_small()
    return population_pipeline(df)

def baseline_medium():
    # Run the population pipeline on the medium dataset
    df = load_input_medium()
    return population_pipeline(df)
    
def baseline_large():
    # Run the population pipeline on the large dataset
    df = load_input_large()
    return population_pipeline(df)
    
def baseline_latency():
    df = load_input_small().head(2)  # using first 2 rows as an example
    return population_pipeline(df)


def q8():
    # Don't modify this part
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

# Create the four DataFrame constants
POPULATION_SMALL = load_input_small()
POPULATION_MEDIUM = load_input_medium()
POPULATION_LARGE = load_input_large()
POPULATION_SINGLE_ROW = load_input_single_row()

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)
    
def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    df = POPULATION_SINGLE_ROW
    if len(df) == 1:
        df = pd.concat([df, df], ignore_index=True)
    return population_pipeline(df)

def q9a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in ouptut/q9a.png
    # Return list of 6 throughputs
    import os
    os.makedirs("output", exist_ok=True)

    h = ThroughputHelper()

    # Baseline pipelines (load from file)
    h.add_pipeline("baseline_small", len(load_input_small()), baseline_small)
    h.add_pipeline("baseline_medium", len(load_input_medium()), baseline_medium)
    h.add_pipeline("baseline_large", len(load_input_large()), baseline_large)

    # Fromvar pipelines (already in memory)
    h.add_pipeline("fromvar_small", len(POPULATION_SMALL), fromvar_small)
    h.add_pipeline("fromvar_medium", len(POPULATION_MEDIUM), fromvar_medium)
    h.add_pipeline("fromvar_large", len(POPULATION_LARGE), fromvar_large)

    # Compare throughput and plot
    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-q9a.png")

    return throughputs


def q9b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in ouptut/q9b.png
    # Return list of 2 latencies
    import os
    os.makedirs("output", exist_ok=True)

    h = LatencyHelper()

    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("fromvar_latency", fromvar_latency)

    latencies = h.compare_latency()
    h.generate_plot("output/part2-q9b.png")

    return latencies



 
"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====
The difference is noticeable but not huge. Pipelines using in-memory variables are a bit faster than those reading from files.
Latency differs more, especially for small datasets. File reading adds extra time for each run, so it affects latency more than throughput.
It shows that keeping data in memory is slightly faster than reading from files, but the biggest performance gains come from how the pipeline is written.
===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def for_loop_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation
    import numpy as np

    # Make sure we work on a copy
    df = df.copy()

    # Sort by country and year for consistent iteration
    df = df.sort_values(["Entity", "Year"])

    growth_rates = []
    current_country = None
    first_year = None
    first_pop = None
    last_year = None
    last_pop = None

    # Iterate through rows manually
    for _, row in df.iterrows():
        country = row["Entity"]
        year = row["Year"]
        pop = row["Population (historical)"]

        if country != current_country:
            # Save growth for the previous country
            if current_country is not None and last_year > first_year:
                growth = (last_pop - first_pop) / (last_year - first_year)
                growth_rates.append(growth)

            # Reset for new country
            current_country = country
            first_year = year
            first_pop = pop
            last_year = year
            last_pop = pop
        else:
            # Update latest year and population
            last_year = year
            last_pop = pop

    # Handle the last country
    if current_country is not None and last_year > first_year:
        growth = (last_pop - first_pop) / (last_year - first_year)
        growth_rates.append(growth)

    # Compute summary statistics manually
    min_val = float(np.min(growth_rates))
    median_val = float(np.median(growth_rates))
    max_val = float(np.max(growth_rates))
    mean_val = float(np.mean(growth_rates))
    std_val = float(np.std(growth_rates))

    return [min_val, median_val, max_val, mean_val, std_val]

def q11():
    # As your answer to this part, call load_input() and then
    # for_loop_pipeline() to return the 5 numbers.
    # (these should match the numbers you got in Q6.)
    df = load_input("data/population.csv")
    return for_loop_pipeline(df)

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    df = load_input_small()
    return for_loop_pipeline(df)

def for_loop_medium():
    df = load_input_medium()
    return for_loop_pipeline(df)
    
def for_loop_large():
    df = load_input_large()
    return for_loop_pipeline(df)

def for_loop_latency():
    df = load_input_single_row()
    # Duplicate the row if only one row exists
    if len(df) == 1:
        df = pd.concat([df, df], ignore_index=True)
        # Make the second row have a different year to avoid empty growth_rates
        df.loc[1, "Year"] += 1
    return for_loop_pipeline(df)

def q12():
    # Don't modify this part
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    # Add all 6 pipelines for a throughput comparison
    # Generate plot in ouptut/q13a.png
    # Return list of 6 throughputs
    import os
    os.makedirs("output", exist_ok=True)

    h = ThroughputHelper()

    # Baseline pipelines (vectorized)
    h.add_pipeline("baseline_small", len(load_input_small()), baseline_small)
    h.add_pipeline("baseline_medium", len(load_input_medium()), baseline_medium)
    h.add_pipeline("baseline_large", len(load_input_large()), baseline_large)

    # For-loop pipelines (non-vectorized)
    h.add_pipeline("for_loop_small", len(load_input_small()), for_loop_small)
    h.add_pipeline("for_loop_medium", len(load_input_medium()), for_loop_medium)
    h.add_pipeline("for_loop_large", len(load_input_large()), for_loop_large)

    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-q13a.png")

    return throughputs

def q13b():
    # Add 2 pipelines for a latency comparison
    # Generate plot in ouptut/q13b.png
    # Return list of 2 latencies
    import os
    os.makedirs("output", exist_ok=True)

    h = LatencyHelper()

    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("for_loop_latency", for_loop_latency)

    latencies = h.compare_latency()
    h.generate_plot("output/part2-q13b.png")

    return latencies

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====
From the throughput results, the baseline pipelines are consistently faster than the 
for-loop pipelines for all dataset sizes—small, medium, and large. This is expected because 
vectorized operations use  optimized implementations that process data in bulk, 
while for-loop implementations iterate element by element, which is slower in Python.
===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====
Similarly, the baseline pipeline shows lower latency than the for-loop pipeline. 
This means that even for a single run, the vectorized pipeline completes faster, confirming 
that vectorization improves both throughput and latency.
===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====
Performance gap grows with dataset size. 
The difference in throughput between baseline and for-loop pipelines increases as the dataset gets larger. 
For small datasets, the difference is noticeable but not too wide. For large datasets, the vectorized pipeline is significantly faster. 
This highlights how vectorized operations scale much better with data size.
===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====
The vectorized vs. for-loop factor had the biggest impact on performance. 
Across all dataset sizes, vectorized pipelines consistently achieved higher throughput and lower latency compared to for-loop pipelines. 
While the file vs. variable difference had some effect—loading from a variable is slightly faster than reading from a 
file—the performance gap was small.
===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====
The throughput tends to decrease as the input dataset size increases, but the rate of decrease depends on the pipeline type. 
For vectorized pipelines, throughput decreases only slightly with increasing dataset size, showing that vectorization scales efficiently. 
===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====
Throughput and latency appear to be inversely related through pipelines with higher throughput
tend to have lower latency, while pipelines with lower throughput have higher latency. 
This makes sense because higher throughput indicates that the pipeline can process more data per unit time, 
My hypothesis is: as throughput increases, latency decreases, and the opposite.
===== END OF Q17 ANSWER =====
"""

"""
===== Extra Credit =====

This part is optional.

Use your pipeline to compare something else!

Here are some ideas for what to try:
- the cost of random sampling vs. the cost of getting rows from the
  DataFrame manually
- the cost of cloning a DataFrame
- the cost of sorting a DataFrame prior to doing a computation
- the cost of using different encodings (like one-hot encoding)
  and encodings for null values
- the cost of querying via Pandas methods vs querying via SQL
  For this part: you would want to use something like
  pandasql that can run SQL queries on Pandas data frames. See:
  https://stackoverflow.com/a/45866311/2038713

As your answer to this part,
as before, return
a. the list of 6 throughputs
and
b. the list of 2 latencies.

and generate plots for each of these in the following files:
    output/part2-ec-a.png
    output/part2-ec-b.png
"""

# Extra credit (optional)

def extra_credit_a():
    raise NotImplementedError

def extra_credit_b():
    raise NotImplementedError

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
