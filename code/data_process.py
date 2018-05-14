'''
center, stablize and clamp ratings
generate Covariance Matrix (uncompleted)
'''
import numpy as np

# Movie Effects
def getMAvg(df):
    GSum = np.sum(df)
    GCnt = np.count_nonzero(df)
    G = GSum/GCnt

    beta = 0.1
    MSum = np.sum(df,axis=0) #the number of ratings for each movie
    MCnt = np.count_nonzero(df,axis=0)
    # produce a stabilized per-movie average rating
    MAvg = (MSum + beta*G)/(MCnt + beta)
    return MAvg

# User Effects
def getUAvg(df,MAvg):
    GSum = np.sum(df)
    GCnt = np.count_nonzero(df)
    G = GSum/GCnt

    beta = 0.01
    USum = np.sum(df-MAvg,axis=1) + beta*G
    c_u = np.count_nonzero(df,axis=1) #the number of movies for each user
    UAvg = USum/(c_u + beta)
    return UAvg

def clamp(df,UAvg,bound):
    #lower the sensitivity of the measurements
    df_hat = (df.transpose()-UAvg).transpose()
    df_hat[ df_hat < -bound ] = -bound
    df_hat[ df_hat > bound ] = bound
    return df_hat


'''
Demo for how to use it:

1. dfs = read_files()
2. df = dfs[0]
   MAvg = getMAvg(df)
   UAvg = getUAvg(df,MAvg)
3. cdf = clamp(df,UAvg,0.09)

'''