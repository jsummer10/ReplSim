# Replacement Policy Simulation

# 1 Overview 

## Dependencies

The following dependencies will need to be installed

``` 
pip3 install xlsxwriter plotly argparse openpyxl pandas tensorflow sklearn
```

## Configuration

Memory can be...

- Read from a file
- Randomly generated

The simulations that will be ran can be changed in src/simulation.py in the SimConfig function. This file will allow you to add/remove simulations along with change the replacement policy and the set associativity. The title value will be applied to the final graph of the data.

``` python 
def SimConfig(self):
	self.sim_configs = []

	self.title = '2-Way Set Associative Replacement Policy Comparison (' + self.mem_pattern + ')'

	self.sim_configs.append(Cache(config_name='LRU Cache (2-way)',   repl='LRU',     ways=2))
	self.sim_configs.append(Cache(config_name='RR Cache (2-way)',    repl='RR',      ways=2))
	self.sim_configs.append(Cache(config_name='LFRU Cache (2-way)',  repl='LFRU',    ways=2))
	self.sim_configs.append(Cache(config_name='LFU Cache (2-way)',   repl='LFU',     ways=2))
	self.sim_configs.append(Cache(config_name='FIFO Cache (2-way)',  repl='FIFO',    ways=2))
	self.sim_configs.append(Cache(config_name='MRU Cache (2-way)',   repl='MRU',     ways=2))
```

## Output

Data will be saved to an excel workbook and a graph demonstrating the hit ratio. These will be located in the output folder

## Supported Replacement Policies

### Standard Replacement Policies

- LRU: Least Recently Used
    - Discards the least recently used items first.
- MRU: Most Recently Used
    - Discards the most recently used items first.
- RR: Random Replacement
    - Randomly chooses which item to discard
- LFRU: Least Frequently Recently Used
    - Replaces an item with the least usage and the least recently used
- LFU: Least Frequently Used
    - Replaces an item with the least usage
- FIFO: First On First Out
    - Replace the item that was added first with no regard to its usage

### Custom Replacement Policies

- LRUML: Least Recently Used with Machine Learning
	- Discards the least recently used items first with machine learning checks and optimizations

# 2 Running

## Command Line Arguments

| Long         | Description                                                |
|--------------|------------------------------------------------------------|
| --file       | Input file containing memory addresses                     |
| --memsize    | Size of memory file to be generated                        |
| --memrange   | Max memory value to be generated                           |
| --mempattern | The memory pattern to be used (normal, loops, rep, random) |
| --cachesize  | Size of the cache                                          |
| --linesize   | Size of the cache line                                     |
| --mult       | Run simulation a specified number of times                 |
| --test       | Test the simulators functionality                          |
      
All arguments are optional. `memsize`, `memrange`, and `mempattern` are used when auto generating a memory file. `file` is used to read in a memory file. `memsize`, `memrange`, and `mempattern` can't be used with `file`. 

When running `mult`, specify a positive integer. This setting cannot be used with `file`. Each new sim will generate a completely new memory file to use.

Generated memory files can follow four patterns:

- Normal: A combination of random addresses, loops, and repetition
- Random: Completely random memory addresses
- Loops: A heavy amount of loops with some random addresses and repetition
- Repetitive: A heavy amount of repetition with some loops and random addresses 

## Examples

Running with a memory file

```
python3 run.py -f mem/sample_mem.txt 
```

Running with auto generated memory

```
python3 run.py --memsize 2000 --memrange 2000 --mempattern normal
```

Running with a configured cache

```
python3 run.py --cachesize 64KB --linesize 32B
```

Running multiple simulations

```
python3 run.py --mult 3
```


# Authors

* Jake Summerville
* Henry Lee
* Martin Lopez
* Fausto Sanchez
