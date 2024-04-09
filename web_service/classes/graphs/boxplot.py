from .graph import Graph
from typing import Tuple
from seaborn import boxplot
from matplotlib.pyplot import figure, gca


class Boxplot(Graph):
    def __init__(self, data, type_measurements: str, figsize: Tuple[int ,int] = (10, 10)):
        Graph.__init__(self, data, type_measurements, figsize )

    def plot_graph(self):
        fig = figure(figsize=self.figsize)
        boxplot(data=self.data)

        ax = gca()

        ax.set_title(f"Box plot of: {self.type_measurements}")
        ax.set_ylabel(f"{self.type_measurements}")

        return fig


