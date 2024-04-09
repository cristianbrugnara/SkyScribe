from flask import Flask
from blueprints.samples_bp import samples_bp
from blueprints.graphs_bp import graph_bp
from blueprints.stats_bp import stats_bp
from blueprints.stations_bp import station_bp
from blueprints.forecast_bp import forecast_bp


if __name__ == '__main__':
    app = Flask(__name__)

    app.register_blueprint(samples_bp)
    app.register_blueprint(graph_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(station_bp)
    app.register_blueprint(forecast_bp)

    app.run(debug=True)
