# Replacement Policy Simulation

# 1 Overview 

## Dependencies

The following dependencies will need to be installed

``` 
pip3 install xlsxwriter plotly
```

## Configuration

Memory can be...

- Read from a file
- Randomly generated

The memory and cache sizes can be configured in src/config.py. 

The simulations that will be ran can be changed in src/simulation.py. This file will allow you to add/remove simulations along with change the replacement policy and the set associativity.

## Output

Data will be saved to an excel workbook and a graph demonstrating the hit ratio. These will be located in the output folder

## Supported Replacement Policies

- LRU: Least Recently Used
	- Discards the least recently used items first.
- RR: Random Replacement
	- Randomly chooses which item to discard
- LFRU: Least Frequently Recently Used
	- Replaces an item with the least usage and the least recently used
- LFU: Least Frequently Used
	- Replaces an item with the least usage

# 2 Running

Run with 

```
python3 run.py 
```

# Authors

* Jake Summerville
* Henry Lee
* Martin Lopez
* Fausto Sanchez
