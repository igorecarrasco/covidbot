"""
COVID data fetcher
"""
from dataclasses import dataclass
from typing import ClassVar

import requests
from fuzzywuzzy import process


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

    def country_data(self, country: str) -> dict:
        """
        Gets country data. Uses fuzzy matching to get the
        most highly likely match for an input country. This
        is because the API we're using isn't particularly
        tidy with its country name usage.

        Parameters:
        -----------
        country: str
            The country name in question
        """
        r = requests.get(f"{self.api_base}/countries", timeout=3)
        result = r.json()

        data = [c for c in result if c["country"] not in self.non_countries]

        countries = [i["country"] for i in result]
        c = process.extractOne(countries, country)

        return [i for i in result if i["country"] == c][0]

