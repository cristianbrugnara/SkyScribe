from web_service.utils.ws_helper_functions import MongoFilterer


class TestMongoFilterer:

    def test_init_and_str_0(self):
        my_dict = {}
        operators = {">" : "$gt",
                            "<" : "$lt",
                            ">=" : "$gte",
                            "<=" : "$lte",
                            "=" : "$eq"}
        flt = MongoFilterer(my_dict)
        assert str(flt) == f"Now working on the following dictionary (obtained from a query string): {my_dict}. " \
                           f"Reminder on the available operators: {operators}"

    def test_filter_by_key_0(self):
        KEY = 'temperature'
        my_dict = {KEY : [">5", "<6"]}
        flt = MongoFilterer(my_dict)

        assert flt.filter_by_key(KEY) == {"$gt" : 5, "$lt" : 6}

    def test_filter_by_key_1(self):
        KEY = 'temperature'
        my_dict = {KEY : ["<=6", ">=5"]}
        flt = MongoFilterer(my_dict)

        assert flt.filter_by_key(KEY) == {"$lte" : 6,"$gte" : 5, }

    def test_filter_by_key_2(self):
        KEY = 'temperature'
        my_dict = {KEY : ["=1"]}
        flt = MongoFilterer(my_dict)

        assert flt.filter_by_key(KEY) == {"$eq" : 1}

    def test_filter_by_key_3(self):
        KEY = 'temperature'
        my_dict = {KEY : ["=1","<=6", ">=5",">5", "<6"]}  # even if it won't make sense
        flt = MongoFilterer(my_dict)

        assert flt.filter_by_key(KEY) == {"$eq" : 1, "$lte" : 6, "$gte" : 5, "$gt" : 5, "$lt" : 6}
