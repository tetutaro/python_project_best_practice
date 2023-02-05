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
poetry shell
pyenv_version=$(python3 ${setup_py} project_python)
pyenv local ${pyenv_version}
pyenv shell ${pyenv_version}
pip install --upgrade pip setuptools wheel
poetry install
python3 ${setup_py} create_basic_files
quick_cmnd=$(python3 ${setup_py} get_sphinx_command)
cd docs >/dev/null 2>&1
${quick_cmnd}
cd - >/dev/null 2>&1
python3 ${setup_py} setup_sphinx
update_files=$(python3 ${setup_py} get_update_files)
if [[ "${update_files}" != "" ]]; then
    git add ${update_files}
    git commit -m "project start"
    git push
fi
delete_setup_py

set +eu

source deactivate
cd ~ >/dev/null 2>&1
cd - >/dev/null 2>&1
