from web_service.classes.weather_station.weather_station import WeatherStation
from datetime import datetime

# NEEDS THE CONTAINER TO BE RUNNING (or another way to access mongo)

# This used to test the WeatherStation(and the WeatherData as they were strictly related) classes

# I instantiate a WeatherStation object at each test to keep the environment fresh


class TestWeatherStation:
    STATION_INDEX = 0

    wrong_date = datetime(2023, 12, 30, 12, 4)
    existing_inner_date = datetime(2023,11,13,12,30)

    def test_init_0(self):
        st = WeatherStation(self.STATION_INDEX)
        assert st.id == 0

    def test_init_1(self):
        st = WeatherStation(self.STATION_INDEX)
        assert st.location.lower() == 'lugano'

    def test_init_2(self):
        st = WeatherStation(self.STATION_INDEX)
        assert len(st.models) == 0

    def test_start_date(self):
        st = WeatherStation(self.STATION_INDEX)
        assert st.start.strftime("%Y-%m-%d %H:%M:%S") == '2023-11-12 18:02:00'

    def test_end_date(self):
        st = WeatherStation(self.STATION_INDEX)
        assert st.end.strftime("%Y-%m-%d %H:%M:%S") == '2023-11-25 11:39:00'

    def test_get_all_samples_0(self):
        st = WeatherStation(self.STATION_INDEX)
        history = st.get_measurements_by_date_range()

        difference = int((st.end-st.start).total_seconds()/60) + 1  # minutes of difference + 1

        assert len(history) == difference

    def test_get_all_samples_1(self):
        st = WeatherStation(self.STATION_INDEX)
        history = st.get_measurements_by_date_range()

        assert history[0]['ts'] == st.start

    def test_get_all_samples_2(self):
        st = WeatherStation(self.STATION_INDEX)
        history = st.get_measurements_by_date_range()

        assert history[-1]['ts'] == st.end

    def test_get_measurement_by_date_0(self):
        st = WeatherStation(self.STATION_INDEX)

        target = st.get_measurement_by_date(date=st.start)
        assert target['ts'] == st.start

    def test_get_measurement_by_date_1(self):
        st = WeatherStation(self.STATION_INDEX)

        target = st.get_measurement_by_date(date=st.end)
        assert target['ts'] == st.end

    def test_get_measurement_by_date_2(self):
        st = WeatherStation(self.STATION_INDEX)

        inner_date = self.existing_inner_date

        target = st.get_measurement_by_date(inner_date)
        assert target['ts'] == inner_date

    def test_get_measurement_by_date_3(self):
        st = WeatherStation(self.STATION_INDEX)

        wrong_date = datetime(2023, 12, 30, 12, 4)
        # right after the last one

        target = st.get_measurement_by_date(wrong_date)
        assert target is None

    def test_get_measurement_by_date_4(self):
        st = WeatherStation(self.STATION_INDEX)

        wrong_date = datetime(2023, 11, 12, 18, 1)
        # right before the first one

        target = st.get_measurement_by_date(wrong_date)
        assert target is None

    # giving it no output was already tested in the get all samples
    def test_get_measurements_by_date_range_0(self):
        st = WeatherStation(self.STATION_INDEX)
        date1 = datetime(2023,11,13,12,30)
        date2 = datetime(2023,11,13,12,55)

        history = st.get_measurements_by_date_range(date1,date2)

        difference = int((date2 - date1).total_seconds() / 60) + 1

        assert len(history) == difference

    def test_get_measurements_by_date_range_1(self):
        st = WeatherStation(self.STATION_INDEX)
        date1 = datetime(2023, 11, 13, 12, 30)
        date2 = datetime(2023, 11, 13, 12, 55)

        date1_sample = st.get_measurement_by_date(date1,which_fields={'ts' : 1})
        date2_sample = st.get_measurement_by_date(date2,which_fields={'ts' : 1})

        history = st.get_measurements_by_date_range(date1,date2,which_fields={'ts' : 1})

        assert date1_sample == history[0] and date2_sample == history[-1]

    def test_get_measurements_by_date_range_2(self):
        st = WeatherStation(self.STATION_INDEX)
        date1 = datetime(2023, 11, 13, 12, 30)
        date2 = datetime(2023, 11, 13, 12, 55)

        valid = True

        history = st.get_measurements_by_date_range(date1, date2, which_fields={'ts': 1})

        for el in history:
            if el['ts'] < date1 or el['ts'] > date2:
                valid = False

        assert valid

    def test_get_measurements_by_date_range_3(self):
        st = WeatherStation(self.STATION_INDEX)
        date1 = datetime(2023, 11, 13, 12, 30)
        date2 = datetime(2023, 11, 13, 12, 55)

        history = st.get_measurements_by_date_range(date2, date1, which_fields={'ts': 1})

        assert history is None

    def test_get_measurements_by_date_range_4(self):
        st = WeatherStation(self.STATION_INDEX)
        date1 = datetime(2023, 11, 13, 12, 30)

        history = st.get_measurements_by_date_range(date1, date1)
        target = st.get_measurement_by_date(date1)

        assert history == [target]

    def test_get_measurement_mongo_filtered_0(self):
        st = WeatherStation(self.STATION_INDEX)

        MAX_T, MIN_T = 25,20
        MIN_H_NOT_IN = 50

        filter = {
            'temp_c' : {'$gte' : MIN_T, '$lte' : MAX_T},
            'humidity' : {'$gt' : MIN_H_NOT_IN}
        }

        filtered_samples = st.get_measurement_mongo_filtered(filter)

        temperatures = [el['temp_c'] for el in filtered_samples]
        humidity = [el['humidity'] for el in filtered_samples]

        assert min(temperatures) >= MIN_T and max(temperatures) <= MAX_T and min(humidity) > MIN_H_NOT_IN

    def test_get_measurement_mongo_filtered_1(self):
        st = WeatherStation(self.STATION_INDEX)
        MAX_T = -30
        filter = {'temp_c': {'$lte': MAX_T}}

        filtered_samples = st.get_measurement_mongo_filtered(filter)

        assert filtered_samples is None

    def test_get_measurement_mongo_filtered_2(self):
        st = WeatherStation(self.STATION_INDEX)
        MAX_T, MIN_T = 100, 0
        filter = {'temp_c': {'$gte': MIN_T, '$lte': MAX_T}}

        filtered_samples = st.get_measurement_mongo_filtered(filter)

        all_samples = st.get_measurements_by_date_range()

        assert filtered_samples == all_samples

    def test_get_measurement_mongo_filtered_3(self):
        st = WeatherStation(self.STATION_INDEX)
        filter = {}

        filtered_samples = st.get_measurement_mongo_filtered(filter)

        all_samples = st.get_measurements_by_date_range()

        assert filtered_samples == all_samples

    def test_update_measurement_field_by_date_0(self):
        FIELD = 'temp_c'
        st = WeatherStation(0)
        date1 = datetime(2023, 11, 13, 12, 30)

        target = st.get_measurement_by_date(date1)

        old_value = target[FIELD]

        replace = old_value + 1

        st.update_measurement_field_by_date(date1, replace, FIELD)

        new_value = st.get_measurement_by_date(date1)[FIELD]

        st.update_measurement_field_by_date(date1, old_value, FIELD)  # reset it

        assert new_value == replace

    def test_update_measurement_field_by_date_1(self):
        st = WeatherStation(self.STATION_INDEX)

        wrong_date = self.wrong_date

        attempt = st.update_measurement_field_by_date(wrong_date,600,'temp_c')

        assert attempt is None

    def test_update_measurement_field_by_date_2(self):
        st = WeatherStation(self.STATION_INDEX)

        start_date = st.start
        new_date = datetime(2023,11,12,18,1) # the minute before

        st.update_measurement_field_by_date(start_date, value=new_date, field='ts')

        difference = int((start_date - st.start).total_seconds() / 60)

        st.update_measurement_field_by_date(new_date, value=start_date, field='ts')

        assert difference == 1

    def test_update_measurement_field_by_date_3(self):
        st = WeatherStation(self.STATION_INDEX)

        end_date = st.end
        new_date = datetime(2023,11,25,11,40)

        st.update_measurement_field_by_date(end_date, value=new_date, field='ts')

        difference = int((st.end - end_date).total_seconds() / 60)

        st.update_measurement_field_by_date(new_date, value=end_date, field='ts')

        assert difference == 1

    def test_add_measurement_0(self):
        st = WeatherStation(self.STATION_INDEX)

        new_date = datetime(2023,11,12,17,1)

        st.add_measurement(new_date)

        sample = st.get_measurement_by_date(new_date)

        st.delete_sample_by_date(new_date)

        assert sample is not None

    def test_add_measurement_1(self):
        FIELD_VALUES = {'temp_c' : -1, 'humidity' : 55}
        st = WeatherStation(self.STATION_INDEX)

        new_date = datetime(2023,11,12,17,1)

        st.add_measurement(new_date, **FIELD_VALUES)

        sample = st.get_measurement_by_date(new_date)

        st.delete_sample_by_date(new_date)

        check = True
        for field in FIELD_VALUES:
            if sample[field] != FIELD_VALUES[field]:
                check=False

        assert check

    def test_add_measurement_2(self):
        st = WeatherStation(self.STATION_INDEX)

        new_date = datetime(2023,11,12,17,1)

        st.add_measurement(new_date)

        sample = st.get_measurement_by_date(new_date)

        st.delete_sample_by_date(new_date)

        # check that all have a default value of 0
        values_of_fields = set(sample.values())
        assert values_of_fields == {0, new_date} or values_of_fields == {new_date, 0}

    def test_add_measurement_3(self):
        st = WeatherStation(self.STATION_INDEX)

        new_date = datetime(2023,11,12,17,1)

        st.add_measurement(new_date, n_of_dogs = 2)   # non default parameter

        sample = st.get_measurement_by_date(new_date)

        st.delete_sample_by_date(new_date)

        assert sample['n_of_dogs'] == 2

    def test_add_measurement_4(self):
        st = WeatherStation(self.STATION_INDEX)

        existing_date = self.existing_inner_date

        attempt = st.add_measurement(existing_date)

        assert attempt == 400

    def test_add_measurement_5(self):
        st = WeatherStation(self.STATION_INDEX)
        pre_length = len(st.get_measurements_by_date_range())

        new_date = datetime(2024,11,12,17,1)

        st.add_measurement(new_date)

        post_length = len(st.get_measurements_by_date_range())

        st.delete_sample_by_date(new_date)

        assert pre_length == post_length - 1

    def test_delete_sample_by_date_0(self):
        st = WeatherStation(self.STATION_INDEX)

        wrong_date = self.wrong_date

        attempt = st.delete_sample_by_date(wrong_date)
        assert attempt is None

    def test_delete_sample_by_date_1(self):
        st = WeatherStation(self.STATION_INDEX)

        existing_date = datetime(2023, 11, 13, 12, 30)
        pre_delete = st.get_measurement_by_date(existing_date)  # to rebuild it
        pre_delete.pop('ts')

        st.delete_sample_by_date(existing_date)

        query = st.get_measurement_by_date(existing_date)

        st.add_measurement(existing_date, **pre_delete)

        assert query is None

    def test_delete_sample_by_date_2(self):
        st = WeatherStation(self.STATION_INDEX)

        first_date = st.start
        second_date = datetime(2023,11,12,18,3)
        pre_delete = st.get_measurement_by_date(first_date)
        pre_delete.pop('ts')

        st.delete_sample_by_date(first_date)

        query = st.get_measurement_by_date(first_date)

        new_first_date = st.start

        st.add_measurement(first_date, **pre_delete)

        assert query is None and second_date == new_first_date

    def test_delete_sample_by_date_3(self):
        st = WeatherStation(self.STATION_INDEX)

        last_date = st.end
        second_tl_date = datetime(2023,11,25,11,38)
        pre_delete = st.get_measurement_by_date(last_date)
        pre_delete.pop('ts')

        st.delete_sample_by_date(last_date)

        query = st.get_measurement_by_date(last_date)

        new_last_date = st.end

        st.add_measurement(last_date, **pre_delete)

        assert query is None and second_tl_date == new_last_date

    def test_delete_sample_by_date_4(self):
        st = WeatherStation(self.STATION_INDEX)
        pre_length = len(st.get_measurements_by_date_range())

        existing_date = datetime(2023, 11, 13, 12, 30)
        pre_delete = st.get_measurement_by_date(existing_date)
        pre_delete.pop('ts')

        st.delete_sample_by_date(existing_date)

        post_length = len(st.get_measurements_by_date_range())

        st.add_measurement(existing_date, **pre_delete)

        assert pre_length == post_length + 1

    def test_update_measurement_by_date_0(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD_VALUES = {'rssi' : -2, 'pressure_mp1' : 99}

        existing_date = st.start

        pre_update = st.get_measurement_by_date(existing_date)
        pre_update.pop('ts')

        st.update_measurement_by_date(existing_date, **FIELD_VALUES)

        sample = st.get_measurement_by_date(existing_date)

        st.update_measurement_by_date(existing_date, **pre_update)

        check = True
        for field in FIELD_VALUES:
            if sample[field] != FIELD_VALUES[field]:
                check = False

        assert check

    def test_update_measurement_by_date_1(self):
        st = WeatherStation(self.STATION_INDEX)

        existing_date = st.start

        pre_update = st.get_measurement_by_date(existing_date)
        pre_update.pop('ts')

        st.update_measurement_by_date(existing_date)

        sample = st.get_measurement_by_date(existing_date)

        st.update_measurement_by_date(existing_date, **pre_update)

        values_of_fields = set(sample.values())
        assert values_of_fields == {0, existing_date} or values_of_fields == {existing_date, 0}

    def test_update_measurement_by_date_2(self):
        st = WeatherStation(self.STATION_INDEX)

        wrong_date = self.wrong_date

        attempt = st.update_measurement_by_date(wrong_date)

        assert attempt is None

    def test__get_feature_array_0(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD = 'temp_c'

        my_array = st._get_feature_array(FIELD)

        assert len(my_array) == len(st.get_measurements_by_date_range())

    def test__get_feature_array_1(self):
        st = WeatherStation(self.STATION_INDEX)     # to check if the values are the right ones
        FIELD = 'temp_c'                            # we could get all samples and create a list of the field
                                                    # but that's literally what feature_array does

        my_array = st._get_feature_array(FIELD)
        mean = sum(my_array) / len(my_array)

        assert round(mean,6) == round(st.mean(FIELD),6) and max(my_array) == st.max(FIELD) and min(my_array) == st.min(FIELD)

    def test__get_feature_array_2(self):
        st = WeatherStation(self.STATION_INDEX)

        assert st._get_feature_array('name') is None

    def test__get_feature_array_3(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD = 'temp_c'

        date1 = datetime(2023, 11, 13, 12, 30)

        my_array = st._get_feature_array(FIELD, start_date=date1)

        history = st.get_measurements_by_date_range(start_date=date1)

        assert len(history) == len(my_array) and my_array[0] == history[0][FIELD]

    def test__get_feature_array_4(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD = 'temp_c'

        date2 = datetime(2023, 11, 13, 12, 55)

        my_array = st._get_feature_array(FIELD, end_date=date2)

        history = st.get_measurements_by_date_range(end_date=date2)

        assert len(history) == len(my_array) and my_array[-1] == history[-1][FIELD]

    def test__get_feature_array_5(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD = 'temp_c'

        date1 = datetime(2023, 11, 13, 12, 30)
        date2 = datetime(2023, 11, 13, 12, 55)

        my_array = st._get_feature_array(FIELD, start_date=date1, end_date=date2)

        history = st.get_measurements_by_date_range(start_date=date1, end_date=date2)

        assert len(history) == len(my_array) and my_array[0] == history[0][FIELD] and my_array[-1] == history[-1][FIELD]

    def test__get_feature_array_6(self):
        st = WeatherStation(self.STATION_INDEX)
        FIELD = 'temp_c'

        date1 = datetime(2023, 11, 13, 12, 30)
        date2 = datetime(2023, 11, 13, 12, 55)

        my_array = st._get_feature_array(FIELD, start_date=date1, end_date=date2)

        mean = sum(my_array) / len(my_array)

        assert round(mean, 6) == round(st.mean(FIELD,date1,date2), 6) and max(my_array) == st.max(FIELD,date1,date2) \
               and min(my_array) == st.min(FIELD,date1,date2)

    def test_create_model_0(self):
        st = WeatherStation(self.STATION_INDEX)

        st.create_model()
        st.create_model(input_fields=['temp_c','humidity'])

        l = len(st.models)

        st.delete_model(0)
        st.delete_model(0)  # after the first model gets deleted the index changes

        assert l == 2

    def test_create_model_1(self):
        st = WeatherStation(self.STATION_INDEX)

        st.create_model()

        model = st.models[0]

        assert model.input_fields is None and model.output_fields is None

    def test_create_model_2(self):
        st = WeatherStation(self.STATION_INDEX)

        st.create_model(input_fields=['temp_c','rssi'],
                        output_fields=['mA_battery'])

        model = st.models[0]

        assert model.input_fields == ['temp_c','rssi'] and model.output_fields == ['mA_battery']

    def test_update_model_0(self):
        st = WeatherStation(self.STATION_INDEX)

        st.create_model(input_fields=['temp_c', 'rssi'],
                        output_fields=['mA_battery'])

        st.update_model(0, input_fields=['rssi'],output_fields=['mA_solar'])

        model = st.models[0]

        assert model.input_fields == ['rssi'] and model.output_fields == ["mA_solar"]

    def test_update_model_1(self):
        st = WeatherStation(self.STATION_INDEX)

        st.create_model(input_fields=None,
                        output_fields=['mA_battery'])

        st.update_model(0, input_fields=['rssi'],output_fields=None)

        model = st.models[0]

        assert model.input_fields == ['rssi'] and model.output_fields is None
