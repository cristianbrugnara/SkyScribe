from flask import Blueprint, request, jsonify
from typing import Union
from web_service.utils.ws_helper_functions import find_station, handle_date, MongoFilterer

# un sample è una misurazione associata a una data
samples_bp = Blueprint('sample', __name__, url_prefix="/stations/<station>/samples")


@samples_bp.route('/')
def get_all_samples(station: Union[int,str]):
    query_dict = request.args.to_dict(flat = False)
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    if len(query_dict) == 0:
        return jsonify(s.get_measurements_by_date_range()), 200

    filterer = MongoFilterer(query_dict)
    filters = {}

    for key in query_dict.keys():
        filters[key] = filterer.filter_by_key(key)

    result = s.get_measurement_mongo_filtered(filters)
    if result:
        return jsonify(result), 200
    return jsonify({'error' : f'Station not found'}), 404


@samples_bp.route('/<date>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def sample_by_date(station: Union[int,str], date : str):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    date = handle_date(date)
    result = None
    code = 200

    if request.method=='GET':
        result = s.get_measurement_by_date(date)
        if result:
            return jsonify(result), 200

    elif request.method == 'DELETE':
        result = s.delete_sample_by_date(date)

    params = request.get_json(silent=True)
    if not params:
        params = {}

    if request.method == 'POST':
        result = s.add_measurement(date, **params)
        if result == 400:
            return jsonify({'error' : f'Sample associated to datetime {date} already present.'}), 400
        return jsonify({}), 201

    elif request.method == 'PUT':
        result = s.update_measurement_by_date(date,**params)
        code = 201

    elif request.method == 'PATCH':
        result = s.update_measurement_field_by_date(date, **params)

    if not result:
        return jsonify({'error' : f'Sample associated to {date} not found'}), 404

    return jsonify({}), code


@samples_bp.route('/<start_date>/<end_date>')
def samples_by_date_range(station: Union[int,str], start_date : str, end_date : str):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    start_date = handle_date(start_date)
    end_date = handle_date(end_date)

    result = s.get_measurements_by_date_range(start_date,end_date)
    if result:
        return jsonify(result), 200

    return jsonify({'error' : f'Samples not found'}), 404


# used to provide the client library with the first and last sample to be used in range-functions
@samples_bp.route('/<int:first_or_last>')   # first or last as 0 or 1.
def get_first_or_last_sample(station: Union[int,str], first_or_last: int):
    s = find_station(station)
    if not s:
        return jsonify({'error': f'Station not found'}), 404

    if first_or_last == 0:
        result = s.start.strftime('%Y-%m-%d %H:%M:%S')
    else:
        result = s.end.strftime('%Y-%m-%d %H:%M:%S')
    return result, 200
