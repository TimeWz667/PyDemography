import pandas as pd
import numpy as np
from collections import Counter
from scipy.linalg import expm
from scipy.optimize import least_squares

__author__ = 'TimeWz667'


def calc_mr_agp(p0, p1, dr, br, ageing):
    """

    :param p0:
    :param p1:
    :param dr:
    :param br:
    :param ageing:
    :return:
    """
    n_age = len(dr)

    BAD = np.diag(- dr - ageing)
    BAD[0,] += br
    BAD[1:n_age, 0:(n_age - 1)] += np.diag(ageing[0:(n_age - 1)])
    trBAD = expm(BAD)

    PBAD = np.dot(trBAD, p0)
    mr0 = np.log(p1 / PBAD)

    def fn(x, p_0, p_1, bad):
        PMBAD = np.dot(expm(bad + np.diag(x)), p_0)
        return PMBAD - p_1

    ols = least_squares(fn, mr0, bounds=(-0.5, 0.5), args=(p0, p1, BAD))

    mr = ols['x']
    error = fn(ols['x'], p0, p1, BAD)
    mse = sum(error * error) / len(error)

    return mr, mse


def as_simulation_input_agp(demo, gp, k, agp, agl, ageing_to_death=False, bind=False):
    """

    :param demo:
    :param gp:
    :param k:
    :param agp:
    :param agl:
    :param ageing_to_death:
    :param bind:
    :return:
    """
    assert len(agl) > 1
    agp_counts = Counter(agp)
    assert len(agp_counts) is len(agl)
    age_span = [agp_counts[i + 1] for i in range(len(agl))]
    ageing = 1 / np.array(age_span)
    if not ageing_to_death:
        ageing[-1] = 0

    years = demo.Years
    year0 = demo.Year0
    year1 = demo.Year1
    years = [year for year in years if year0 <= year <= year1]

    if gp == 'F':
        op, od, ob = demo.PopF, demo.DeaF, demo.BirN * k
    elif gp == 'M':
        op, od, ob = demo.PopM, demo.DeaM, demo.BirN * k
    elif gp == 'T':
        op, od, ob = demo.PopT, demo.DeaT, demo.BirN * k
    else:
        raise (KeyError('Unknown group of population'))

    ps, drs, brs, mrs, mses = list(), list(), list(), list(), list()

    for year in years:
        bn = ob.loc[year][0]
        p0 = pd.Series(op.loc[year])
        p1 = pd.Series(op.loc[year + 1])
        dr = pd.Series(od.loc[year] * p0).groupby(agp).sum()

        p0 = p0.groupby(agp).sum()
        p1 = p1.groupby(agp).sum()
        dr /= p0
        br = bn / p0.sum()

        mr, mse = calc_mr_agp(p0, p1, dr, br, ageing)

        ps.append(p0.tolist())
        drs.append(dr.tolist())
        brs.append(br.tolist())
        mrs.append(list(mr))
        mses.append(mse)

    def as_df(d, pre=''):
        if len(pre):
            d = pd.DataFrame(d, columns=['{} [{}]'.format(pre, l) for l in agl])
        else:
            d = pd.DataFrame(d, columns=list(agl))
        d['Year'] = years
        d = d.set_index('Year')
        return d

    if bind:
        res = pd.DataFrame({'Year': years, 'BirR': brs})
        res = pd.merge(res, as_df(drs, 'DeaR'), on='Year')
        res = pd.merge(res, as_df(mrs, 'MigR'), on='Year')
        res = pd.merge(res, as_df(ps, 'PopN'), on='Year')
        res['MSE'] = mses
        res = res.set_index('Year')
    else:
        res = {
            'BirR': pd.DataFrame({'Year': years, 'BirR': brs}).set_index('Year'),
            'DeaR': as_df(drs),
            'MigR': as_df(mrs),
            'PopN': as_df(ps),
            'MSE': pd.DataFrame({'Year': years, 'MSE': mses}).set_index('Year'),
            'Labels': agl,
            'Ageing': ageing
        }

    return res
