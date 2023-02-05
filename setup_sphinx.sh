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
quick_cmnd=$(python3 ${setup_py} get_sphinx_command)
cd docs >/dev/null 2>&1
${quick_cmnd}
cd - >/dev/null 2>&1
python3 ${setup_py} setup_sphinx
delete_setup_py
