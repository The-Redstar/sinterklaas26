
import opensimplex
import numpy as np

def gen():
    opensimplex.random_seed()
    return list(map(float,opensimplex.noise2array(np.arange(0,50,0.050)*1.5,np.array([0])).tolist()[0]))

