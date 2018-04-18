"""Api gateway for fabr8-analytics services."""

import json
import logging
import os

import requests
from flask import Flask, request, session, current_app
from flask.json import jsonify
from urllib.parse import urljoin

from gateway.auth import login_required
from gateway.defaults import configuration
from gateway.errors import HTTPError

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def logout():
    """Logout."""
    if 'auth_token' not in session:
        return {}, 401

    session.pop('auth_token')
    return {}, 201


@app.route('/')
def index():
    """List all known services."""
    response = {
        'services': sorted(list(configuration.bayesian_services.keys()))
    }

    return jsonify(response), 200


@app.route('/<service>/<path:varargs>', methods=['POST', 'GET'])
@login_required
def api_gateway(service, varargs=None):
    """Call f8a service based on request parameters.

    Parameters are separated by / where the firs is servicename
    second is the service endpoint name following by
    data that service ingest separated by /
    """
    if service not in configuration.bayesian_services:
        return jsonify({'error': 'unknown service'}), 400

    uri = urljoin(configuration.bayesian_services[service], varargs)
    headers = {'Content-Type': 'application/json'}

    if request.method == 'POST':
        try:
            result = requests.post(uri, json=json.dumps(request.values), headers=headers)
            status_code = result.status_code
            current_app.logger.info('Request has reported following body: {r}'.format(r=result))
        except requests.exceptions.ConnectionError:
            error = {"Error": "Error occurred during the request adress"
                              " {u} is not available".format(u=uri)}
            status_code = 500
            current_app.logger.error(error)

    elif request.method == 'GET':
        try:
            result = requests.get(uri, headers=headers)
            status_code = result.status_code
            current_app.logger.info('Request has reported following body: {r}'.format(r=result))
        except requests.exceptions.ConnectionError:
            error = {"Error": "Error occurred during the request adress"
                              " {u} is not available".format(u=uri)}
            status_code = 500
            current_app.logger.error(error)

    response = app.response_class(
        response=json.dumps(error or result.text),
        status=status_code,
        mimetype='application/json'
    )

    return response


@app.route('/readiness')
def readiness():
    """Handle the /readiness REST API call."""
    current_app.logger.debug("Readiness probe - connect")
    return jsonify({}), 200


@app.route('/liveness')
def liveness():
    """Handle the /liveness REST API call."""
    current_app.logger.debug("Liveness probe - connect")
    return jsonify({}), 200


@app.route('/<path:invalid_path>')
def api_404_handler(*args, **kwargs):
    """Handle all other routes not defined above."""
    return jsonify(error='Cannot match given query to any API v1 endpoint'), 404


if __name__ == '__main__':
    app.run()
