[![Build Status](https://ci.centos.org/view/Devtools/job/devtools-fabric8-analytics-api-gateway-f8a-build-master/badge/icon)](https://ci.centos.org/view/Devtools/job/devtools-fabric8-analytics-api-gateway-f8a-build-master/)

# fabric8-analytics-api-gateway

is proxy service that forwards requests to fabric8-analytics services.

List of supported [services](https://github.com/fabric8-analytics/fabric8-analytics-api-gateway/blob/8ddf91dddc7641667b40776439149c4c8019515a/gateway/defaults.py#L71)

Whitelisted users that can access these services are [here](https://github.com/fabric8-analytics/fabric8-analytics-api-gateway/blob/master/gateway/users_whitelist)

## Usage

export your Openshiftio token to env variable OSIO_TOKEN.

The only difference between call to actual service and the proxy call,

is that we append service_name before the request path.

In this example its the data_importer.

```
curl -i -H "Authorization: Bearer $OSIO_TOKEN" -H "Accept: application/json" "http://localhost:5000/data_importer/api/v1/pending"
```

### Footnotes

## Coding standards


- You can use scripts `run-linter.sh` and `check-docstyle.sh` to check if the code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) coding standards. These scripts can be run w/o any arguments:

```
./run-linter.sh
./check-docstyle.sh
```

The first script checks the indentation, line lengths, variable names, white space around operators etc. The second
script checks all documentation strings - its presence and format. Please fix any warnings and errors reported by these
scripts.

