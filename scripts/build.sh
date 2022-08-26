#!/usr/bin/bash

set -e


export FASTIDIUS_VERSION=0.0.14

scripts/compile.sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

rm -rf build/ dist/ fastidius.egg-info/
python setup.py sdist bdist_wheel

echo "__version__ = '$FASTIDIUS_VERSION'" > fastidius/__init__.py

echo
read -p "Upload to pypi? "
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    twine upload -u __token__ -p $PYPI_TOKEN --skip-existing dist/*
fi
