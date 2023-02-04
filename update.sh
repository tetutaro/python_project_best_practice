#!/usr/bin/env bash

set -eu

update_py="_update_project.py"

function download_update_py () {
    curl -fsSL -o ${update_py} "https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/update.py"
}

function delete_update_py () {
    rm -f ${update_py}
}

export PATH=${HOME}/.pyenv/bin:${HOME}/.local/bin:${PATH}
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
download_update_py
shell_version=$(python3 ${update_py} latest_venv)
pyenv shell ${shell_version}
poetry update
pyenv_version=$(python3 ${update_py} project_python)
pyenv local ${pyenv_version}
pyenv shell ${pyenv_version}
pip install --upgrade pip setuptools wheel
poetry install
delete_update_py

set +eu

source deactivate
cd ~ >/dev/null 2>&1
cd - >/dev/null 2>&1
