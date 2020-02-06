import pandas as pd

__author__ = 'TimeWz667'


def load_demo(folder, index='Time'):
    dat = {
        'p_f': pd.read_csv('{}/PopF.csv'.format(folder)).set_index(index),
        'p_m': pd.read_csv('{}/PopM.csv'.format(folder)).set_index(index),
        'p_t': pd.read_csv('{}/PopT.csv'.format(folder)).set_index(index),
        'dr_f': pd.read_csv('{}/DeaF.csv'.format(folder)).set_index(index),
        'dr_m': pd.read_csv('{}/DeaM.csv'.format(folder)).set_index(index),
        'dr_t': pd.read_csv('{}/DeaT.csv'.format(folder)).set_index(index),
        'bn': pd.read_csv('{}/Births.csv'.format(folder)).set_index(index)
    }
    return dat


def fetch_demo(folder='ByCountry/United Kingdom', repo='TimeWz667/pop4modelling', branch='master', index='Time'):
    url = 'https://raw.githubusercontent.com/{}/{}/{}'.format(repo, branch, folder)
    url = url.replace(' ', '%20')

    dat = {
        'p_f': pd.read_csv('{}/PopF.csv'.format(url)).set_index(index),
        'p_m': pd.read_csv('{}/PopM.csv'.format(url)).set_index(index),
        'p_t': pd.read_csv('{}/PopT.csv'.format(url)).set_index(index),
        'dr_f': pd.read_csv('{}/DeaF.csv'.format(url)).set_index(index),
        'dr_m': pd.read_csv('{}/DeaM.csv'.format(url)).set_index(index),
        'dr_t': pd.read_csv('{}/DeaT.csv'.format(url)).set_index(index),
        'bn': pd.read_csv('{}/Births.csv'.format(url)).set_index(index)
    }
    return dat
