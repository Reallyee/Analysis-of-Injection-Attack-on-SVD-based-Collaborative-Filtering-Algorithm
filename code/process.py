from collections import OrderedDict
import os
import codecs
import glob
import numpy as np
import re
import copy as cp
import queue 


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
	test_information = np.zeros((5, 943, 1682))
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
		mean.append(mean_value/line_number)
		for user in range(0, all_information.shape[1]):
			user_mean_value=0
			item_number = 0
			for item in range(0, all_information.shape[2]):
				if all_information[index][user][item] != 0:
					user_mean_value += all_information[index][user][item]
					item_number += 1
			if item_number != 0:
				bu[index][user]  = user_mean_value/item_number-mean[index]
		for item in range(0, all_information.shape[2]):
			item_mean_value = 0
			user_number = 0
			for user in range(0, all_information.shape[1]):
				if all_information[index][user][item] != 0:
					item_mean_value += all_information[index][user][item]
					user_number += 1
			if user_number != 0:
				bi[index][item] = item_mean_value/user_number-mean[index]
		index += 1
	os.getcwd()
	os.chdir("/media/mint/mint/Differential_Privacy/data/test")
	pattern = re.compile(r'\d+') #find numbers
	files = glob.glob('*.test')
	index = 0
	for filename in files:
		line_number = 0
		mean_value = 0
		f = codecs.open(filename, 'r', encoding='utf-8')
		for line in f:
			information = pattern.findall(line)
			# information 0 user 1 item 2 rank
			test_information[index][int(information[0])-1][int(information[1])-1]=int(information[2])
	return all_information, mean, bi, bu, test_information


def train(matrix_rank, eta, mu, iteration_time):
	MaxRate = 5
	MinRate = 1
	information, mean, bi, bu, test_information = read_files()
#     the range of the rank is [1,5]
	p = np.random.rand(bi.shape[1], matrix_rank)
	q = np.random.rand(matrix_rank, bi.shape[1])
	new_information = np.zeros((5, 943, 1682))
	train_number = 0
	rui = 0
	for iterator in range(0, iteration_time):
		Rmse = 0
		mLastRmse = 100000
		nRateNum = 0
		for user in range(0, bu.shape[1]):
			for item in range(0, bi.shape[1]):
				rui = mean[train_number]+bu[train_number][user]+bi[train_number][item]+np.inner(p[user], q[:,item])
				if rui> MaxRate:
					rui = MaxRate
				if rui < MinRate:
					rui = MinRate
				e = information[train_number][user][item]-rui
				bu[train_number][user] += eta*(e-mu*bu[train_number][user])
				bi[train_number][item] += eta*(e-mu*bi[train_number][item])
				for rank in range(0, matrix_rank):
					p[user][rank] = eta*(e*q[rank][item]-mu*p[user][rank])
					q[rank][item] = eta*(e*p[user][rank]-mu*q[rank][item])
				Rmse += e*e
				nRateNum += 1
				new_information[train_number][user][item] =  mean[train_number]+bu[train_number][user]+bi[train_number][item]+np.inner(p[user], q[:,item])			
		Rmse = np.sqrt(Rmse/nRateNum)
		if Rmse>mLastRmse:
			break;
		mLastRmse = Rmse
		eta *= 0.9
		# print("iterator:", iterator,  "       Rmse:", Rmse)
		# test 
		test_number = 0
		error = 0
		for user in range(0, test_information.shape[1]):
			for item in range(0, test_information.shape[2]):
				e = 0
				if test_information[train_number][user][item] != 0:
					e = test_information[train_number][user][item]-new_information[train_number][user][item]
					error += e*e
					test_number += 1
		sse = error
		# print("mse :", np.sqrt(error/test_number))
		# print("sse :", sse)
		# print("iterator:", iterator,  "       Rmse:", Rmse, "    mse :", np.sqrt(error/test_number), "    sse :", sse)
		# print(iterator, "&",format(Rmse, '.4f'),"&", format(np.sqrt(error/test_number), '.4f'), "&",format(sse, '.4f'),"\\\ \hline ")
		predict, amount = test_train(new_information, test_information)
		print("predict accuracy is :" ,predict/amount)
	


def train_with_noise(matrix_rank, eta, mu, iteration_time):
	MaxRate = 5
	MinRate = 1
	train_number = 0
	information, mean, bi, bu, test_information = read_files()
	noisy_information = cp.deepcopy(information)
	noisy_information[train_number] = information[train_number] + np.random.laplace(scale=0.1)
