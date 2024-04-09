from flask import Blueprint, request, jsonify
from web_service.utils.ws_helper_functions import find_station
from typing import Union


forecast_bp = Blueprint('forecast', __name__, url_prefix="/stations/<station>/forecast")


@forecast_bp.route('/models', methods = ['POST', 'GET'])
def models(station: Union[int,str]):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    if request.method == 'GET':
        return [i for i in range(len(s.models))]

    params = request.get_json(silent=True)
    if not params:
        params = {}

    idx = s.create_model(**params)

    return jsonify({'idx' : idx}), 201


@forecast_bp.route('/models/<idx>', methods = ['GET','DELETE','PATCH'])
def one_model(station: Union[int,str], idx : int):
    idx = int(idx)
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    if idx < 0 or idx >= len(s.models):
        return jsonify({'error' : 'model not found'}), 404

    if request.method == "DELETE":
        s.delete_model(idx)
        return jsonify({"result": f"model {idx} deleted"}), 200

    elif request.method == 'PATCH':
        params = request.get_json(silent=True)
        if not params:
            params = {}

        s.update_model(idx, **params)
        return jsonify({"result": f"model {idx} updated"}), 200

    model = s.models[idx]

    res = f'Model {idx}:\n'
    for i,layer in enumerate(model.model.layers):
        res+=f'Layer {i+1}: {layer.name.title()}, output shape: {layer.output_shape}\n'

    inputs = model.input_fields
    outputs = model.output_fields

    res+=f"Receives as input: {inputs if inputs else 'All fields'}\n"
    res+=f"Outputs: {outputs if outputs else 'All fields'}"
    return res, 200


@forecast_bp.route('/models/<idx>/train', methods = ['POST'])
def train_model(station: Union[int,str], idx : int):
    idx = int(idx)
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    if idx < 0 or idx >= len(s.models):
        return jsonify({'error' : 'model not found'}), 404

    params = request.get_json(silent=True)
    if not params:
        params = {}

    return s.train_model(idx = idx, **params)


@forecast_bp.route('/models/<idx>/predict')
def forecast(station: Union[int,str], idx :  int):
    idx = int(idx)
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404

    if idx < 0 or idx >= len(s.models):
        return jsonify({'error' : 'model not found'}), 404

    result = s.predict(idx)

    return jsonify(result), 200
