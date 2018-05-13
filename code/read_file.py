from collections import OrderedDict
import os
import codecs
import glob
import numpy


# read file
os.getcwd()
os.chdir("/home/mint/PycharmProjects/Differential_Privacy/download/training_set")
'''
movie is the dictionary of the all the movie information
the format is :
{movie_id : [ [customer_id, ranking, date]]} 
'''
movie = OrderedDict()
files = glob.glob('*.txt')
file_list = codecs.open('all.txt', 'a')
for filename in files:
    f = codecs.open(filename, 'r', encoding='utf-8')
    index = 0
    for line in f:
        if index == 0:
            movie_id = line.split(':')[0]
            movie_dict = []
            index += 1
        elif index > 0:
            information = []
            customer_id = line.split(',')[0]
            information.append(customer_id)
            ranking = int(line.split(',')[1])
            information.append(ranking)
            date = line.split(',')[2]
            information.append(date[0:10])
            movie_dict.append(information)
            index += 1
    movie[movie_id] = movie_dict

print(movie)


