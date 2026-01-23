#!/bin/bash

source ./venv/bin/activate
uvicorn api:app --reload --port 8000
