# I apologize in advance if human rights were violated in this code

from datetime import datetime


class Sample:
    def __init__(self, date : datetime, **params):
        self._modifiable = True
        self.ts = date
        self.__dict__.update((key,value) for key,value in params.items())
        self.__dict__['ts'] = date

        self._modifiable = False

    @property
    def available_fields(self):
        lst = list(self.__dict__.keys())
        lst.remove('_modifiable')
        return lst

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        raise AttributeError(f"Attribute {item} not present in the sample.")

    # so I can prevent the set operation without defining properties since the arguments can change,
    # and this object is just a physical representation.To update a sample one can use update_sample() of WeatherStation

    def __setattr__(self, key, value):
        if key == '_modifiable':
            super().__setattr__(key,value)

        elif not self._modifiable:
            raise AttributeError("Sample object cannot be modified manually.")

    def __str__(self):
        pairs = self.__dict__
        my_str = f"Measurement of {pairs['ts']} "

        pairs.pop('_modifiable')
        pairs.pop('ts')
        if len(pairs) == 0:
            my_str+="no measurement "

        for el in pairs.items():
            my_str+=f"| {el[0]} : {el[1]} "
        return my_str[:-1]
