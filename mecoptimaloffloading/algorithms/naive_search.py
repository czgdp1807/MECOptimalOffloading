from mecoptimaloffloading.algorithms.bi_search import bi_search
from mecoptimaloffloading.algorithms.utils import eta, energy_time
import random, math, copy

def update(config, i):
    def list2list(l):
        s = ""
        for el in l:
            s += str(el)
        num = int(s, 2) + 1
        new_str = '{0:b}'.format(num)
        new_str = ((config['M'] if i == 1 else config['N']) - len(new_str) + 2)*'0' + \
                    new_str
        return [int(c) for c in new_str]
    config['a'][i] = list2list(config['a'][i])

def naive_search(config):
    M = config['M'] + 2
    N = config['N'] + 2
    config['a'] = {1: [0 for _ in range(M)],
                   2: [0 for _ in range(N)]}
    opt_a = None
    ETA1, ETA2 = math.inf, math.inf
    itr = 0
    for _ in range(2**M):
        config['a'][2] = [0 for _ in range(N)]
        for _ in range(2**N):
            print(itr)
            try:
                bi_search(config)
            except TypeError:
                itr += 1
                update(config, 2)
                continue
            _E1, _E2, _T1, _T2 = energy_time(config)
            _ETA1, _ETA2 = eta(_E1, _T1, config['beta1_e']), \
                            eta(_E2, _T2, config['beta2_e'])
            if _ETA1 + _ETA2 <= ETA1 + ETA2:
                ETA1, ETA2 = _ETA1, _ETA2
                opt_a = copy.deepcopy(config['a'])
            itr += 1
            update(config, 2)
        update(config, 1)
    config['a'] = copy.deepcopy(opt_a)
    return ETA1, ETA2
