import numpy as np

def FourierMatrix(n):
    a = np.array(np.arange(n), ndmin=2)
    return np.exp(2j*np.pi/n*a.T*a)