#     the range of the rank is [1,5]
	p = np.random.rand(bi.shape[1], matrix_rank)
	q = np.random.rand(matrix_rank, bi.shape[1])
	new_information = np.zeros((5, 943, 1682))
	rui = 0
	for iterator in range(0, iteration_time):
		Rmse = 0
		mLastRmse = 100000
		nRateNum = 0
		for user in range(0, bu.shape[1]):
			for item in range(0, bi.shape[1]):
				# if information[train_number][user][item] != 0:
				rui = mean[train_number]+bu[train_number][user]+bi[train_number][item]+np.inner(p[user], q[:,item])
				if rui> MaxRate:
					rui = MaxRate
				if rui < MinRate:
					rui = MinRate
				e = noisy_information[train_number][user][item]-rui
				bu[train_number][user] += eta*(e-mu*bu[train_number][user])
				bi[train_number][item] += eta*(e-mu*bi[train_number][item])
				for rank in range(0, matrix_rank):
					p[user][rank] = eta*(e*q[rank][item]-mu*p[user][rank])
					q[rank][item] = eta*(e*p[user][rank]-mu*q[rank][item])
				Rmse += e*e
				nRateNum += 1
				new_information[train_number][user][item] =  mean[train_number]+bu[train_number][user]+bi[train_number][item]+np.inner(p[user], q[:,item])			
		Rmse = np.sqrt(Rmse/nRateNum)
		if Rmse>mLastRmse:
			break;
		mLastRmse = Rmse
		eta *= 0.9
		
		# test 
		test_number = 0
		error = 0
		for user in range(0, test_information.shape[1]):
			for item in range(0, test_information.shape[2]):
				e = 0
				if test_information[train_number][user][item] != 0:
					e = test_information[train_number][user][item]-new_information[train_number][user][item]
					error += e*e
					test_number += 1
		sse = error
		# print("iterator:", iterator,  "       Rmse:", Rmse, "    mse :", np.sqrt(error/test_number), "    sse :", sse)
		# print(iterator, "&",format(Rmse, '.4f'),"&", format(np.sqrt(error/test_number), '.4f'), "&",format(sse, '.4f'),"\\\ \hline ")
		predict, amount = test_train(new_information, test_information)
		print("predict accuracy is :" ,predict/amount)
		
		


def test_train(new_information, test_information):
	train_number = 0
	N_number = 5
	predict_number = 0
	amount = 0
	for user in range(0, test_information.shape[1]):
		top_n_predict = []
		top_n_real = []
		index = 0
		min_predict = 6
		min_user_predict = 0
		min_item_predict = 0
		min_real = 6
		min_user_real = 0
		min_item_real = 0
		for item in range(0, test_information.shape[2]):
			if test_information[train_number][user][item] != 0:
				if index == 0:
					min_predict = new_information[train_number][user][item]
					min_user_predict = user
					min_item_predict = item
					min_real = test_information[train_number][user][item]
					min_user_real = user
					min_item_real = item
				if index<N_number:
					top_n_real.append((user, item))
					top_n_predict.append((user, item))
					if test_information[train_number][user][item]<min_real:
						min_real = test_information[train_number][user][item]
						min_user_real = user
						min_item_real = item
					if new_information[train_number][user][item]<min_predict:
						min_predict = new_information[train_number][user][item]
						min_user_predict = user
						min_item_predict = item
					index += 1
				else:
					if test_information[train_number][user][item]>min_real:
						top_n_real.remove((min_user_real, min_item_real))
						min_real = test_information[train_number][user][item]
						min_user_real = user
						min_item_real = item
						top_n_real.append((user, item))
						for elem in range(0, len(top_n_real)):
							if test_information[train_number][top_n_real[elem][0]][top_n_real[elem][1]]<min_real:
								min_real = test_information[train_number][top_n_real[elem][0]][top_n_real[elem][1]]
								min_user_real = top_n_real[elem][0]
								min_item_real = top_n_real[elem][1]
					if new_information[train_number][user][item]>min_predict:
						top_n_predict.remove((min_user_predict, min_item_predict))
						min_predict = new_information[train_number][user][item]
						min_user_predict = user
						min_item_predict = item
						top_n_predict.append((user, item))
						for elem in range(0, len(top_n_predict)):
							if new_information[train_number][top_n_predict[elem][0]][top_n_predict[elem][1]]<min_predict:
								min_predict = new_information[train_number][top_n_predict[elem][0]][top_n_predict[elem][1]]
								min_user_predict = top_n_predict[elem][0]
								min_item_predict = top_n_predict[elem][1]
		print("--------------predition----------------")
		print(top_n_predict)
		for elem in top_n_real:
			print(new_information[train_number][0][1])
		print(top_n_real)
		for elem in top_n_real:
			print(test_information[train_number][0][1])
		for elem in top_n_predict:
			if elem in top_n_real:
				predict_number += 1
		amount += 5
	return predict_number, amount








print("----------------train orginal data----------------------")
train(600, 0.1, 0.01, 10)
print("----------------train data with noise-------------------")
train_with_noise(600, 0.1, 0.01, 10)

        
        

    



