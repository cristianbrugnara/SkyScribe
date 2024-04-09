from .graph import Graph
from typing import Tuple
from seaborn import scatterplot
from matplotlib.pyplot import figure, gca


class ScatterPlot(Graph):
    def __init__(self, data, data2, type_measurements, type_measurements2, figsize: Tuple[int, int] = (10, 10)):
        Graph.__init__(self, data, type_measurements, figsize)
        self.data2 = data2
        self.type_measurements2 = type_measurements2

    def plot_graph(self):
        fig = figure(figsize=self.figsize)
        scatterplot(x=self.data, y=self.data2)
        ax = gca()

        ax.set_title(f"Scatter plot of: {self.type_measurements} and {self.type_measurements2}")
        ax.set_xlabel(f"{self.type_measurements}")
        ax.set_ylabel(f"{self.type_measurements2}")

        return fig
