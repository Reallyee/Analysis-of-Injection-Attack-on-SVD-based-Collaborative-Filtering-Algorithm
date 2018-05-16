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
	mean = []
	bu = np.zeros((5, 943))
	bi = np.zeros((5, 1682))
	all_information = np.zeros((5, 943, 1682))
	os.getcwd()
	os.chdir("/media/mint/mint/Differential_Privacy/data/train")
	pattern = re.compile(r'\d+') #find numbers
	files = glob.glob('*.txt')
	index = 0
	for filename in files:
		line_number = 0
		mean_value = 0
		f = codecs.open(filename, 'r', encoding='utf-8')
		for line in f:
			information = pattern.findall(line)
			# information 0 user 1 item 2 rank
			all_information[index][int(information[0])-1][int(information[1])-1]=int(information[2])
			mean_value += int(information[2])
			line_number += 1
			bu[index][int(information[0])-1] += int(information[2])
			bi[index][int(information[1])-1] += int(information[2])
		mean.append(mean_value/line_number)
		for elem in range(1, bu.shape[1]+1):
			bu[index][elem] = bu[index][elem]/bu.shape[1]-mean_value
		for elem in range(1, bi.shape[1]+1):
			bi[index][elem] = bi[index][elem]/bi.shape[1]-mean_value
		index += 1
	return all_information, mean, bi, bu


def train(matrix_rank, eta, mu, iteration_time):
	MaxRate = 5
	MinRate = 1
    information, mean, bi, bu = read_file.read_files()
#     the range of the rank is [1,5]
    p = np.random.rand(bi.shape[1], matrix_rank)/10
    q = np.random.rand(matrix_rank, bi.shape[1])/10
    train_number = 0
	rui = 0
    for iterator in iteration_time:
        Rmse = 0
		nRateNum = 0
        for user in range(0, bu.shape[1]):
			for item in range(0, bi.shape[1]):
				if(information[train_number][user][item] != 0)
					rui = mean[train_number]+bu[user]+bi[item]+np.inner(p[user], q[:,item])
					if rui> MaxRate:
						rui = MaxRate
					if rui < MinRate:
						rui = MinRate
					e = information[train_number][user][item]-rui
					bu[user] += eta*(e-mu*bu[user])
					bi[item] += eta*(e-mu*bi[item])
					for rank in range(0, maxtirx_rank):
						p[user][rank] = eta*(e*q[rank][item]-mu*p[user][rank])
						q[rank][item] = eta*(e*p[user][rank]-mu*q[rank][item])
					Rmse += e*e
					nRateNum += 1
		Rmse = np.sqrt(Rmse/nRateNum)
		if Rmse>mLastRmse:
			break;
		mLastRmse = Rmse
		eta *= 0.9

        
        

    



