from flask import Blueprint, Response, jsonify
from web_service.utils.ws_helper_functions import find_station
from typing import Union
import io
from web_service.classes.graphs.graph_types import GraphType
from web_service.mongo.connect import stations


graph_bp = Blueprint('graphs',__name__, url_prefix='/stations/<station>/graphs')


@graph_bp.route('/<graph_type>/<pin>')
def plot_graph_1var(station : Union[str,int], graph_type : str, pin : str):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404
    s_id = s.id

    try:
        pins = stations.find_one({'_id': s_id}, {'available_data': 1, '_id': 0})['available_data']
    except KeyError:
        return jsonify({'error': 'Data not found. Station might not store data.'}), 404

    graph_type = graph_type.lower()

    if graph_type.upper() not in [el.name for el in list(GraphType) if 'one_var' in el.value]:
        return jsonify({'error': 'Graph type not found'}), 400
    if pin not in pins:
        return jsonify({'error': 'Pin not found'}), 400

    if graph_type == 'boxplot':
        try:
            graph = s.box_plot(pin)
            img = io.BytesIO()
            graph.savefig(img, format='png')
            img.seek(0)
            return Response(img.getvalue(), mimetype='image/png')
        except Exception as e:
            return jsonify({'error': f"Error during graph generation {e}"}), 500

    if graph_type == 'histogram':
        try:
            graph = s.histogram(pin)
            img = io.BytesIO()
            graph.savefig(img, format='png')
            img.seek(0)
            return Response(img.getvalue(), mimetype='image/png')
        except Exception as e:
            return jsonify({'error': f"Error during graph generation {e}"}), 500

    if graph_type == 'lineplot':
        try:
            line_plot = s.line_plot(pin)
            fig = line_plot.plot_graph()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            return Response(img.getvalue(), mimetype='image/png')
        except Exception as e:
            return jsonify({'error': f"Error during graph generation {e}"}), 500

    return jsonify({'error': 'Graph type not supported'}), 400


@graph_bp.route('/<graph_type>/<pin1>/<pin2>')
def plot_graph_2var(station : Union[str,int], graph_type : str, pin1 : str, pin2 : str):
    s = find_station(station)
    if not s:
        return jsonify({'error' : f'Station not found'}), 404
    s_id = s.id

    try:
        pins = stations.find_one({'_id': s_id}, {'available_data': 1, '_id': 0})['available_data']
    except KeyError:
        return jsonify({'error': 'Data not found. Station might not store data.'}), 404

    graph_type = graph_type.lower()

    if graph_type.upper() not in [el.name for el in list(GraphType) if 'two_var' in el.value]:
        return jsonify({'error': 'Graph type not found'}), 400
    if pin1 not in pins or pin2 not in pins:
        return jsonify({'error': 'Pin not found'}), 400

    if graph_type == 'scatterplot':
        try:
            graph = s.scatter_plot(pin1, pin2)
            img = io.BytesIO()
            graph.savefig(img, format='png')
            img.seek(0)
            return Response(img.getvalue(), mimetype='image/png')
        except Exception as e:
            return jsonify({'error': f"Error during graph generation {e}"}), 500

    if graph_type == 'lineplot':
        try:
            line_plot = s.line_plot(pin1, pin2)
            fig = line_plot.plot_graph()
            img = io.BytesIO()
            fig.savefig(img, format='png')
            img.seek(0)
            return Response(img.getvalue(), mimetype='image/png')
        except Exception as e:
            return jsonify({'error': f"Error during graph generation {e}"}), 500
