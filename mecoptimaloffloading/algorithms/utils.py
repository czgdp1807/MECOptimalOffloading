import math, mpmath

__all__ = [
    'computation_time_device_1',
    'downlink_data_rate',
    'downloading_transmission_time',
    'energy_consumption_device_1',
    'energy_consumption_device_2',
    'energy_consumption_local',
    'eta',
    'exec_time_edge',
    'exec_time_local',
    'offloading_transmission_energy',
    'offloading_transmission_time',
    'optimal_freq_device_1',
    'optimal_freq_device_2',
    'optimal_transmission_power_device_1',
    'optimal_transmission_power_device_2',
    'total_time_device_1',
    'total_wait_device_2',
    'transmission_time_device_1',
    'uplink_data_rate',
    'wait_time_device_1',
    'wait_time_device_2'
]

def exec_time_local(workload, cpu_frequency):
    return [L/f for L, f in
            zip(workload, cpu_frequency)]

def energy_consumption_local(workload, cpu_frequency, k):
    return [k*L*f**2 for L, f in
            zip(workload, cpu_frequency)]

def uplink_data_rate(transmission_power, offloading_gain,
                     bandwidth, sigma):
    return [bandwidth*math.log2(1 + (p*h)/sigma**2)
            for p, h in zip(transmission_power, offloading_gain)]

def offloading_transmission_time(Outputs, data_rate):
    return [0] + [Outputs[i-1]/data_rate[i] for i in
                    range(1, len(data_rate))]

def offloading_transmission_energy(transmission_power, transmission_time):
    return [p*t for p, t in zip(transmission_power, transmission_time)]

def exec_time_edge(workload, cpu_frequency):
    return [L/cpu_frequency for L in workload]

def downlink_data_rate(transmission_power, downloading_gain,
                       bandwidth, sigma):
    return [bandwidth*math.log(1 + (t*g)/sigma**2)
            for t, g in zip(transmission_power, downloading_gain)]

def downloading_transmission_time(Outputs, data_rate):
    return offloading_transmission_time(Outputs, data_rate)

def computation_time_device_1(local_times, edge_times, a):
    return sum([(1 - ai)*tl + ai*tc for ai, tl, tc
            in zip(a, local_times, edge_times)])

def transmission_time_device_1(up_time, down_time, a):
    return sum([a[0]*up_time[0]] + [a[i]*(1 - a[i-1])*up_time[i] +
            (1 - a[i])*a[i-1]*down_time[i]
            for i in range(1, len(a) - 1)] + [a[-1]*down_time[-1]])

def total_time_device_1(computation_time, transmission_time):
    return computation_time + transmission_time

def energy_consumption_device_1(local_energy, transmission_energy, a):
    return sum([0] + [(1 - a[i])*local_energy[i] +
            a[i]*(1 - a[i-1])*transmission_energy[i]
            for i in range(1, len(a) - 1)] + [(1 - a[-2])*transmission_energy[-1]])

def energy_consumption_device_2(local_energy, transmission_energy, a):
    return energy_consumption_device_1(local_energy, transmission_energy, a)

def wait_time_device_1(local_times, edge_times,
                       up_times, down_times,
                       a, ak2, tk2):
    tl, tc, tu, td = local_times, edge_times, up_times, down_times
    f = lambda i: ((1 - a[i])*tl[i] + a[i]*(tc[i] + tu[i]) + a[i-1]*td[i] -
                    a[i-1]*a[i]*(tu[i] + td[i]))
    time = sum([f(i) for i in range(1, len(a) - 1)])
    return time + (1 - a[-2])*tu[-1] + (1 - ak2)*tk2

def wait_time_device_2(local_times, edge_times,
                       up_times, down_times, a, k):
    tl, tc, tu, td = local_times, edge_times, up_times, down_times
    f = lambda i: ((1 - a[i])*tl[i] + a[i]*(tc[i] + tu[i]) + a[i-1]*td[i] -
                    a[i-1]*a[i]*(tu[i] + td[i]))
    time = sum([f(i) for i in range(1, k)])
    return time + a[k]*tu[k] + a[k-1]*td[k] - a[k-1]*a[k]*(tu[k] + td[k])

def total_wait_device_2(device_1_time, device_2_time,
                        local_time, comp_times, a, k):
    time = max(device_1_time, device_2_time)
    return time + sum([(1 - a[i])*local_time[i] + a[i]*comp_times[i]
                        for i in range(k, len(a) - 1)])

def eta(energy, time, beta):
    return beta*energy + (1 - beta)*time

def optimal_freq_device_1(beta_t, beta_e, lamda, f_peak, _k, M):
    expr = min(((beta_t + lamda)/(2*_k*beta_e))**(1/3), f_peak)
    return [expr for _ in range(M+2)]

def optimal_freq_device_2(beta_t, beta_e, mu, _k, k, f_peak, M):
    expr1 = min((mu/(2*_k*beta_e))**(1/3), f_peak)
    expr2 = min((beta_t/(2*_k*beta_e))**(1/3), f_peak)
    l1 = [expr1 for _ in range(k)]
    l2 = [expr2 for _ in range(k, M+2)]
    return l1 + l2

def lambertw(x):
    num = mpmath.lambertw(x)
    return num

def optimal_transmission_power_device_1(beta_t, beta_e, lamda, sigma, P, h, M):
    A1 = 1 + (beta_t + lamda)/(beta_e*P)
    B1 = lambda i: h[i]*(beta_t + lamda)/(beta_e*sigma**2) - 1
    A2 = 1 + lamda/(beta_e*P)
    B2 = lambda i: (h[i]*lamda)/(beta_e*sigma**2) - 1
    cond = lambda i: h[i] < (sigma**2/P)*(A1/-(lambertw(-A1*math.exp(-A1))) - 1)
    l1 = [0] + [P if cond(i) else (sigma**2/h[i])*(B1(i)/(lambertw(B1(i)/math.e)) - 1)
          for i in range(M)]
    cond = lambda i: h[i] < (sigma**2/P)*(A2/-(lambertw(-A2*math.exp(-A2))) - 1)
    l1.append(P if cond(M+1) else (sigma**2/h[M+1])*(B2(M+1)/(lambertw(B2(M+1)/math.e)) - 1))
    return l1

def optimal_transmission_power_device_2(beta_t, beta_e, mu, sigma, P, h, k, N):
    A3 = 1 + beta_t/(beta_e*P)
    B3 = lambda i: (h[i]*beta_t)/(beta_e*sigma**2) - 1
    A4 = 1 + mu/(beta_e*P)
    B4 = lambda i: (h[i]*mu)/(beta_e*sigma**2) - 1
    cond = lambda i: h[i] < (sigma**2/P)*(A4/-(mpmath.lambertw(-A4*math.exp(-A4))) - 1)
    l1 = [P if cond(i) else (sigma**2/h[i])*(B4(i)/(mpmath.lambertw(B4(i)/math.e)) - 1)
          for i in range(k + 1)]
    cond = lambda i: h[i] < (sigma**2/P)*(A3/-(mpmath.lambertw(-A3*math.exp(-A3))) - 1)
    l2 = [P if cond(i) else (sigma**2/h[i])*(B3(i)/(mpmath.lambertw(B3(i)/math.e)) - 1)
            for i in range(k + 1, N + 2)]
    return l1 + l2

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
