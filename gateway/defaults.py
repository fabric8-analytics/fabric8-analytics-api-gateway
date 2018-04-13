#!/usr/bin/env python3

"""Module that contains global variables with the project runtime configuration."""
import datetime
import os
from flask.json import JSONEncoder


def json_serial(obj):
    """Sanitize datetime serialization."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError('Type {t} not serializable'.format(t=type(obj)))


class JSONEncoderWithExtraTypes(JSONEncoder):
    """Implementation of JSON Encoder.

    It supports additional types:

        - date/time objects
        - arbitrary non-mapping iterables
    """

    def default(self, obj):
        """Encode method."""
        try:
            if isinstance(obj, datetime.datetime):
                return json_serial(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class F8AConfiguration:
    """Configuration class."""

    # keep disabled authentication by default
    DISABLE_AUTHENTICATION = os.getenv('DISABLE_AUTHENTICATION', '1') in ('1', 'True', 'true')

    BAYESIAN_DATA_IMPORTER_SERVICE_PORT = os.getenv("BAYESIAN_DATA_IMPORTER_SERVICE_PORT", 9192)

    BAYESIAN_DATA_IMPORTER_SERVICE_HOST = os.getenv("BAYESIAN_DATA_IMPORTER_SERVICE_HOST",
                                                    "data-model-importer")

    DATA_IMPORTER_ENDPOINT = "http://%s:%s" % (BAYESIAN_DATA_IMPORTER_SERVICE_HOST,
                                               BAYESIAN_DATA_IMPORTER_SERVICE_PORT)

    BAYESIAN_JWT_AUDIENCE = os.getenv("BAYESIAN_JWT_AUDIENCE", "fabric8-online-platform")

    BAYESIAN_FETCH_PUBLIC_KEY = os.getenv("BAYESIAN_FETCH_PUBLIC_KEY", "keycloak-url")

    BAYESIAN_JOBS_SERVICE_PORT = os.getenv("BAYESIAN_JOBS_SERVICE_PORT", "data-model-importer")

    BAYESIAN_JOBS_SERVICE_HOST = os.getenv("BAYESIAN_JOBS_SERVICE_HOST", "data-model-importer")

    JOBS_ENDPOINT = "http://%s:%s" % (BAYESIAN_JOBS_SERVICE_HOST, BAYESIAN_JOBS_SERVICE_PORT)

    BAYESIAN_GREMLIN_HTTP_SERVICE_HOST = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_HOST",
                                                   "data-model-importer")

    BAYESIAN_GREMLIN_HTTP_SERVICE_PORT = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_PORT",
                                                   "data-model-importer")

    GREMLIN_ENDPOINT = "http://%s:%s" % (BAYESIAN_GREMLIN_HTTP_SERVICE_HOST,
                                         BAYESIAN_GREMLIN_HTTP_SERVICE_PORT)

    bayesian_services = {'data_importer': DATA_IMPORTER_ENDPOINT,
                         'jobs': JOBS_ENDPOINT,
                         'gremlin': GREMLIN_ENDPOINT}


configuration = F8AConfiguration()
