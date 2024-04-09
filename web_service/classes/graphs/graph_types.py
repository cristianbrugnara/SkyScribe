from enum import Enum, auto


class GraphType(Enum):
    BOXPLOT = ['one_var', auto()]
    SCATTERPLOT = ['two_var', auto()]
    LINEPLOT = ['one_var', 'two_var', auto()]
    HISTOGRAM = ['one_var', auto()]
