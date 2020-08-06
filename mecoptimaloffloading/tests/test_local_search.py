from mecoptimaloffloading.algorithms.local_search import local_search
from mecoptimaloffloading.algorithms.utils import energy_time
import math, random

def test_local_search():
    h_func = lambda d: 4.11*((3*10**8)/(4*math.pi*915*10**6*d))**3
    d = {1: 15, 2: 15}
    M, N = 3, 5
    config = {  'L': {1: [0, 65.5*10**6, 40.3*10**6, 96.6*10**6, 0],
                    2: [0, 70.8*10**6, 95.3*10**6, 86.4*10**6, 18.6*10**6, 158.6*10**6, 0]},
                'P': {1: 0.1, 2: 0.1},
                'fc': 10**10,
                'f_peak': 10**8,
                '_k': 10**(-26),
                'k': 4,
                'h': {1: [h_func(d[1]) for _ in range(M+2)],
                     2: [h_func(d[2]) for _ in range(N+2)]},
                'g': {1: [h_func(d[1]) for _ in range(M+2)],
                     2: [h_func(d[2]) for _ in range(N+2)]},
                'sigma': 10**(-5),
                'W': 2*10**6,
                'M': M,
                'N': N,
                'p': {1: [], 2: []},
                'f': {1: [], 2: []},
                'O': {1: [1500*8192, 1000*8192, 1600*8192, 1000*8192, 0],
                      2: [2000*8192, 1500*8192, 1000*8192, 1400*8192, 1500*8192, 1000*8192, 0]}}
    config['beta1_t'] = 0.085
    config['beta1_e'] = 1 - 0.085
    config['beta2_t'] = 0.1
    config['beta2_e'] = 0.9
    ETA1, ETA2 = local_search(config, max_iters=5)
    print(config['a'], ETA1, ETA2)

flag = True
while flag:
    try:
        test_local_search()
        flag = False
    except TypeError:
        continue
