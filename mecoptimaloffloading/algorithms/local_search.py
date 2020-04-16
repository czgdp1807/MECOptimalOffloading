from mecoptimaloffloading.algorithms.bi_search import bi_search
from mecoptimaloffloading.algorithms.utils import eta, energy_time
import random, copy

def update(config, i, j):
    config['a'][1][i] = 1 - config['a'][1][i]
    config['a'][2][j] = 1 - config['a'][2][j]

def local_search(config, max_iters=10):
    M = config['M'] + 2
    N = config['N'] + 2
    config['a'] = {1: [random.randint(0, 1)
                      for _ in range(M)],
                   2: [random.randint(0, 1)
                      for _ in range(N)]}
    bi_search(config)
    E1, E2, T1, T2 = energy_time(config)
    ETA1, ETA2 = eta(E1, T1, config['beta1_e']), \
                    eta(E2, T2, config['beta2_e'])
    for itr in range(max_iters):
        print(itr, config['a'], ETA1, ETA2)
        for i in range(M):
            flag2 = True
            for j in range(N):
                if not flag2:
                    break
                curr_a = copy.deepcopy(config['a'])
                update(config, i, j)
                try:
                    bi_search(config)
                except TypeError:
                    curr_a = copy.deepcopy(config['a'])
                    continue
                _E1, _E2, _T1, _T2 = energy_time(config)
                _ETA1, _ETA2 = eta(_E1, _T1, config['beta1_e']), \
                                eta(_E2, _T2, config['beta2_e'])
                if _ETA1 + _ETA2 <= ETA1 + ETA2:
                    ETA1, ETA2 = _ETA1, _ETA2
                    flag2 = False
                else:
                    config['a'] = copy.deepcopy(curr_a)
    return ETA1, ETA2
