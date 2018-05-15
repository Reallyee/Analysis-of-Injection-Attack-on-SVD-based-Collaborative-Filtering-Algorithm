from collections import OrderedDict
import os
import codecs
import glob
import numpy as np
import re


# read file
'''
movie is the dictionary of the all the movie information
the format is :
{movie_id : [ [customer_id, ranking, date]]} 
'''
def read_files():
        all_information = np.zeros((5, 943, 1682))
        os.getcwd()
        os.chdir("/media/mint/mint/Differential_Privacy/data/train")
        pattern = re.compile(r'\d+') #find numbers
        files = glob.glob('*.txt')
        index = 0
        for filename in files:
                f = codecs.open(filename, 'r', encoding='utf-8')
                for line in f:
                        information = pattern.findall(line)
                        all_information[index][int(information[0])-1][int(information[1])-1]=int(information[2])
                index += 1
        return all_information


