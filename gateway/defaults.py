"""Module that contains global variables with the project runtime configuration."""
import os


class F8AConfiguration:
    """Configuration class."""

    DISABLE_AUTHENTICATION = os.getenv('DISABLE_AUTHENTICATION', 'false') in ('1', 'True', 'true')

    BAYESIAN_DATA_IMPORTER_SERVICE_PORT = os.getenv("BAYESIAN_DATA_IMPORTER_SERVICE_PORT", 9192)

    BAYESIAN_DATA_IMPORTER_SERVICE_HOST = os.getenv("BAYESIAN_DATA_IMPORTER_SERVICE_HOST",
                                                    "data-model-importer")

    DATA_IMPORTER_ENDPOINT = "http://%s:%s" % (BAYESIAN_DATA_IMPORTER_SERVICE_HOST,
                                               BAYESIAN_DATA_IMPORTER_SERVICE_PORT)

    BAYESIAN_JWT_AUDIENCE = os.getenv("BAYESIAN_JWT_AUDIENCE", "fabric8-online-platform")

    BAYESIAN_FETCH_PUBLIC_KEY = os.getenv("BAYESIAN_FETCH_PUBLIC_KEY", "keycloak-url")

    BAYESIAN_JOBS_SERVICE_PORT = os.getenv("BAYESIAN_JOBS_SERVICE_PORT", 34000)

    BAYESIAN_JOBS_SERVICE_HOST = os.getenv("BAYESIAN_JOBS_SERVICE_HOST", "jobs-service")

    JOBS_ENDPOINT = "http://%s:%s" % (BAYESIAN_JOBS_SERVICE_HOST, BAYESIAN_JOBS_SERVICE_PORT)

    BAYESIAN_GREMLIN_HTTP_SERVICE_HOST = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_HOST",
                                                   "gremlin-service")

    BAYESIAN_GREMLIN_HTTP_SERVICE_PORT = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_PORT",
                                                   8182)

    GREMLIN_ENDPOINT = "http://%s:%s" % (BAYESIAN_GREMLIN_HTTP_SERVICE_HOST,
                                         BAYESIAN_GREMLIN_HTTP_SERVICE_PORT)

    BAYESIAN_GREMLIN_HTTPINGESTION_SERVICE_HOST = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_HOST",
                                                            "gremlin-service")

    BAYESIAN_GREMLIN_HTTPINGESTION_SERVICE_PORT = os.getenv("BAYESIAN_GREMLIN_HTTP_SERVICE_PORT",
                                                            8182)

    GREMLIN_INGESTION_ENDPOINT = "http://%s:%s" % (BAYESIAN_GREMLIN_HTTPINGESTION_SERVICE_HOST,
                                                   BAYESIAN_GREMLIN_HTTPINGESTION_SERVICE_PORT)

    bayesian_services = {'data_importer': DATA_IMPORTER_ENDPOINT,
                         'jobs': JOBS_ENDPOINT,
                         'gremlin': GREMLIN_ENDPOINT,
                         'gremlin_ingestion': GREMLIN_INGESTION_ENDPOINT}


configuration = F8AConfiguration()
