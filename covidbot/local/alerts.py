from random import choices
from typing import Callable

import humanize

from .covid import Covid
from .graph import Graph
from .image import Image


class Alerts(Covid, Graph, Image):
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
            [
                self.world_data,
                self.random_country_data(),
                self.random_country_graph(),
                self.random_image(),
            ],
            weights=[0.2, 0.4, 0.2, 0.2],
            k=1,
        )
        return chosen[0]

    def generate(self):
        """
        Generates the alert.

        Data for a given country looks like this:
        {'country': 'Malta', 'cases': 21, 'todayCases': 3, 'deaths': 0, 'todayDeaths': 0, 'recovered': 2, 'critical': 0}

        Data for the world looks like:
        {'cases': 162386, 'deaths': 5984, 'recovered': 75967}
        """
        data = self.chosen_data

        if data.get("image"):
            self.__image(data)
        elif data.get("graph"):
            self.__graph(data)
        elif not data.get("country"):
            self.__world(data)
        elif data.get("cases") == 0:
            self.__no_cases(data)
        elif data.get("cases") == data.get("todayCases"):
            self.__first_batch(data)
        elif data.get("deaths") == data.get("todayDeaths") and data.get("deaths") != 0:
            self.__first_deaths(data)
        else:
            self.__country(data)

    def __image(self, data):
        self.post(
            f"Guidance from the World Health Organization (WHO)",
            media_ids=[self.random_filename],
        )

    def __graph(self, data):
        cases = data["cases"]
        country = data["country"]

        self.post(
            f"Evolution of number of cases for {country}, with a total confirmed of {humanize.intcomma(cases)}",
            media_ids=[self.media_id],
        )

    def __world(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)

        self.post(
            f"Latest worldwide COVID-19 data: {humanize.intcomma(cases)} cases, {humanize.intcomma(deaths)} deaths.\n\nA {rate}% fatality rate."
        )

    def __country(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)

        self.post(
            f"Latest COVID-19 data for {data['country']}: {humanize.intcomma(cases)} case{'s' if cases > 1 else ''}, of those {humanize.intcomma(data['todayCases'])} today; {humanize.intcomma(deaths)} death{'s' if deaths > 1 else ''}, of those {humanize.intcomma(data['todayDeaths'])} today.\n\nA {rate}% fatality rate."
        )

    def __first_batch(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        self.post(
            f"First case{'s' if cases > 1 else ''} of COVID-19 confirmed in {data['country']}: {humanize.intcomma(cases)} case{'s' if cases > 1 else ''}, with {humanize.intcomma(deaths)} death{'s' if deaths > 1 else ''} reported."
        )

    def __first_deaths(self, data):
        cases = data["cases"]
        deaths = data["deaths"]

        rate = round(deaths / cases * 100, 2)
        self.post(
            f"First death{'s' if cases > 1 else ''} by COVID-19 reported in {data['country']}: {humanize.intcomma(deaths)} {'people' if cases > 1 else 'person'} have died out of {humanize.intcomma(cases)} confirmed cases.\n\nA {rate}% fatality rate."
        )

    def __no_cases(self, data):
        self.post(
            f"Latest COVID-19 data: {data['country']} still reports no infections or deaths."
        )
