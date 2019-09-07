#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/public/source-code"

cd ${CODE_DIR}

pwd | xargs python3 /analyzer/find_depth.py
