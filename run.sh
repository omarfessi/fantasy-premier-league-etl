#!/bin/bash
set -e
function format-lint {
    echo "Running ruff linters and formatting"
    ruff check --fix .
    ruff format .
    
}
function run-pipeline {
    echo "Running fpl pipeline"
    python3 -i ingestion/pipeline.py
}

run-pipeline