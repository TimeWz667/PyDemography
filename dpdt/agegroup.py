import numpy as np

__author__ = 'TimeWz667'


AG_CA = [1] * 15 + [2] * 86
AL_CA = ['0-14'] + ['15+']

AG_CMO = [1] * 15 + [2] * 50 + [3] * 36
AL_CMO = ['0-14', '15-64', '65+']

AG_CYMO = [1] * 15 + [2] * 20 + [3] * 30 + [3] * 36
AL_CYMO = ['0-14', '15-34', '35-64', '65+']

AG_5Y75 = list(np.repeat(range(1, 16), 5)) + [16] * 26
AL_5Y75 = ['{}-{}'.format(i * 5, i * 5 + 4) for i in range(15)] + ['75+']

AG_5Y80 = list(np.repeat(range(1, 17), 5)) + [17] * 21
AL_5Y80 = ['{}-{}'.format(i * 5, i * 5 + 4) for i in range(16)] + ['80+']
