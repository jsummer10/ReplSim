'''
Project     : Replacement Policy Simulation
File name   : fileparser.py
Authors     : Jake Summerville, Henry Lee, 
              Martin Lopez, Fausto Sanchez
Creation    : 04/17/21
Description : The file contains the functionality to 
              parse input files
'''

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
        
        input_data.append(line)

    return input_data