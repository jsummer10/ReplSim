# Replacement Policy Simulation

# 1 Overview 

## Memory Input

Memory can either be read from a file or a randomly generated memory file. This randomly generated memory file can also be saved for later use

## Output

Data will be saved to an excel workbook in the output folder

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
