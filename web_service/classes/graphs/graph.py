from abc import ABC,abstractmethod
import matplotlib.pyplot as plt
from typing import Iterable,Tuple


class Graph(ABC):
    def __init__(self, data, type_measurements: str, figsize: Tuple[int ,int] = (10 ,10)):
        self.__data = data
        self.__figsize = figsize
        self.__fig, self.__ax = plt.subplots()
        self.__type_measurements = type_measurements

    @property
    def data(self):
        return self.__data

    @property
    def figsize(self):
        return self.__figsize

    @property
    def fig(self):
        return self.__fig

    @property
    def ax(self):
        return self.__ax

    @property
    def type_measurements(self):
        return self.__type_measurements

    @abstractmethod
    def plot_graph(self):
        pass
