from mecoptimaloffloading.algorithms.bi_search import bi_search
from mecoptimaloffloading.algorithms.utils import energy_time
import math, random, matplotlib.pyplot as plt

def test_bi_search():
    random.seed(0)
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
                'a': {1: [random.randint(0, 1) for _ in range(M+2)],
                      2: [random.randint(0, 1) for  _ in range(N+2)]},
                'M': M,
                'N': N,
                'p': {1: [], 2: []},
                'f': {1: [], 2: []},
                'O': {1: [1500*8192, 1000*8192, 1600*8192, 1000*8192, 0],
                      2: [2000*8192, 1500*8192, 1000*8192, 1400*8192, 1500*8192, 1000*8192, 0]}}
    config['beta1_t'] = 0.085
    config['beta1_e'] = 1 - 0.085
    b2_t = 0.1
    energies_1, times_1 = [], []
    energies_2, times_2 = [], []
    for _ in range(80):
        config['beta2_t'] = b2_t
        config['beta2_e'] = 1 - b2_t
        b2_t += 0.01
        bi_search(config)
        e1, e2, t1, t2 = energy_time(config)
        energies_1.append(e1)
        energies_2.append(e2)
        times_1.append(t1)
        times_2.append(t2)
    line1, = plt.plot(times_1, energies_1, label='WD1', linewidth=1)
    line2, = plt.plot(times_2, energies_2, label='WD2', linewidth=1)
    plt.legend(handles=[line1, line2])
    plt.xlabel("T/s")
    plt.ylabel("E/J")
    filename = 'beta1_t' + "_".join(str(config['beta1_t']).split('.')) + ".png"
    plt.savefig("./mecoptimaloffloading/results/bi_search/" + filename)

flag = True
while flag:
    try:
        test_bi_search()
        flag = False
    except TypeError:
        continue
