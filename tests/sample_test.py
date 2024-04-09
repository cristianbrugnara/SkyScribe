from client_library.sky_scribe.sample import Sample
from datetime import datetime


class TestSample:

    date = datetime(2023,12,3,13,34)

    def test_init_and_available_fields_0(self):
        sm = Sample(self.date)
        assert sm.available_fields == ['ts']

    def test_init_and_available_fields_1(self):
        sm = Sample(self.date, humidity=0.6, rssi=1)
        assert sorted(sm.available_fields) == sorted(['ts','humidity', 'rssi'])

    def test_init_0(self):
        sm = Sample(self.date, humidity = 0.6, rssi = 1)
        assert (sm.humidity == 0.6) and (sm.rssi == 1)

    def test_init_1(self):
        sm = Sample(self.date)
        assert sm._modifiable == False

    def test_getattr_0(self):
        sm = Sample(self.date)
        error = False
        try:
            print(sm.rssi)
        except AttributeError as e:
            error=True

        assert error == True

    def test_getattr_1(self):
        sm = Sample(self.date)
        try:
            print(sm.rssi)
        except AttributeError as e:
            msg = str(e)

        assert msg == "Attribute rssi not present in the sample."

    def test_getattr_2(self):
        sm = Sample(self.date, rssi=1)
        assert sm.rssi == 1

    def test_setattr_0(self):
        sm = Sample(self.date, rssi=1)
        try:
            sm.rssi = 2
        except AttributeError as e:
            msg = str(e)

        assert msg == "Sample object cannot be modified manually."

    def test_setattr_1(self):
        sm = Sample(self.date)
        try:
            sm.not_present = 2
        except AttributeError as e:
            msg = str(e)

        assert msg == "Sample object cannot be modified manually."

    def test_str_0(self):
        sm = Sample(self.date)
        assert str(sm) == f'Measurement of {self.date} no measurement'

    def test_str_1(self):
        sm = Sample(self.date, rssi=1)
        assert str(sm) == f'Measurement of {self.date} | rssi : 1'

    def test_str_2(self):
        sm = Sample(self.date, temp_c=6.67 ,rssi=1)
        assert str(sm) == f'Measurement of {self.date} | temp_c : 6.67 | rssi : 1'



