'''
Project     : Replacement Policy Simulation
File name   : fileparser.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the functionality to 
              parse input files
'''

import sys

def Parse(filename):

    try:
        file = open(filename, "r")
    except:
        raise Exception("Unable to open " + filename)

    file_data = file.readlines()

    input_data = []

    for line in file_data:
        line = line.strip()
        if (line == '\n' or line == ''):
            continue
        
        try:
            line = int(line)
        except:
            print('Memory files can only contain integers')
            sys.exit()

        input_data.append(line)

    return input_data