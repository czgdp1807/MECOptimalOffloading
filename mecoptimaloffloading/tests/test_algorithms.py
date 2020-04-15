from mecoptimaloffloading.algorithms.bi_search import bi_search
from mecoptimaloffloading.algorithms.utils import *
import math, random, matplotlib.pyplot as plt

def energy_time(config):
    local_energy = energy_consumption_local(config['L'][1], config['f'][1], config['_k'])
    t1_data_rate = uplink_data_rate(config['p'][1], config['h'][1],
                                    config['W'], config['sigma'])
    t1_up_times = offloading_transmission_time(config['O'][1], t1_data_rate)
    t1_data_rate = downlink_data_rate(config['p'][1], config['g'][1],
                                        config['W'], config['sigma'])
    t1_down_times = downloading_transmission_time(config['O'][1], t1_data_rate)
    offloading_enrgy = offloading_transmission_energy(config['p'][1], t1_up_times)
    energy_device_1 = energy_consumption_device_1(local_energy, offloading_enrgy, config['a'][1])
    local_times = exec_time_local(config['L'][1], config['f'][1])
    edge_times = exec_time_edge(config['L'][1], config['fc'])
    total_comp_time_1 = computation_time_device_1(local_times, edge_times, config['a'][1])
    trans_times = transmission_time_device_1(t1_up_times, t1_down_times, config['a'][1])
    total_time_device_1 = total_comp_time_1 + trans_times
    local_energy = energy_consumption_local(config['L'][2], config['f'][2], config['_k'])
    t2_data_rate = uplink_data_rate(config['p'][2], config['h'][2],
                                    config['W'], config['sigma'])
    t2_up_times = offloading_transmission_time(config['O'][2], t2_data_rate)
    t2_data_rate = downlink_data_rate(config['p'][2], config['g'][2],
                                        config['W'], config['sigma'])
    t2_down_times = downloading_transmission_time(config['O'][2], t2_data_rate)
    offloading_energy = offloading_transmission_energy(config['p'][2], t2_up_times)
    energy_device_2 = energy_consumption_device_2(local_energy, offloading_energy, config['a'][2])
    local_times = exec_time_local(config['L'][2], config['f'][2])
    edge_times = exec_time_edge(config['L'][2], config['fc'])
    total_comp_time_2 = computation_time_device_1(local_times, edge_times, config['a'][2])
    trans_times = transmission_time_device_1(t2_up_times, t2_down_times, config['a'][2])
    total_time_device_2 = total_comp_time_2 + trans_times
    return energy_device_1, energy_device_2, total_time_device_1, total_time_device_2


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

test_bi_search()
