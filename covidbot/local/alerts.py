from random import choices
from typing import Callable

import humanize

from .covid import Covid
from .graph import Graph
from .image import Image
from .testing import Testing
from .twitter import Twitter


class Alerts(Covid, Graph, Image, Testing, Twitter):
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
                self.random_country_data,
                self.random_country_graph,
                self.random_image,
                self.random_country_tests,
                self.random_country_group_graph,
            ],
            weights=[0.2, 0.1, 0.25, 0.05, 0.15, 0.25],
            k=1,
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

        if data.get("image"):
            self.__image(data)
        elif data.get("tests"):
            self.__tests(data)
        elif data.get("graph"):
            self.__graph(data)
        elif data.get("graph_group"):
            self.__graph_group(data)
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
        img_path = data["img_path"]
        media_id = self.upload_image(img_path)

        self.post(
            f"Guidance from the World Health Organization (WHO)", media_ids=[media_id],
        )

    def __graph(self, data):
        cases = data["cases"]
        country = data["country"]
        img_path = data["img_path"]
        media_id = self.upload_image(img_path)

        self.post(
            f"Evolution of number of cases for {country.replace('*', '')}, with a total confirmed of {humanize.intcomma(cases)}",
            media_ids=[media_id],
        )

    def __graph_group(self, data):
        countries = data["countries"]
        img_path = data["img_path"]
        media_id = self.upload_image(img_path)

        self.post(
            f"Evolution of cases in {', '.join(countries)}, since 100th confirmed case.",
            media_ids=[media_id],
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
        today_cases = data["todayCases"]
        today_deaths = data["todayDeaths"]
        rate = round(deaths / cases * 100, 2)

        self.post(
            f"Latest COVID-19 data for {data['country']}: {humanize.intcomma(cases)} case{'s' if cases > 1 else ''}, of those {humanize.intcomma(today_cases)} today; {humanize.intcomma(deaths)} death{'s' if deaths > 1 else ''}, of those {humanize.intcomma(today_deaths)} today.\n\nA {rate}% fatality rate."
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

    def __tests(self, data):
        try:  # lets try to enrich this with other statistics from the country in question
            if len(data["country"]) <= 2:
                raise ValueError("Likely a state. Skipping...")
            country_data = self.country(data["country"])
            cases = country_data["cases"]
            today_cases = country_data["todayCases"]
            deaths = country_data["deaths"]
            today_deaths = country_data["todayDeaths"]
        except Exception as e:  # if anything blows up here and we can't find the country by FuzzyMatching, no biggie
            print(str(e))
            country_data = None

        message = (
            f"Total COVID-19 tests performed in {data['country']}: {data['tests']}."
        )

        if country_data:
            message = (
                message
                + f" {humanize.intcomma(cases)} case{'s' if cases > 1 else ''}, of those {humanize.intcomma(today_cases)} today; {humanize.intcomma(deaths)} death{'s' if deaths > 1 else ''}, of those {humanize.intcomma(today_deaths)} today."
            )

        self.post(message)
