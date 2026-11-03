#!/bin/sh
# Run from repository root. Only mocks and disposable test databases.
set -eu
backend/.venv/bin/python -m unittest discover -s backend/tests -v > docs/evidence/part3/backend-output.txt 2>&1
npm --prefix frontend test > docs/evidence/part3/frontend-output.txt 2>&1
npm --prefix frontend run build > docs/evidence/part3/build-output.txt 2>&1
git diff --check
