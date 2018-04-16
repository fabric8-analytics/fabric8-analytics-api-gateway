"""Api gateway for fabr8-analytics services."""

import json
import logging

import requests
from flask import Flask, request, session
from flask.json import jsonify
from urllib.parse import urljoin

from gateway.auth import login_required
from gateway.defaults import configuration
from gateway.errors import HTTPError

logger = logging.getLogger(__name__)

app = Flask(__name__)


def logout():
    """Logout from the Job service (if the user is already loged in)."""
    if 'auth_token' not in session:
        return {}, 401

    session.pop('auth_token')
    return {}, 201


@app.route('/_error')
def error():
    """Implement the endpoint used by httpd, which redirects its errors to it."""
    try:
        status = int(request.environ['REDIRECT_STATUS'])
    except Exception:
        # if there's an exception, it means that a client accessed this directly;
        # in this case, we want to make it look like the endpoint is not here
        return api_404_handler()
    msg = 'Unknown error'
    # for now, we just provide specific error for stuff that already happened;
    #  before adding more, I'd like to see them actually happening with reproducers
    if status == 401:
        msg = 'Authentication failed'
    elif status == 405:
        msg = 'Method not allowed for this endpoint'
    raise HTTPError(status, msg)


@app.route('/<path:varargs>', methods=['POST', 'GET'])
@login_required
def api_gateway(varargs=None):
    """Call f8a service based on request parameters.

    Parameters are separated by / where the firs is servicename
    second is the service endpoint name following by
    data that service ingest separated by /
    """
    vargs_array = varargs.split("/")
    # get service name
    service_name = vargs_array[0] or 'data_importer'
    # remove service name from the url
    payload = "/".join(vargs_array[1:])

    uri = urljoin(configuration.bayesian_services[service_name], payload)
    headers = {'Content-Type': 'application/json'}

    if request.method == 'POST':
        try:
            result = requests.post(uri, json=json.dumps(payload), headers=headers)
            status_code = result.status_code
            logger.info(logger, 'Request has reported following body: {r}'.format(r=result))
        except requests.exceptions.ConnectionError:
            result = {'Error': 'Error occurred during the request'}
            status_code = 500

    elif request.method == 'GET':
        try:
            result = requests.get(uri, headers=headers)
            status_code = result.status_code
            logger.info(logger, 'Request has reported following body: {r}'.format(r=result))
        except requests.exceptions.ConnectionError:
            result = {'Error': 'Error occurred during the request'}
            status_code = 500

    return jsonify(result.text), status_code


@app.route('/readiness')
def readiness():
    """Handle the /readiness REST API call."""
    return jsonify({}), 200


@app.route('/liveness')
def liveness():
    """Handle the /liveness REST API call."""
    return jsonify({}), 200


@app.route('/<path:invalid_path>')
def api_404_handler(*args, **kwargs):
    """Handle all other routes not defined above."""
    return jsonify(error='Cannot match given query to any API v1 endpoint'), 404


if __name__ == '__main__':
    app.run()
