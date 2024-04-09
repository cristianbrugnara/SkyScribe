import requests
from typing import Dict, List
from .exceptions import NotTrainedError
from pandas import DataFrame
from .utils.config import URL_BASELINE
from .utils.cl_helper_functions import weather_json_to_oop,weather_json_to_dataframe

class Forecaster:
    """
    Model class of the library.
    Offers the possibility of training the model, predicting records or updating the information about the model.
    To delete a model use `WeatherStation.delete_model()` and delete the object.
    """
    def __init__(self, model_id : int, station_id : int):
        """
        Constructor of the model. The object is supposed to be created by a `WeatherStation` object.
        :param model_id: Integer ID assigned to the model.
        :param station_id: Integer ID associated to the native station.
        """
        self.__id = model_id
        self.__station = station_id
        self.__trained = False

    def __str__(self):
        """
        Offers a comfortable way to check the specifics of the model, such as its layers and their input and output shapes.
        :return: String representation of the model.

        :rtype: str
        """
        my_str = requests.get(f"{URL_BASELINE}/stations/{self.__station}/forecast/models/{self.__id}").text
        return my_str

    @property
    def id(self):
        return self.__id

    @property
    def station_id(self):
        return self.__station

    def _update_id(self, new_id : int):
        self.__id = new_id

    def train(self, epochs : int = 5, batch_size : int = 32):
        """
        Used to prepare the model for predictions. It might take some time.
        :param epochs: Epochs the model should train for (NOTE: Early Stopping will stop the process if convenient).
        :param batch_size: Size of the training batches. Usually smaller batches lead to longer training times and better results.
        :return: None. Prints a confirmation of training at the end.
        :rtype: None
        """
        body = locals()
        body.pop('self')
        request = requests.post(f"{URL_BASELINE}/stations/{self.station_id}/forecast/models/{self.__id}/train", json=body)
        if request.status_code == 200:
            self.__trained = True
            print(f"Model {self.id} of station {self.station_id} is ready for predictions")
            return

    def forecast(self, as_dataframe : bool = False, as_dict : bool = False):
        """
        Used to get the predictions. If `as_dataframe` and `as_dict` parameters are left None, the result will be a list of `Sample` objects.

        :param as_dataframe: Whether to return the predictions as a pandas DataFrame.
        :param as_dict: Whether to return the predictions as a list of dictionaries.
        :return: horizon_steps predictions according to the model output_fields.
        :rtype: List[Sample,Dict,DataFrame]
        """
        if not self.__trained:
            raise NotTrainedError(f"Model {self.id} of station {self.station_id} has not been trained yet!"
                                  f"Please execute model.train() first.")

        request = requests.get(f'{URL_BASELINE}/stations/{self.station_id}/forecast/models/{self.id}/predict')

        if request.status_code == 200:
            result = request.json()

        if not as_dict and not as_dataframe:
            result = weather_json_to_oop(result)
        if as_dataframe:
            result = weather_json_to_dataframe(result, 'ts')
        return result

    def update_model_fields(self, input_fields : List[str] = None, output_fields : List[str] = None):
        """
        Used to change the input or output fields of a model.
        Requires the model to be trained after.

        :param input_fields: Fields the model uses to train. If None all fields will be used.
        :param output_fields: Fields the model predicts. If None all fields will be predicted.
        :rtype: None
        """

        body = {"input_fields" : input_fields, "output_fields" : output_fields}

        self.__trained = False
        update = requests.patch(f'{URL_BASELINE}/stations/{self.station_id}/forecast/models/{self.id}', json = body)