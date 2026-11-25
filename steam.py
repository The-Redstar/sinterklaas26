
import opensimplex
import numpy as np

def gen(t=50):
    opensimplex.random_seed()
    return list(map(float,opensimplex.noise2array(np.arange(0,t,0.050)*1.5,np.array([0])).tolist()[0]))

