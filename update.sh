#!/usr/bin/env bash

set -eu

setup_py="_setup_project.py"

function download_setup_py () {
    curl -fsSL -o ${setup_py} "https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/setup.py"
}

function delete_setup_py () {
    rm -f ${setup_py}
}

export PATH=${HOME}/.pyenv/bin:${HOME}/.local/bin:${PATH}
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
download_setup_py
shell_version=$(python3 ${setup_py} latest_venv)
pyenv shell ${shell_version}
poetry update
pyenv_version=$(python3 ${setup_py} project_python)
pyenv local ${pyenv_version}
pyenv shell ${pyenv_version}
pip install --upgrade pip setuptools wheel
delete_setup_py

set +eu

source deactivate
cd ~ >/dev/null 2>&1
cd - >/dev/null 2>&1
