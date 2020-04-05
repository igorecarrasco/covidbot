"""
Makes graphs based on the Johns Hopkings University tally of COVID-19 cases/deaths
"""
import random
from datetime import datetime
from typing import ClassVar

import matplotlib.dates as mdates
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import (
    MultipleLocator,
    ScalarFormatter,
    StrMethodFormatter,
    MaxNLocator,
)

from .country_groups import COUNTRY_GROUPS
from .utils import distribution


class Graph:
    cases_csv: ClassVar[
        str
    ] = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

    def random_country(self) -> list:
        """
        Gets a country at random. Weights more highly for countries
        with more cases, using a Pareto distribution.
        """
        self.df = (  # Get the data in a format we want to work with
            pd.read_csv(self.cases_csv)
            .drop(columns=["Province/State", "Lat", "Long"])
            .groupby("Country/Region")
            .sum()
            .rename(
                columns=lambda x: datetime.strptime(x, "%m/%d/%y").strftime("%d%b%Y")
            )
            .drop(labels="Diamond Princess")
        )

        self.df = self.df.sort_values(by=self.df.columns[-1], ascending=False)
        indexes = self.df.index
        dist = distribution(len(indexes))

        chosen = np.random.choice(indexes, 1, p=dist)[0]
        return chosen

    def make_graph(self, country):
        """
        Generates graph for a given country, returns the total
        number of cases. This method is doing two things at the
        same time, which is less than ideal but this is where we
        landed for now... may revisit later. 
        """

        series = self.df.loc[country, :].replace(0, np.nan).dropna()
        sz = (series > 9) * 1

        series = (series * sz).replace(0, np.nan).dropna()

        mx = max(map(int, list(series)))

        series2 = list(series.copy(deep=True))
        non_cumulative = []
        series2.reverse()
        for idx, num in enumerate(series2):
            try:
                non_cumulative.append(int(num - series2[idx + 1]))
            except IndexError:
                break

        non_cumulative.reverse()
        fig = plt.figure(figsize=(12, 6.75))
        ax = series.plot(marker="o", markersize=3.5)
        blue_line = mlines.Line2D(
            [], [], color="blue", marker="o", markersize=3.5, label="Cumulative(log)",
        )
        ax2 = ax.twinx()
        ax2.yaxis.set_tick_params(grid_alpha=0.4)
        bars = ax2.bar(
            x=range(len(non_cumulative)),
            height=non_cumulative,
            width=0.2,
            color="orange",
            edgecolor="orange",
            label="Daily(lin)",
        )
        ax.set_yscale("log")  # Use logarithmic scale for clarity
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.tick_params(which="minor", length=2)
        ax.grid(alpha=0.7, linestyle="dashed", linewidth=0.9)
        fig.autofmt_xdate()
        plt.style.use("seaborn-whitegrid")  # This is a nice theme to use.
        plt.title(f"COVID-19 cases, cumulative and daily: {country.replace('*', '')}")

        first_leg = plt.legend(
            bbox_to_anchor=(-0.1, 1.02, 1.0, 0.100),
            loc="upper left",
            handles=[blue_line],
        )
        plt.gca().add_artist(first_leg)

        plt.legend(
            bbox_to_anchor=(0.1, 1.02, 1.0, 0.100), loc="upper right", handles=[bars]
        )
        plt.margins(0.4)
        plt.savefig("/tmp/plot.png", bbox_inches="tight")

        return mx

    def make_group_countries_graph(self, countries):
        fig = plt.figure(figsize=(12, 6.75))
        countries_title = []
        ax = plt.gca()
        for country in countries:
            series = self.df.loc[country, :].replace(0, np.nan).dropna()

            sz = (series > 99) * 1

            series = (series * sz).replace(0, np.nan).dropna()
            s = list(series)
            if any(s):
                countries_title.append(country)
                ax.plot(s, marker="o", markersize=3, label=country)

        ax.legend()
        plt.yscale("log")  # Use logarithmic scale for clarity
        ax.grid(alpha=0.7, linestyle="dashed", linewidth=0.9)
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
        ax.yaxis.set_major_locator(MaxNLocator(8))

        plt.style.use("seaborn-whitegrid")  # This is a nice theme to use.

        plt.title(f"COVID-19 cases, cumulative: {', '.join(countries_title)}")
        plt.xlabel("Days since 100th confirmed case")
        plt.margins(0.0001)
        plt.savefig("/tmp/group_plot.png", bbox_inches="tight")

    def random_country_graph(self):
        """
        Generates graph, returns data to create an alert.
        """
        country = self.random_country()
        while True:
            try:
                cases_total = self.make_graph(country)
                break
            except ValueError:
                continue

        return {
            "graph": True,
            "cases": cases_total,
            "country": country,
            "img_path": "/tmp/plot.png",
        }

    def random_country_group_graph(self):
        """
        Generates graph for a random group of countries. We'll pick from the
        WHO's groupings, as defined here, broken down in case they're too big:
        
        https://www.who.int/quantifying_ehimpacts/global/ebdcountgroup/en/
        """
        countries = random.choice(COUNTRY_GROUPS)
        self.df = (  # Get the data in a format we want to work with
            pd.read_csv(self.cases_csv)
            .drop(columns=["Province/State", "Lat", "Long"])
            .groupby("Country/Region")
            .sum()
            .rename(
                columns=lambda x: datetime.strptime(x, "%m/%d/%y").strftime("%d%b%Y")
            )
            .drop(labels="Diamond Princess")
        )

        self.make_group_countries_graph(countries)

        return {
            "graph_group": True,
            "countries": countries,
            "img_path": "/tmp/group_plot.png",
        }
