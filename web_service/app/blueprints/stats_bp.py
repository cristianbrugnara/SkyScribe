from flask import Blueprint, jsonify, request
from web_service.utils.ws_helper_functions import find_station
from typing import Union
from web_service.mongo.connect import stations
from web_service.utils.ws_helper_functions import handle_date
from web_service.classes.statistics.statistics_type import StatType


stats_bp = Blueprint('statistics', __name__, url_prefix="/stations/<station>/statistics")


@stats_bp.route('/')
def get_statistics(station: Union[int,str]):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404
    s_id = s.id

    try:
        pins = stations.find_one({'_id': s_id}, {'available_data': 1, '_id': 0})['available_data']
    except KeyError:
        return jsonify({'error': 'Data not found. Station might not store data.'}), 404

    query_dict = request.args.to_dict(flat=False)

    if len(query_dict) == 0:
        return jsonify({f'{pin}' :
                    {'mean': s.mean(pin),
                     'max': s.max(pin),
                     'min': s.min(pin),
                     'stdev': s.std(pin)}
                for pin in pins}), 200


    stat_type = query_dict['stat-type'][0].lower()
    pin = query_dict['pin'][0]

    if stat_type.upper() not in [el.name for el in list(StatType)]:
        return jsonify({'error': 'Statistic type not found'}), 400
    if pin not in pins:
        return jsonify({'error': 'Pin not found'}), 400

    result = None

    if stat_type == 'mean':
        result = s.mean(pin)

    if stat_type == 'max':
        result = s.max(pin)

    if stat_type == 'min':
        result = s.min(pin)
    if stat_type == 'std':
        result = s.std(pin)

    if result is None:
        return jsonify({'error': 'Data not found'}), 404
    return jsonify({'result': result}), 200


@stats_bp.route('/<start_date>/<end_date>')
def get_statistic_of_pin_filtered(station: Union[int, str],start_date : str, end_date : str):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404
    s_id = s.id

    try:
        pins = stations.find_one({'_id': s_id}, {'available_data': 1, '_id': 0})['available_data']
    except KeyError:
        return jsonify({'error': 'Data not found. Station might not store data.'}), 404

    query_dict = request.args.to_dict(flat=False)
    start_date = handle_date(start_date)
    end_date = handle_date(end_date)

    if len(query_dict) == 0:
        return {f'{pin}' :
                    {'mean': s.mean(pin, start_date, end_date),
                     'max': s.max(pin, start_date, end_date),
                     'min': s.min(pin, start_date, end_date),
                     'stdev': s.std(pin, start_date, end_date)}
                for pin in pins}, 200

    stat_type = query_dict['stat-type'][0].lower()
    pin = query_dict['pin'][0]

    if stat_type.upper() not in [el.name for el in list(StatType)]:
        return jsonify({'error' : 'Statistic type not found'}), 400

    if pin not in pins:
        return jsonify({'error': 'Pin not found'}), 400

    result = None

    if stat_type == 'mean':
        result = s.mean(pin,start_date, end_date)

    if stat_type == 'max':
        result = s.max(pin, start_date, end_date)

    if stat_type == 'min':
        result = s.min(pin,start_date, end_date)

    if stat_type == 'std':
        result = s.std(pin, start_date, end_date)

    if result is None:
        return jsonify({'error': 'Data not found'}), 404
    return jsonify({'result': result}), 200

