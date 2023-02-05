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
shell_version=$(python3 ${setup_py} create_pyproject)
pyenv shell ${shell_version}
python3 ${setup_py} create_basic_files
delete_setup_py
