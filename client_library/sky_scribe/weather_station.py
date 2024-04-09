import requests
from datetime import datetime
from typing import Dict, List,Union,Tuple,Any
from .exceptions import *
from pandas import DataFrame
from .sample import Sample
from .utils.cl_helper_functions import weather_json_to_oop,weather_json_to_dataframe,build_date
from .utils.config import URL_BASELINE
from .forecaster import Forecaster


class WeatherStation:
    """
    The class that implements the vast majority of SkyScribe's functions.
    It allows for a wide variety of get, add, delete and update operations on its measurements, which in this context are labeled as 'samples'.
    Additional offered functions include statistic computations, graph plotting and forecasting models creation.
    """
    def __init__(self, id : int, location : str):
        """
        Constructor to build an object The objects are intended to be created with the function get_one_station() and not created directly by the user.
        :param id: The ID associated to the station.
        :param location: The location or address of the station.
        """
        self.__id = id
        self.__loc = location.title()
        self.__models = []

    def __str__(self):
        """
        String representation of the instances. It simply shows the ID and the location.
        :rtype: str
        """
        return f"Weather Station | ID : {self.id} | Address: {self.location}"

    @property
    def location(self):
        return self.__loc

    @property
    def id(self):
        return self.__id

    @property
    def models(self):
        return self.__models

    # SAMPLES FUNCTIONS

    @staticmethod
    def _str_to_date(str_date : str, format = '%Y-%m-%d %H:%M:%S') -> datetime:
        return datetime.strptime(str_date,format)

    def get_all_samples(self, as_dataframe : bool = False, as_dict : bool = False) -> List[Union[Sample,Dict,DataFrame]]:
        """
        Used to get the complete history of measurements done and stored by the stations.
        This can be either a list of :class: `Sample` objects, dictionaries or as a dataframe. One can specify this choice with the following parameters.
        If both are left `False`, `Sample` objects are returned.

        :param as_dataframe: Whether to return the data in a pandas DataFrame.
        :param as_dict: Whether to return the data as python dictionaries.
        :return: List of all samples in the station.
        :rtype: List[Union[Sample,Dict,DataFrame]]
        """

        result = requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/").json()
        if not as_dict and not as_dataframe:
            result = weather_json_to_oop(result)

        if as_dataframe:
            result = weather_json_to_dataframe(result, 'ts')

        return result

    def get_one_sample(self, year : int = 2023, month : int = 11, day : int = 1, hour : int = 1, minute : int = 1,
                       prebuilt_date : datetime = None, as_dataframe : bool = False, as_dict : bool = False) -> Union[Sample,Dict,DataFrame]:
        """
        Function used to access one specific sample, by specifying its date (and time). Can be done by manually writing the time parameters or using a prebuilt date.
        :param year: Year of the date to use.
        :type year: int
        :param month: Month of the date to use.
        :type month: int
        :param day: Day of the month to use.
        :type day: int
        :param hour: Hour of the day.
        :type hour: int
        :param minute: Minute of the hour.
        :type minute: int
        :param prebuilt_date: Date passed instead of specifying each field.
        :type prebuilt_date: datetime
        :param as_dataframe: Whether to return the data in a pandas DataFrame.
        :param as_dict: Whether to return the data as python dictionaries.
        :return: One spacific sample based on the date.
        :rtype: Union[Sample,Dict,DataFrame]
        """

        if prebuilt_date:
            date = prebuilt_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = build_date(year, month, day, hour, minute).strftime('%Y-%m-%d %H:%M:%S')

        request =  requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/{date}")

        if request.status_code == 200:
            result = request.json()
            if not as_dict and not as_dataframe:
                result = weather_json_to_oop(result)
            if as_dataframe:
                result = weather_json_to_dataframe(result, 'ts')
            return result

        elif request.status_code == 404:
            raise NotFoundError(f'Sample associated to {date} not found.')

    def get_range_of_samples(self, year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None, minute_1 : int = None,
                          year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None, minute_2: int = None,
                          prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None,
                                as_dataframe : bool = False, as_dict : bool = False) -> List[Union[Sample,Dict,DataFrame]]:

        """
        Behave similarly to `get_all_samples()` with the difference that we can specify two dates, the starting date and the ending date.
        One can do it in two ways, manually or with prebuilt dates. To avoid argument cluttering, it is suggested to use the second approach.
        Omitting all parameters will make the method behave like `get_all_samples()`.

        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :param as_dataframe: Whether to return the data in a pandas DataFrame.
        :param as_dict: Whether to return the data as python dictionaries.
        :return: List of all samples in the station taken within the specified range.
        :rtype: List[Union[Sample,Dict,DataFrame]]
        """
        if not year_1 and not prebuilt_date_1:
            date1 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/0").text)
        elif prebuilt_date_1:
            date1 = prebuilt_date_1.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date1 = build_date(year_1,month_1,day_1,hour_1,minute_1).strftime('%Y-%m-%d %H:%M:%S')

        if not year_2 and not prebuilt_date_2:
            date2 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/1").text)
        elif prebuilt_date_2:
            date2 = prebuilt_date_2.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date2 = build_date(year_2, month_2, day_2, hour_2, minute_2).strftime('%Y-%m-%d %H:%M:%S')

        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/{date1}/{date2}")

        if request.status_code == 200:
            result = request.json()
            if not as_dict and not as_dataframe:
                result = weather_json_to_oop(result)
            if as_dataframe:
                result = weather_json_to_dataframe(result, 'ts')
            return result

    def get_filtered_samples(self, as_dataframe : bool = False, as_dict : bool = False
                             , **filters : Tuple[Union[float,None], Union[float,None]]) -> List[Union[Sample,Dict,DataFrame]]:
        """
        Allows to retrieve measurements that fit some specified maximum and minimum conditions, the boundaries are included in the search.
        If one of the two boundaries is left as `None` it will behave normally.
        This means that not keyword arguments to the method will make it act like `get_all_samples()`.

        :param as_dataframe: Whether to return the data in a pandas DataFrame.
        :param as_dict: Whether to return the data as python dictionaries.

        :param filters: Keyword arguments that specify the minimum and maximum values of the field. The syntax is <field>=[<min>,<max>]
        :return: List of all samples in the station after filtering.
        :rtype: List[Union[Sample,Dict,DataFrame]]
        """

        query_string = "?"
        for field, range_ in filters.items():
            lower, upper = range_
            if lower is not None:      # >= in percent encoding
                query_string+=f"{field}=%3E%3D{lower}"

            if upper is not None:
                if lower is not None:
                    query_string += '&'  # <= in percent encoding
                query_string+=f"{field}=%3C%3D{upper}"

            if lower is not None or upper is not None:
                query_string+='&'
        query_string = query_string[:-1]
        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/{query_string}")

        if request.status_code == 200:
            result = request.json()
            if not as_dict and not as_dataframe:
                result = weather_json_to_oop(result)
            if as_dataframe:
                result = weather_json_to_dataframe(result, 'ts')
            return result

    def delete_sample(self,  year : int = 2023, month : int = 11, day : int = 1, hour : int = 1, minute : int = 1,
                      prebuilt_date : datetime = None):
        """
        Used to delete a sample based on the date which can be both manually inserted or specified using a datetime object.
        :param year: Year of the date to use.
        :type year: int
        :param month: Month of the date to use.
        :type month: int
        :param day: Day of the month to use.
        :type day: int
        :param hour: Hour of the day.
        :type hour: int
        :param minute: Minute of the hour.
        :type minute: int
        :param prebuilt_date: Date passed instead of specifying each field.
        :type prebuilt_date: datetime
        :return: None if the operations works as expected. Raises an exception otherwise.
        """

        if prebuilt_date:
            date = prebuilt_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = build_date(year, month, day, hour, minute).strftime('%Y-%m-%d %H:%M:%S')

        request = requests.delete(f'{URL_BASELINE}/stations/{self.id}/samples/{date}')
        if request.status_code == 200:
            return
        raise NotFoundError(f'Sample associated to {date} not found.')

    def add_sample(self,year : int = 2023, month : int = 11, day : int = 1, hour : int = 1, minute : int = 1,
                prebuilt_date : datetime = None, **fields : float):
        """
        Used to insert a new measurement by specifying the date and the desired fields, as keywork arguments.
        It is important that a sample associated to that date isn't already present in the station. In that case, one can use `replace_sample()`.

        :param year: Year of the date to use.
        :type year: int
        :param month: Month of the date to use.
        :type month: int
        :param day: Day of the month to use.
        :type day: int
        :param hour: Hour of the day.
        :type hour: int
        :param minute: Minute of the hour.
        :type minute: int
        :param prebuilt_date: Date passed instead of specifying each field.
        :type prebuilt_date: datetime
        :param fields: Keyword arguments representing the value of the field. Generally the values should be numerical, but some stations might measure other type of fields.
        :return: None if the operations works as expected. Raises an exception otherwise.
        """

        if prebuilt_date:
            date = prebuilt_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = build_date(year, month, day, hour, minute).strftime('%Y-%m-%d %H:%M:%S')

        body = {el[0] : fields.get(el[0], 0) for el in fields.items()}

        request = requests.post(f"{URL_BASELINE}/stations/{self.id}/samples/{date}", json = body)

        if request.status_code == 201:
            return
        elif request.status_code == 400:
            return BadRequestError(f'Sample associated to {date} already exists.')

    def replace_sample(self,year : int = 2023, month : int = 11, day : int = 1, hour : int = 1, minute : int = 1,
                prebuilt_date : datetime = None, **fields: float):
        """
        Used to replace an existing sample by specifying the date and the desired fields, as keywork arguments.
        This is used when one needs to completely replace a sample, as the non-specified values will either be set as default (for the values specified in the Blynk table in the documentation) or not be set.
        Thus, if the goal is to simply modify some fields, the right method is `update_sample()`.
        The sample associated to the date must exist, if one desires to add a new sample, use `add_sample()`.

        :param year: Year of the date to use.
        :type year: int
        :param month: Month of the date to use.
        :type month: int
        :param day: Day of the month to use.
        :type day: int
        :param hour: Hour of the day.
        :type hour: int
        :param minute: Minute of the hour.
        :type minute: int
        :param prebuilt_date: Date passed instead of specifying each field.
        :type prebuilt_date: datetime
        :param fields: Keyword arguments representing the value of the field. Generally the values should be numerical, but some stations might measure other type of fields.
        :return: None if the operations works as expected. Raises an exception otherwise.
        """

        if prebuilt_date:
            date = prebuilt_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = build_date(year, month, day, hour, minute).strftime('%Y-%m-%d %H:%M:%S')

        body = {el[0] : fields.get(el[0], 0) for el in fields.items()}

        request = requests.put(f"{URL_BASELINE}/stations/{self.id}/samples/{date}", json=body)

        if request.status_code == 201:
            return
        else:
            raise NotFoundError(f'Sample associated to {date} not found.')

    def update_sample(self,field_to_update : str, value : Any,year : int = 2023, month : int = 11, day : int = 1,
                      hour : int = 1, minute : int = 1,prebuilt_date : datetime = None):

        """
        Used to update or modify a single field of a sample specified using a date.
        The other fields won't be affected.
        :param field_to_update: Name of the field (parameter) to be updated.
        :type field_to_update: str
        :param value: The new value of the field. Generally a number.
        :param year: Year of the date to use.
        :type year: int
        :param month: Month of the date to use.
        :type month: int
        :param day: Day of the month to use.
        :type day: int
        :param hour: Hour of the day.
        :type hour: int
        :param minute: Minute of the hour.
        :type minute: int
        :param prebuilt_date: Date passed instead of specifying each field.
        :type prebuilt_date: datetime
        :return: None if the operations works as expected. Raises an exception otherwise.
        """

        if prebuilt_date:
            date = prebuilt_date.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date = build_date(year, month, day, hour, minute).strftime('%Y-%m-%d %H:%M:%S')

        patch = {'value' : value, 'field' : field_to_update}

        request = requests.patch(f"{URL_BASELINE}/stations/{self.id}/samples/{date}", json = patch)
        if request.status_code == 200:
            return
        else:
            raise NotFoundError(f'Sample associated to {date} not found.')

    # STATISTICS FUNCTIONS

    def get_general_statistics(self, as_dataframe : bool = False) -> List[Dict[str, float]]:
        """
        Used to obtain a complete statistical view of the fields measured by the station.
        Currently available statistics are mean, max, min and population standard deviation.
        :param as_dataframe: Whether to obtain the result as a pandas DataFrame, with the statistic types as rows and fields as columns. A dictionary is provided otherwise
        :return: Statistics provided for each field of the whether station.
        :rtype: List[Dict[str, float]]
        """
        result = requests.get(f"{URL_BASELINE}/stations/{self.id}/statistics/").json()

        if as_dataframe:
            result = DataFrame(result)
        return result

    def _stat(self, stat_type : str, field : str):
        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/statistics/?stat-type={stat_type}&pin={field}")
        if request.status_code == 200:
            return request.json()['result']
        if request.status_code == 400:
            raise NotFoundError(f'Field {field} not present.')

    def mean(self, field : str) -> float:
        """
        Returns mean of all samples for the specified field.
        To get the mean of samples between two dates, use `mean_in_range()`.

        :param field: Field of choice.
        :return: Mean of field.
        :rtype: float
        """

        return self._stat('mean', field)

    def min(self, field : str) -> float:
        """
        Returns min of all samples for the specified field.
        To get the min of samples between two dates, use `min_in_range()`.

        :param field: Field of choice.
        :return: Minimum value of field.
        :rtype: float
        """

        return self._stat('min', field)

    def max(self, field : str) -> float:
        """
        Returns maximum of all samples for the specified field.
        To get the max of samples between two dates, use `max_in_range()`.

        :param field: Field of choice.
        :return: Maximum value of field.
        :rtype: float
        """

        return self._stat('max', field)

    def std(self, field : str) -> float:
        """
        Returns population standard deviation of all samples for the specified field.
        To get the std of samples between two dates, use `std_in_range()`.

        :param field: Field of choice.
        :return: Population standard deviation of field.
        :rtype: float
        """

        return self._stat('std', field)

    def get_general_statistics_in_range(self, year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None, minute_1 : int = None,
                          year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None, minute_2: int = None,
                          prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None, as_dataframe : bool = False) -> List[Dict[str, float]]:
        """
        Used to obtain a complete statistical view of the fields measured by the station within a certain time period.
        Currently available statistics are mean, max, min and population standard deviation.

        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :param as_dataframe: Whether to obtain the result as a pandas DataFrame, with the statistic types as rows and fields as columns. A dictionary is provided otherwise
        :return: Statistics provided for each field of the whether station from sampled within a date range.
        :rtype: List[Dict[str, float]]
        """

        if not year_1 and not prebuilt_date_1:
            date1 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/0").text)
        elif prebuilt_date_1:
            date1 = prebuilt_date_1.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date1 = build_date(year_1,month_1,day_1,hour_1,minute_1).strftime('%Y-%m-%d %H:%M:%S')

        if not year_2 and not prebuilt_date_2:
            date2 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/1").text)
        elif prebuilt_date_2:
            date2 = prebuilt_date_2.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date2 = build_date(year_2, month_2, day_2, hour_2, minute_2).strftime('%Y-%m-%d %H:%M:%S')

        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/statistics/{date1}/{date2}")
        if request.status_code == 404:
            raise NotFoundError('Station might not offer data reading.')

        result = request.json()

        if as_dataframe:
            result = DataFrame(result)
        return result

    def _stat_in_range(self, stat_type : str, field : str, year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None,
                      minute_1 : int = None,year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None,
                      minute_2: int = None,prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None) -> float:

        if not year_1 and not prebuilt_date_1:
            date1 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/0").text)
        elif prebuilt_date_1:
            date1 = prebuilt_date_1.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date1 = build_date(year_1,month_1,day_1,hour_1,minute_1).strftime('%Y-%m-%d %H:%M:%S')

        if not year_2 and not prebuilt_date_2:
            date2 = self._str_to_date(requests.get(f"{URL_BASELINE}/stations/{self.id}/samples/1").text)
        elif prebuilt_date_2:
            date2 = prebuilt_date_2.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date2 = build_date(year_2, month_2, day_2, hour_2, minute_2).strftime('%Y-%m-%d %H:%M:%S')

        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/statistics/{date1}/{date2}"
                               f"?stat-type={stat_type}&pin={field}")

        if request.status_code == 200:
            return request.json()['result']

        if request.status_code == 400:
            raise BadRequestError(f"Field {field} not present.")
        raise NotFoundError(f"Data not present.")

    def mean_in_range(self, field : str,year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None,
                      minute_1 : int = None,year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None,
                      minute_2: int = None, prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None) -> float:

        """
        Returns mean of samples collected during the provided time period for the specified field.
        To reduce argument cluttering this function was separated from `mean()` which computed the statistic on all samples.

        :param field: Field of choice.
        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :return: Mean of field within the time period.
        :rtype: float
        """

        return self._stat_in_range('mean',field,year_1,month_1,day_1,hour_1,minute_1,year_2,
                                   month_2,day_2,hour_2,minute_2,prebuilt_date_1,prebuilt_date_2)

    def min_in_range(self, field : str, year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None,
                      minute_1 : int = None,year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None,
                      minute_2: int = None,prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None) -> float:
        """
        Returns minimum of samples collected during the provided time period for the specified field.
        To reduce argument cluttering this function was separated from `min()` which computed the statistic on all samples.

        :param field: Field of choice.
        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :return: Minimum value of field within the time period.
        :rtype: float
        """

        return self._stat_in_range('min', field, year_1, month_1, day_1, hour_1, minute_1, year_2,
                                   month_2, day_2, hour_2, minute_2, prebuilt_date_1, prebuilt_date_2)

    def max_in_range(self, field : str, year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None,
                      minute_1 : int = None,year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None,
                      minute_2: int = None, prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None) -> float:
        """
        Returns maximum of samples collected during the provided time period for the specified field.
        To reduce argument cluttering this function was separated from `max()` which computed the statistic on all samples.

        :param field: Field of choice.
        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :return: Maximum value of field within the time period.
        :rtype: float
        """

        return self._stat_in_range('max',field,year_1,month_1,day_1,hour_1,minute_1,year_2,
                                   month_2,day_2,hour_2,minute_2,prebuilt_date_1,prebuilt_date_2)

    def std_in_range(self, field : str,year_1 : int = None, month_1 : int = None, day_1 : int = None, hour_1 : int = None,
                      minute_1 : int = None, year_2: int = None, month_2: int = None, day_2: int = None, hour_2: int = None,
                      minute_2: int = None, prebuilt_date_1: datetime = None, prebuilt_date_2 : datetime = None) -> float:
        """
        Returns population standard deviation of samples collected during the provided time period for the specified field.
        To reduce argument cluttering this function was separated from `std()` which computed the statistic on all samples.

        :param field: Field of choice.
        :param year_1: Year of the starting date.
        :param month_1: Month of the starting date.
        :param day_1: Day of the starting date.
        :param hour_1: Hour of the starting date.
        :param minute_1: Minute of the starting date.
        :param year_2: Year of the ending date.
        :param month_2: Month of the ending date.
        :param day_2: Day of the ending date.
        :param hour_2: Hour of the ending date.
        :param minute_2: Minute of the ending date.
        :param prebuilt_date_1: Starting date passed instead of specifying each field.
        :type prebuilt_date_1: datetime
        :param prebuilt_date_2: Ending date passed instead of specifying each field.
        :type prebuilt_date_2: datetime
        :return: Standard deviation of field within the time period.
        :rtype: float
        """

        return self._stat_in_range('std',field,year_1,month_1,day_1,hour_1,minute_1,year_2,
                                   month_2,day_2,hour_2,minute_2,prebuilt_date_1,prebuilt_date_2)

    # GRAPHS

    def _plot(self,graph_type : str ,field : str, file_path : str, field_2 : str = None):
        fields_input = f"{field}" if field_2 is None else f"{field}/{field_2}"
        request = requests.get(f"{URL_BASELINE}/stations/{self.id}/graphs/{graph_type}/{fields_input}")
        if request.status_code == 200:
            with open(f"{file_path}/{graph_type}_of_{fields_input.replace('/','-')}.jpg", 'wb') as f:
                f.write(request.content)
        elif request.status_code == 404:
            raise NotFoundError(f'Field "{field} not found."')

    def boxplot(self, field :  str, file_path : str):
        """
        Plots a boxplot of the specified field using the Seaborn library. It then creates a .jpg file in the `file_path` to access the graph.

        :param field: Field of choice.
        :param file_path: Path where the image will be saved.
        :rtype: None
        """

        self._plot('boxplot',field, file_path)

    def histogram(self, field: str, file_path: str):
        """
        Plots a histogram of the specified field using the Seaborn library. It then creates a .jpg file in the `file_path` to access the graph.

        :param field: Field of choice.
        :param file_path: Path where the image will be saved.
        :rtype: None
        """
        self._plot('histogram', field, file_path)

    def scatterplot(self, field_1 : str, field_2 : str, file_path : str):
        """
        Plots a scatterplot of the specified fields using the Seaborn library. It then creates a .jpg file in the `file_path` to access the graph.
        `field_1` and `field_2` must be provided.

        :param field_1: First field of choice. Will be associated to the X-axis.
        :param field_2: Second field of choice. Will be associated to the Y-axis.
        :param file_path: Path where the image will be saved.
        :rtype: None
        """
        self._plot('scatterplot', field_1,file_path,field_2)

    def lineplot(self,file_path : str, field_1 : str, field_2 : str = None):
        """
        Plots a boxplot of the specified field(s) using the Seaborn library. It then creates a .jpg file in the `file_path` to access the graph.
        `field_1` must be always provided. If `field_2` isn't provided only one line will be plotted.

        :param field_1: First field of choice.
        :param field_2: Second field of choice. If provided will be plotted as a second line.
        :param file_path: Path where the image will be saved.
        :rtype: None
        """
        if field_2 is None:
            self._plot('lineplot',field_1,file_path)
        else:
            self._plot('lineplot', field_1,file_path,field_2)

    # FORECASTING

    def create_model(self, input_fields : List[str] = None, output_fields : List[str] = None,
                     input_steps = 300,horizon_steps : int = 250, optimizer : Union[str] = 'adam',
                     loss : Union[str] = 'huber') -> Forecaster:

        """
        Used to create a LSTM recurrent neural network using TensorFlow.
        It is necessary to provide the specifications about what the model uses to train and what it forecasts.
        This method is the first step to utilize the forecasting options of the library.
        NOTE: High `horizon_steps` values and bad combinations of input and output fields might heavily impact the performance.

        :param input_fields: List of the fields the model takes as input in order to train. If left to `None`, all will be used.
        :type input_fields: List[str]
        :param output_fields: List of the fields the model will predict. If left to `None`, all will be predicted.
        :type output_fields: List[str]
        :param input_steps: Number of samples the model uses to make a prediction.
        :param horizon_steps: Total number of samples to predict.
        :param optimizer: Optimizer that the model will use. Suggested options are Adam (default) and SGD.
        :param loss: Loss function the model will optimize. Suggested options are Huber (default), MSE and MAE.
        :return: Forecaster
        """

        body = locals()
        body.pop('self')

        create = requests.post(f"{URL_BASELINE}/stations/{self.id}/forecast/models", json = body)

        model_id = len(self.__models)

        model = Forecaster(model_id ,self.id)

        self.__models.append(model)
        return model

    def delete_model(self, id : int):
        """
        Used to delete a model. To get the ID of the model one can either use `WeatherStation.models` indexes or `Forecaster.id`.

        :param id: Id of the model.
        :return: None, but prints a message if the model was successfully deleted; alternatively raises an exception.
        :rtype: None
        """

        if id<0 or id>=len(self.__models):
            raise NotFoundError(f"The station has no model with ID {id}.")

        model = str(self.__models.pop(id))
        delete = requests.delete(f"{URL_BASELINE}/stations/{self.id}/forecast/models/{id}")
        if delete.status_code == 200:
            for i in range(id,len(self.__models)):
                self.__models[i]._update_id(i)

            print(f"Deleted the following model: \n{model}")