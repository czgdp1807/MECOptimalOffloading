from mecoptimaloffloading.algorithms.utils import *

__all__ = [
    'bi_search'
]

def wait_times(config):
    t1_local_times = exec_time_local(config['L'][1], config['f'][1])
    t1_edge_times = exec_time_edge(config['L'][1], config['fc'])
    t1_data_rate = uplink_data_rate(config['p'][1], config['h'][1],
                                    config['W'], config['sigma'])
    t1_up_times = offloading_transmission_time(config['O'][1], t1_data_rate)
    t1_data_rate = downlink_data_rate(config['p'][1], config['g'][1],
                                    config['W'], config['sigma'])
    t1_down_times = downloading_transmission_time(config['O'][1], t1_data_rate)
    t2_local_times = exec_time_local(config['L'][2], config['f'][2])
    t2_edge_times = exec_time_edge(config['L'][2], config['fc'])
    t2_data_rate = uplink_data_rate(config['p'][2], config['h'][2],
                                    config['W'], config['sigma'])
    t2_up_times = offloading_transmission_time(config['O'][2], t2_data_rate)
    t2_data_rate = downlink_data_rate(config['p'][2], config['g'][2],
                                    config['W'], config['sigma'])
    t2_down_times = downloading_transmission_time(config['O'][2], t2_data_rate)
    k = config['k']
    res1 = wait_time_device_1(t1_local_times, t1_edge_times, t1_up_times,
                              t1_down_times, config['a'][1], config['a'][1][k],
                              t2_down_times[k])
    res2 = wait_time_device_2(t2_local_times, t2_edge_times, t2_up_times,
                              t2_down_times, config['a'][2], k)
    return res1, res2

def update(config, lamda, mu):
    config['p'][1] = optimal_transmission_power_device_1(
                        config['beta1_t'], config['beta1_e'], lamda,
                        config['sigma'], config['P'][1],
                        config['h'][1], config['M'])
    config['p'][2] = optimal_transmission_power_device_2(
                        config['beta2_t'], config['beta2_e'], mu,
                        config['sigma'], config['P'][2],
                        config['h'][2], config['k'], config['N'])
    config['f'][1] = optimal_freq_device_1(config['beta1_t'], config['beta1_e'],
                                            lamda, config['f_peak'], config['_k'],
                                            config['M'])
    config['f'][2] = optimal_freq_device_2(config['beta2_t'], config['beta2_e'],
                                            mu, config['_k'], config['k'],
                                            config['f_peak'], config['M'])

def bi_search(config, prec=0.0001):
    vub, vlb = config['beta2_t'], 0
    while True:
        v = (vub + vlb)/2
        update(config, v, config['beta2_t'] - v)
        t1_wait, t2_wait = wait_times(config)
        if t1_wait - t2_wait < 0:
            vub = v
        else:
            vlb = v
        if abs(t1_wait - t2_wait) < prec:
            break
