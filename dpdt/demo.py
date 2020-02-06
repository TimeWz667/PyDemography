from dpdt.load import fetch_demo, load_demo

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

    def to_sim_all(self):
        pass

    def to_sim_by_sex(self):
        pass

    def to_sim_by_age(self, agp, agl, ageing_to_death=False):
        pass

    def to_sim_by_age_sex(self, agp, agl, ageing_to_death=False):
        pass

    def __str__(self):
        return 'Demography Data(Year:[{}, {}], Age:[0, {}]'.format(
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
    print(demo)
