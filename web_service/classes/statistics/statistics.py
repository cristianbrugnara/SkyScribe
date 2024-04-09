from statistics import pstdev, mean


class Statistics:

    @staticmethod
    def get_mean(feature_array):
        return mean(feature_array)

    @staticmethod
    def get_max(feature_array):
        return max(feature_array)

    @staticmethod
    def get_min(feature_array):
        return min(feature_array)

    @staticmethod
    def get_std(feature_array):
        return pstdev(feature_array,)
