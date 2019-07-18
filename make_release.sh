#!/usr/bin/env bash
rm -rf dist/* build/* && python setup.py bdist_wheel --universal && twine upload dist/*