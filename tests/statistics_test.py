from web_service.classes.statistics.statistics import Statistics
from statistics import StatisticsError
from math import sqrt


class TestStatistics:
    empty = []

    one_value = [704]

    dicrete = [1,2,3,4,5]

    floats = [-3.4,1.222, 5.77, 2.3001]

    inf = [3,float('inf')]
    minf = [3,float('-inf')]
    both_inf = [float('inf'), float('-inf')]

    def test_get_mean_0(self):
        error = False
        try:
            Statistics.get_mean(self.empty)
        except StatisticsError:
            error = True

        assert error

    def test_get_mean_1(self):
        res = Statistics.get_mean(self.one_value)

        assert res == self.one_value[0]

    def test_get_mean_2(self):
        res = Statistics.get_mean(self.dicrete)

        assert res == 3

    def test_get_mean_3(self):
        res = Statistics.get_mean(self.floats)

        assert round(res,6) == round(1.473025,6)

    def test_get_mean_4(self):
        res = Statistics.get_mean(self.inf)

        assert round(res,6) == float('inf')

    def test_get_mean_5(self):
        res = Statistics.get_mean(self.minf)

        assert round(res, 6) == float('-inf')

    def test_get_mean_6(self):
        res = Statistics.get_mean(self.both_inf)

        assert str(res) == 'nan'

    def test_get_max_0(self):
        error = False
        try:
            Statistics.get_max(self.empty)
        except ValueError:
            error = True

        assert error

    def test_get_max_1(self):
        res = Statistics.get_max(self.one_value)
        assert res == self.one_value[0]

    def test_get_max_2(self):
        res = Statistics.get_max(self.dicrete)

        assert res == 5

    def test_get_max_3(self):
        res = Statistics.get_max(self.floats)

        assert res == 5.77

    def test_get_max_4(self):
        res = Statistics.get_max(self.inf)

        assert res == float('inf')

    def test_get_min_0(self):
        error = False
        try:
            Statistics.get_min(self.empty)
        except ValueError:
            error = True

        assert error

    def test_get_min_1(self):
        res = Statistics.get_min(self.one_value)
        assert res == self.one_value[0]

    def test_get_min_2(self):
        res = Statistics.get_min(self.dicrete)

        assert res == 1

    def test_get_min_3(self):
        res = Statistics.get_min(self.floats)

        assert res == -3.4

    def test_get_min_4(self):
        res = Statistics.get_min(self.minf)

        assert res == float('-inf')

    def test_get_std_0(self):
        error = False
        try:
            Statistics.get_std(self.empty)
        except StatisticsError:
            error = True

        assert error

    def test_get_std_1(self):
        res = Statistics.get_std(self.one_value)
        assert res == 0

    def test_get_std_2(self):
        res = Statistics.get_std(self.dicrete)

        assert res == sqrt(2)

    def test_get_std_3(self):
        res = Statistics.get_std(self.floats)

        assert round(res,6) == round(3.2770960242073,6)

    def test_get_std_4(self):
        error = False
        try:
            Statistics.get_std(self.inf)
        except OverflowError :
            error = True

        assert error
