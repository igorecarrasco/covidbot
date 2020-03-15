from random import choices
from typing import Callable

import humanize

from .covid import Covid


class Alerts(Covid):
    def __init__(self):
        super().__init__()

    @property
    def chosen_data(self) -> Callable:
        """
        Chooses at random with weighted distribution whether to get
        data for the whole world or any specific country. We want
        to post countries more.
        """
        chosen: Callable = choices(
            [self.world_data, self.random_country], weights=[0.1, 0.9], k=1
        )
        return chosen[0]()

    def generate(self):
        """
        Generates the alert.

        Data for a given country looks like this:
        {'country': 'Malta', 'cases': 21, 'todayCases': 3, 'deaths': 0, 'todayDeaths': 0, 'recovered': 2, 'critical': 0}

        Data for the world looks like:
        {'cases': 162386, 'deaths': 5984, 'recovered': 75967}
        """
        data = self.chosen_data
        if not data.get("country"):
            self.__world(data)
        elif data.get("cases") == 0:
            self.__no_cases(data)
        elif data.get("cases") == data.get("todayCases"):
            self.__first_batch(data)
        elif data.get("deaths") == data.get("todayDeaths") and data.get("deaths") != 0:
            self.__first_deaths(data)
        else:
            self.__country(data)

    def __world(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)

        self.post(
            f"Latest worldwide COVID-19 data: {humanize.intcomma(cases)} cases, {humanize.intcomma(deaths)} deaths.\n\nA {rate}% mortality rate."
        )

    def __country(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)

        self.post(
            f"Latest COVID-19 data for {data['country']}: {humanize.intcomma(cases)} cases, of those {data['todayCases']} today; {humanize.intcomma(deaths)} deaths, of those {data['todayDeaths']} today.\n\nA {rate}% mortality rate."
        )

    def __first_batch(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        self.post(
            f"First cases of COVID-19 confirmed in {data['country']}: {humanize.intcomma(cases)} cases, with {humanize.intcomma(deaths)} deaths reported."
        )

    def __first_deaths(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)
        self.post(
            f"First deaths by COVID-19 reported in {data['country']}: {humanize.intcomma(deaths)} people have died out of {humanize.intcomma(cases)} confirmed cases.\n\nA {rate}% mortality rate."
        )

    def __no_cases(self, data):
        self.post(
            f"Latest COVID-19 data: {data['country']} still reports no infections or deaths."
        )
