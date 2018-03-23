#!/usr/bin/env bash

#make necessary changes in config.py
gunicorn --pythonpath /api_gateway/ -b 0.0.0.0:5000 api_v1:app