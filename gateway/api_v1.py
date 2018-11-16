"""Api gateway for fabric8-analytics services."""

import os
import logging
import requests
from flask import Flask, request, current_app, Response
from flask.json import jsonify
from urllib.parse import urljoin

from gateway.auth import login_required
from gateway.defaults import configuration
from gateway.errors import HTTPError


def configure_logging(flask_app):
    """Configure logging for this application."""
    # Do not interfere if running in debug mode
    if not flask_app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
        log_level = os.environ.get('FLASK_LOGGING_LEVEL', logging.getLevelName(logging.WARNING))
        handler.setLevel(log_level)

        flask_app.logger.addHandler(handler)
        flask_app.config['LOGGER_HANDLER_POLICY'] = 'never'
        flask_app.logger.setLevel(logging.DEBUG)


# initialize the Flask application
app = Flask(__name__)

# configure logging for the Flask application
configure_logging(app)


@app.route('/')
def index():
    """List all known services."""
    response = {
        'services': sorted(list(configuration.bayesian_services.keys()))
    }

    return jsonify(response), 200


@app.route(
    '/<service>/<path:varargs>',
    methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
)
@app.route(
    '/<service>/',
    methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'],
    defaults={'varargs': None}
)
@login_required
def api_gateway(service, varargs):
    """Forward requests to the `service`."""
    if service not in configuration.bayesian_services:
        return jsonify({'error': 'unknown service'}), 400

    url = urljoin(configuration.bayesian_services[service], varargs or '/')
    current_app.logger.debug('Forwarding request to {url}'.format(url=url))

    response = requests.request(
        method=request.method,
        params=request.args.items(),
        url=url,
        headers={
            key: value for (key, value) in request.headers
            if key != 'Host'
        },
        data=request.get_data(),
        cookies=request.cookies
    )

    response = Response(response.content, response.status_code, response.headers.items())
    return response


@app.errorhandler(404)
def api_404_handler(*args, **_kwargs):
    """Handle all other routes not defined above."""
    return jsonify(error='no such endpoint'), 404


@app.errorhandler(HTTPError)
def error_handler(error):
    """Handle errors which occurred while processing requests."""
    return jsonify(error=error.error), error.status_code


if __name__ == '__main__':
    app.run()
