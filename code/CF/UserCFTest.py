import numpy as np
import math
from operator import itemgetter
import os
import codecs
import glob
import re
import time

# read file
def read_files():
    all_information = np.zeros((5, 944, 1683))
    os.getcwd()
    os.chdir("/Users/audrey/Documents/GitHub/Differential-Privacy/data/train")
    '''
    movie is the dictionary of the all the movie information
    the format is :
    {movie_id : [ [customer_id, ranking, date]]} 
    '''
    pattern = re.compile(r'\d+') #find numbers
    files = glob.glob('*.txt')

    index = 0
    for filename in files:
        f = codecs.open(filename, 'r', encoding='utf-8')
        for line in f:
                information = pattern.findall(line)
                all_information[index][int(information[0])][int(information[1])]=int(information[2])
        index += 1

    return all_information

def UserSimilarity(train):
    mov_user = train.transpose()
    
    #caculate co-rated movies
    co = {}
    for i in range(np.shape(mov_user)[0]):
        #users who rate the same movie
        users = np.where(mov_user[i]>0)[0]
        for u in users:
            #print(type(u))
            if u not in co:
                co[u] = {}
            for v in users:
                if u==v:
                    continue;
                if(v not in co[u]):
                    co[u][v] = 0
                #the num of movies co-rated by u and v
                co[u][v] += 1
                
    #caculate similarity matrix user_sim
    user_sim = {}
    for u, co_u in co.items():
        if u not in user_sim:
            user_sim[u] = {}
        for v, times in co_u.items():
            u_len = np.count_nonzero(train[u,:])
            v_len = np.count_nonzero(train[v,:])
            user_sim[u][v] = times/math.sqrt( u_len * v_len )
            
    return user_sim

def Recommend(u,train,user_sim):
#   Find K similar users and recommend N movies for user
    k = 10
    n = 5
    
    rank = {}

    if np.count_nonzero(train[u]) == 0:
        print('User ',u,' has not rate any movie')
        return

    m_u = np.where(train[u]>0)[0]
    for v, sim in sorted(user_sim[u].items(), key=itemgetter(1), reverse=True)[0:k]:
#         print("top k: u",v)
        m_v = np.where(train[v,:]>0)[0]
        for m in m_v:
            if m in m_u:
                continue;
            if m not in rank:
                rank[m]=0
            rank[m] += sim*train[v,m]
#     print("rank",rank)
    return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:n]

if __name__ == '__main__':
    t1 = time.time()



    dfs = read_files()
    train = dfs[0]
    user_sim = UserSimilarity(train)

    print(type(Recommend(2,train,user_sim)))
    # for u in range(np.shape(train)[0]):
	 #    rec = Recommend(u,train,user_sim)
	 #    print("rec for User ",u,' ',rec)

    print('Elapsed time ', time.time()-t1, 's')