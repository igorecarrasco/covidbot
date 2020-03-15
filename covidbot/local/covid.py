"""
COVID data fetcher
"""
from typing import ClassVar

import numpy as np
import requests
from fuzzywuzzy import process
from numpy import random

from .utils import distribution


class Covid:
    api_base: ClassVar[str] = "https://corona.lmao.ninja"
    non_countries: ClassVar[list] = ["Diamond Princess"]

    @property
    def world_data(self) -> dict:
        """
        Gets worldwide data.
        """
        r = requests.get(f"{self.api_base}/all", timeout=3)
        result = r.json()
        return result

    @property
    def countries_data(self) -> list:
        """
        Gets countries data. 
        """
        r = requests.get(f"{self.api_base}/countries", timeout=3)
        result = r.json()

        data = [c for c in result if c["country"] not in self.non_countries]

        return data

    def __country(self, country: str) -> dict:
        """
        Gets data for a specific country. Uses fuzzy matching 
        to get the most highly likely match for an input 
        country. This is because the API we're using isn't
        particularly tidy with its country name usage.

        Parameters:
        -----------
        country: str
            The country name in question
        """
        data = self.__countries_data__
        country_names = [i["country"] for i in data]
        c: str = process.extractOne(country, country_names)[0]

        return [i for i in data if i["country"] == c][0]

    def random_country_data(self) -> dict:
        """
        Gets a random country, weighted by a Pareto
        distribution so we give countries with higher
        case loads more prominence.
        """

        c_data = self.countries_data
        draw = random.choice(c_data, 1, p=distribution(len(c_data)))

        return draw[0]
