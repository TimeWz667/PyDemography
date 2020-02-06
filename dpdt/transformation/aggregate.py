import numpy as np
import pandas as pd

__author__ = 'TimeWz667'


def calc_mr_agg(p0, p1, dr, br):
    """
    Calculate migration rate for aggregated population
    :param p0: initial population size
    :param p1: target population size
    :param dr: death rate
    :param br: birth rate
    :return: a tuple of (migration rate, mse)
    """
    mr = np.log(p1 / p0) - br + dr
    p_hat = p0 * np.exp(mr + br - dr)
    return mr, pow(p_hat - p1, 2)


def as_simulation_input_agg(demo, gp, k):
    """
    Generate simulation-friendly aggregated data
    :param demo: Demography data
    :type demo: Demography
    :param gp: group of population, T for total, F for female, M for male
    :param k: proportion of birth count
    :return: a data frame of generated data
    :rtype: pd.DataFrame
    """
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
        raise(KeyError('Unknown group of population'))

    ps, drs, brs, mrs, mses = list(), list(), list(), list(), list()

    for year in years:
        bn = ob.loc[year][0]

        p0 = op.loc[year]
        p1 = op.loc[year + 1]
        dr = od.loc[year]

        dr = (dr * p0).sum() / p0.sum()
        p0 = p0.sum()
        p1 = p1.sum()
        br = k * bn / p0

        mr, mse = calc_mr_agg(p0, p1, dr, br)

        ps.append(p0)
        drs.append(dr)
        brs.append(br)
        mrs.append(mr)
        mses.append(mse)

    res = {
        'Year': years,
        'Pop': ps,
        'DeaR': drs,
        'BirR': brs,
        'MigR': mrs,
        'MSE': mses
    }

    res = pd.DataFrame(res)
    res = res.set_index('Year')

    return res
