import math
import pandas as pd

pd.set_option('display.max_columns', 10000)

def e_s(T):
    return 6.11 * (53.49 - 6808 / T - 5.09 * T.apply(math.log)).apply(math.exp)

def e(r, e_s):
    return r*e_s

def T(T_virt, w):
    return T_virt / (1 + 0.61 * w)

def r(T_dew, T_virt):
    return ((2.5e06/461.51) * ((T_dew - T_virt) / (T_dew * T_virt))).apply(math.exp)

def w(p, e):
    return 0.622 * e / (p-e)

def theta_virt(T_virt, p):
    return T_virt * (1000 / p) ** (287 / 1005)

def theta_e(T, p, e, w, r):
    pd = p - e
    return T * ((1000 / pd) ** (287 / 1005)) * (r ** ((-w*461.51)/1005)) * ((2.5e06*w)/(1005 * T)).apply(math.exp)

df = pd.DataFrame({
    'p': [1000, 950, 900, 850, 800, 750, 700, 650, 600],
    'T_virt': [30.0, 25.0, 18.5, 16.5, 20.0, 10.0, -5.0, -10.0, -20.0],
    'T_dew': [22.0, 21.0, 18.0, 15.0, 10.0, 5.0, -10.0, -15.0, -30.0]
    })

df['T_virt']= df['T_virt'] + 273.15
df['T_dew'] = df['T_dew'] + 273.15

df['r'] = r(df['T_dew'], df['T_virt'])
df['e_s'] = e_s(df['T_virt'])
df['e'] = e(df['r'], df['e_s'])
df['w'] = w(df['p'], df['e'])
df['T'] = T(df['T_virt'], df['w'])
df['theta_virt'] = theta_virt(df['T_virt'], df['p'])
df['theta_e'] = theta_e(df['T'], df['p'], df['e'], df['w'], df['r'])
df['w'] = df['w'] * 1000

print(df)
