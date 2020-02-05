__author__ = 'TimeWz667'


class Demography:
    def __init__(self, bn, pf, pm, pt, df, dm, dt, sex_ratio_birth=107):
        self.BirN = bn
        self.PopF = pf
        self.PopM = pm
        self.PopT = pt
        self.DeaF = df
        self.DeaM = dm
        self.DeaT = dt
        self.SexRationBirth = sex_ratio_birth
        self.Years = list(bn.index)
        self.Years.sort()

    def set_years(self):
        pass

    def reset_years(self):
        pass

    def to_sim_all(self):
        pass

    def to_sim_by_sex(self):
        pass

    def to_sim_by_age(self, agp, agl):
        pass

    def to_sim_by_age_sex(self, agp, agl):
        pass

    @staticmethod
    def load(self, folder: str, index='Time'):
        pass

    @staticmethod
    def fetch(self, repo, folder, branch='master', index='Time'):
        pass
