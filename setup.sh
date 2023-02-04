#!/usr/bin/env bash

set -eu

function download_setup_py () {
    return 0
}

function delete_setup_py () {
    return 0
}

download_setup_py
shell_version=$(python3 setup.py create_pyproject)
pyenv shell ${shell_version}
poetry shell
pvenv_version=$(python3 setup.py project_python)
pyenv local ${pyenv_version}
pip install --upgrade pip setuptools wheel
python3 setup.py create_basic_files
dev_packages=$(python3 setup.py get_dev_packages)
poetry add --group dev ${dev_packages}
quick_cmnd=$(python3 setup.py get_sphinx_command)
cd docs && ${quick_cmnd}
python3 setup.py setup_sphinx
delete_setup_py
