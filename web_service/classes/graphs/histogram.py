from .graph import Graph
from typing import Tuple
from seaborn import histplot
from matplotlib.pyplot import figure, gca


class Histogram(Graph):
    def __init__(self, data, type_measurements: str, figsize: Tuple[int ,int] = (10, 10)):
        Graph.__init__(self, data, type_measurements, figsize)

    def plot_graph(self):
        fig = figure(figsize=self.figsize)
        histplot(data=self.data, kde= True)

        ax = gca()

        ax.set_title(f"Histogram of: {self.type_measurements}")
        ax.set_xlabel(f"{self.type_measurements}")

        return fig
