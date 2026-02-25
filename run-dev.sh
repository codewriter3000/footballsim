#!/bin/bash

source ./venv/bin/activate
uvicorn src.integrations.api:app --reload --port 8000
