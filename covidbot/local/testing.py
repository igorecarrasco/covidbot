"""
This code is to scrape testing data for dozens of countries around the world compiled 
by the good people of Wikipedia. The article this data figures in is 
https://en.wikipedia.org/wiki/COVID-19_testing. The data is released under the Creative 
Commons Attribution-Share-Alike License 3.0.
"""

import numpy as np
import requests

from bs4 import BeautifulSoup

from .utils import distribution


class Testing:
    url = "https://en.wikipedia.org/wiki/Template:COVID-19_testing"

    @property
    def countries(self) -> list:
        """
        Get countries from the Wikipedia table
        """
        return [
            a.string
            for a in self.table.find_all("a")
            if not a.string.startswith("[")
            and len(a.string) > 1
            and a.string != "testing"
        ]

    @property
    def tests(self) -> list:
        """
        Get numbers of tests administered from Wikipedia table
        """
        bd = self.table.find("tbody")
        rows = bd.find_all("tr")
        tests = []
        for i, r in enumerate(
            rows
        ):  # find_all isn't an iterator, so we have to do skip the header in this clunky way
            if i == 0:
                continue
            else:
                tests.append(r.find("td").string.replace("\n", ""))

        return tests

    @property
    def testing_data(self):
        return list(zip(self.countries, self.tests))

    def random_country_tests(self):
        """
        Returns number of tests for a random country
        """
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.content, features="html.parser")
        self.table = self.soup.find("table", {"class": "covid19-testing"})

        data = self.testing_data
        dist = distribution(len(data))
        idx = np.random.choice(len(data), size=1, p=dist)
        chosen = data[idx[0]]

        return {"country": chosen[0], "tests": chosen[1]}
