from .graph import Graph
from typing import Tuple
from seaborn import lineplot
from matplotlib.pyplot import figure, gca
import matplotlib.pyplot as plt


class LinePlot(Graph):
    def __init__(self, data, data2, type_measurements: str, type_measurements2: str, type_measurements3=None, data3=None, figsize: Tuple[int ,int] = (10, 10), ):
        Graph.__init__(self, data, type_measurements, figsize )
        self.data2 = data2
        self.data3 = data3
        self.type_measurements2 = type_measurements2
        self.type_measurements3 = type_measurements3

    def plot_graph(self):
        fig = figure(figsize=self.figsize)
        lineplot(x=self.data2, y=self.data)
        if self.data3 is not None and self.type_measurements3 is not None:
            fig, ax1 = plt.subplots(figsize=self.figsize)
            ax2 = ax1.twinx()

            line1 = ax1.plot(self.data2, self.data, label=self.type_measurements)
            line2 = ax2.plot(self.data2, self.data3, label=self.type_measurements3, color='tab:orange')

            ax1.set_xlabel('Time')
            ax1.set_ylabel(self.type_measurements)
            ax2.set_ylabel(self.type_measurements3)

            lines = line1 + line2
            labels = [l.get_label() for l in lines]
            ax1.legend(lines, labels, loc='upper left')

            ax1.set_title(f"Line plot of: {self.type_measurements} and {self.type_measurements3}")

            return fig

        ax = gca()

        ax.set_title(f"line plot of: {self.type_measurements}")
        ax.set_ylabel(f"{self.type_measurements}")
        ax.set_xlabel("Time")

        return fig