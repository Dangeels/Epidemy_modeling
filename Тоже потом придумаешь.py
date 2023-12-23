import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

class NazvaniePotomPridumau():

    def __init__(self,
                 country: str = 'Russia',
                 days_of_simulation: int = 365,
                 coef_base: float = 0.35,
                 coef_quarantine: float = 0.135,
                 death_rate: float = 0.035,
                 recovery_rate: float = 0.1,
                 day_quarantine: int = 73,
                 incubation_period: int = 15
                 ):
        self.country = country
        self.days_of_simulation = days_of_simulation
        self.coef_base = coef_base
        self.coef_quarantine = coef_quarantine
        self.death_rate = death_rate
        self.recovery_rate = recovery_rate
        self.day_quarantine = day_quarantine
        self.incubation_period = incubation_period



    def get_coef(self, day: int) -> float:
        return self.coef_base if day < self.day_quarantine else self.coef_quarantine

    def get_folks_per_day(self, lst: list) -> dict:

        return {
                'max_day': lst.index(max(lst))+1,
                'max_day_count' : lst[lst.index(max(lst))],
                'total' : sum(lst)
                }

    def simulation(self) -> dict:
        # Первый инфицированный
        infected = np.random.randint(1, self.incubation_period, 1)

        infected_lst = []
        new_cases_lst = []
        recovered_lst = []
        deaths_lst = []

        for day in np.arange(1,self.days_of_simulation+1):
            # Проверяем заражённых на предмет появления симптомов
            new_cases_idx = np.argwhere(infected == day).flatten()
            # Удаляем заражённых с симптомами из списка инфицированных, способных заражать
            infected = np.delete(infected, new_cases_idx)
            # Генерируем новых заражённых в соответствии с распределением Пуассона и добавляем их к имеющимся
            new_infected_count = np.random.poisson(self.get_coef(day), infected.size).sum()
            new_infected = np.random.randint(1, self.incubation_period, new_infected_count) + day
            infected = np.concatenate((infected, new_infected))
            # Заполняем статистику
            infected_lst.append(infected.size)
            new_cases_lst.append(new_cases_idx.size)
            recovered_lst.append(math.floor(infected.size * self.recovery_rate))
            deaths_lst.append(math.floor(infected.size * self.death_rate))

        return {'infected':infected_lst,'registered_cases':new_cases_lst,'recovered':recovered_lst,'deaths':deaths_lst}

if __name__ == '__main__':

    np.random.seed(0)

    suka = NazvaniePotomPridumau()
    infected, new_cases, recovered, deaths = suka.simulation().values()

    matplotlib.rcParams['axes.formatter.limits'] = (-3,15)

    blyat = suka.simulation()
    colours = {'infected':'y','registered_cases':'g','recovered':'b','deaths':'r'}
    for i in blyat.keys():
        plt.figure(figsize=(10,10))
        plt.plot(blyat[i],colours[i])
        plt.title(f'Maximum day {suka.get_folks_per_day(blyat[i])["max_day"]}, count {suka.get_folks_per_day(blyat[i])["max_day_count"]}')
        plt.ylabel(f'Amount of {i} per day')
        plt.xlabel('Days')
        plt.show()


    values = [suka.get_folks_per_day(i)['total'] for i in blyat.values()]

    plt.subplots(figsize=(12,10))
    plt.barh(y=['infected','registered_cases','recovered','deaths'][::-1],width=values[::-1])
    plt.show()


