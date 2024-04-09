from flask import Blueprint,request, jsonify
from web_service.mongo.connect import stations


station_bp = Blueprint('station', __name__, url_prefix="/stations")


@station_bp.route('/',methods=['GET'])
def get_stations():
    params = request.get_json(silent=True)
    if not params:
        return jsonify(list(stations.find())), 200

    result = stations.find_one({'location' : params['location'].title()})
    if not result:
        return jsonify({'error': 'Station not found'}), 404

    return jsonify(result), 200


@station_bp.route('/<int:station_id>')
def get_station_by_id(station_id: int):
    result = stations.find_one({'_id' : station_id})
    if not result:
        return jsonify({'error': 'Station not found'}),404
    return jsonify(result), 200
