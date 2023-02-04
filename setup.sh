#!/usr/bin/env bash

set -eu

function download_setup_py () {
    return 0
}

function delete_setup_py () {
    return 0
}

export PATH=${HOME}/.pyenv/bin:${HOME}/.local/bin:${PATH}
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
download_setup_py
shell_version=$(python3 setup.py create_pyproject)
pyenv shell ${shell_version}
poetry update
pyenv_version=$(python3 setup.py project_python)
pyenv local ${pyenv_version}
pyenv shell ${pyenv_version}
pip install --upgrade pip setuptools wheel
python3 setup.py create_basic_files
dev_packages=$(python3 setup.py get_dev_packages)
echo ${dev_packages}
poetry add --group dev ${dev_packages}
quick_cmnd=$(python3 setup.py get_sphinx_command)
cd docs >/dev/null 2>&1
${quick_cmnd}
cd - >/dev/null 2>&1
python3 setup.py setup_sphinx
delete_setup_py
source deactivate
cd ~ >/dev/null 2>&1
cd - >/dev/null 2>&1
