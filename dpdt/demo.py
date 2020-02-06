import pandas as pd
from dpdt.load import fetch_demo, load_demo
from dpdt.transformation import as_simulation_input_agg, as_simulation_input_agp

__author__ = 'TimeWz667'


class Demography:
    def __init__(self, bn, p_f, p_m, p_t, dr_f, dr_m, dr_t, sex_ratio_birth=107):
        self.BirN = bn
        self.PopF = p_f
        self.PopM = p_m
        self.PopT = p_t
        self.DeaF = dr_f
        self.DeaM = dr_m
        self.DeaT = dr_t
        self.SexRationBirth = sex_ratio_birth
        self.Years = list(bn.index)
        self.Years.sort()
        self.Year0 = min(self.Years)
        self.Year1 = max(self.Years)

    def set_years(self, y0, y1):
        assert y0 < y1
        assert y1 <= max(self.Years)
        assert y0 > min(self.Years)
        self.Year0, self.Year1 = y0, y1

    def reset_years(self):
        self.Year0 = min(self.Years)
        self.Year1 = max(self.Years)

    def calc_sex_ratio_at_birth(self):
        pr_f = 100 / (self.SexRationBirth + 100)
        return pr_f, 1 - pr_f

    def to_sim_all(self):
        """
        Generate simulation-friendly aggregate data
        :return: a data frame of generated data
        :rtype: pd.DataFrame
        """
        return as_simulation_input_agg(self, 'T', 1)

    def to_sim_by_sex(self):
        """
        Generate simulation-friendly sex-specific data
        :return: a data frame of generated data
        :rtype: pd.DataFrame
        """
        pr_f, pr_m = self.calc_sex_ratio_at_birth()
        sim_f = as_simulation_input_agg(self, 'F', pr_f)
        sim_m = as_simulation_input_agg(self, 'M', pr_m)

        sim_sex = pd.merge(sim_f, sim_m, on='Year', suffixes=['_F', '_M'])
        return sim_sex

    def to_sim_by_age(self, agp, agl, ageing_to_death=False, bind=False):
        """

        :param agp:
        :param agl:
        :param ageing_to_death:
        :param bind:
        :return:
        """
        return as_simulation_input_agp(self, 'T', 1, agp, agl,
                                       ageing_to_death = ageing_to_death, bind = bind)

    def to_sim_by_age_sex(self, agp, agl, ageing_to_death=False, bind=False):
        """

        :param agp:
        :param agl:
        :param ageing_to_death:
        :param bind:
        :return:
        """
        pr_f, pr_m = self.calc_sex_ratio_at_birth()
        sim_f = as_simulation_input_agp(self, 'F', pr_f, agp, agl,
                                        ageing_to_death=ageing_to_death, bind=bind)
        sim_m = as_simulation_input_agp(self, 'M', pr_m, agp, agl,
                                        ageing_to_death=ageing_to_death, bind=bind)

        if bind:
            sim_age_sex = pd.merge(sim_f, sim_m, on='Year', suffixes=['_F', '_M'])
        else:
            sim_age_sex = {
                'Female': sim_f,
                'Male': sim_m
            }

        return sim_age_sex

    def __str__(self):
        return 'Demography Data(Year:[{}, {}], Age:[0, {}])'.format(
            self.Year0, self.Year1, self.DeaT.shape[1] - 1)

    __repr__ = __str__

    @staticmethod
    def load(folder: str, index='Time', sex_ratio_birth=107):
        dat = load_demo(folder, index=index)
        demo = Demography(**dat, sex_ratio_birth=sex_ratio_birth)
        return demo

    @staticmethod
    def fetch(folder, repo='TimeWz667/pop4modelling', branch='master',
              index='Time', sex_ratio_birth=107):
        dat = fetch_demo(folder, repo=repo, index=index, branch=branch)
        demo = Demography(**dat, sex_ratio_birth=sex_ratio_birth)
        return demo


if __name__ == '__main__':
    demo = Demography.fetch('ByCountry/United Kingdom')
    demo.set_years(2000, 2020)

    print(demo)

    print(demo.to_sim_all())

    print(demo.to_sim_by_sex())
