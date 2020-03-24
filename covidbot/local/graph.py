"""
Makes graphs based on the Johns Hopkings University tally of COVID-19 cases/deaths
"""
from typing import ClassVar

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

from .twitter import Twitter
from .utils import distribution


class Graph(Twitter):
    cases_csv: ClassVar[
        str
    ] = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"

    def __init__(self):
        super().__init__()
        self.df = (  # Get the data in a format we want to work with
            pd.read_csv(self.cases_csv)
            .drop(columns=["Province/State", "Lat", "Long"])
            .groupby("Country/Region")
            .sum()
            .replace(0, np.nan)
            .dropna()
            .rename(
                columns=lambda x: datetime.strptime(x, "%m/%d/%y").strftime("%d%b%Y")
            )
        )

        self.df = self.df.sort_values(by=self.df.columns[-1], ascending=False)

    def random_country(self):
        """
        Gets a country at random. Weights more highly for countries
        with more cases, using a Pareto distribution.
        """
        indexes = self.df.index
        dist = distribution(len(indexes))

        chosen = np.random.choice(indexes, 1, p=dist)[0]
        data = self.df.loc[chosen, :]
        return chosen, data

    def make_graph(self, country, series):
        """
        Generates graph for a given country, returns the total
        number of cases. This method is doing two things at the
        same time, which is less than ideal but this is where we
        landed for now... may revisit later. 
        """
        plt.figure(figsize=(12, 6.75))

        ax = plt.gca()

        ax.set_yscale("log")  # Use logarithmic scale for clarity

        plt.style.use("seaborn-darkgrid")  # This is a nice theme to use.
        mx = max(map(int, list(series)))
        plt.yticks(
            [mx, mx // 10, mx // 100, mx // 500, mx // 2500],
            [
                int(round(mx, len(str(mx)) * -1 + 2)),
                int(round(mx // 10, len(str(mx // 10)) * -1 + 2)),
                int(round(mx // 100, len(str(mx // 100)) * -1 + 2)),
                int(round(mx // 500, len(str(mx // 500)) * -1 + 2)),
                int(round(mx // 2500, len(str(mx // 2500)) * -1 + 2)),
            ],
        )
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d%b%Y"))
        plt.margins(0.02)
        plt.title(f"COVID-19 cases: {country}")
        fig = plt.figure()
        fig.autofmt_xdate()

        series.plot(marker="o")
        plt.savefig("/tmp/plot.png", bbox_inches="tight")
        return mx

    def random_country_graph(self):
        """
        Generates graph, returns data to create an alert.
        """
        country, data = self.random_country()
        cases_total = self.make_graph(country, data)
        self.media_id = self.upload_image("/tmp/plot.png")
        return {"graph": True, "cases": cases_total, "country": country}
