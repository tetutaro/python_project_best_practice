#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import List, Tuple
import os
import re
import subprocess
from subprocess import CompletedProcess
from pathlib import Path
from datetime import datetime
from logging import getLogger, Logger, StreamHandler, Formatter, INFO

PYPROJECT: str = '''[tool.poetry]
name = "{PROJECT}"
version = "0.0.0"  # Automatically updated up poetry-dynamic-versioning
description = ""
authors = ["{NAME}"]
repository = "{REPOSITORY}"
packages = [{{include = "{PACKAGE}"}}]

[tool.poetry.dependencies]
python = "^{PYVERSION}"

[build-system]
requires = ["poetry-core>=1.0.0", "poetry-dynamic-versioning"]
build-backend = "poetry_dynamic_versioning.backend"

[tool.poetry-dynamic-versioning]
enable = true
vcs = "git"
format = "{{base}}"
style = "pep440"

[tool.poetry-dynamic-versioning.substitution]
files = ["{PACKAGE}/__init__.py"]

# [tool.flake8]
# -> .flake8

[tool.black]
line-length = 79
include = "\\.pyi?$"

[tool.mypy]
ignore_missing_imports = true

[tool.pytest.ini_options]
addopts = "-v --cov --flake8 --mypy"
filterwarnings = """
    ignore:SelectableGroups dict interface is deprecated. Use select.
"""

[tool.sphinx-pyproject]
copyright = "{YEAR}, {NAME}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.linkcode", "sphinx.ext.githubpages", "sphinx_rtd_theme"]
templates_path = ["_templates"]
exclude_patterns = []
language = "ja"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
'''

MAKEFILE: str = """.PHONY: clean
clean: clean-python clean-package clean-tests clean-system

.PHONY: clean-python
clean-python:
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*.pyd' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -rf {} +

.PHONY: clean-package
clean-package:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf .eggs/
	@find . -name '*.egg-info' -exec rm -rf {} +
	@find . -name '*.egg' -exec rm -rf {} +

.PHONY: clean-tests
clean-tests:
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .tox/
	@rm -f .coverage
	@rm -rf htmlcov/

.PHONY: clean-system
clean-system:
	@find . -name '*~' -exec rm -f {} +
	@find . -name '.DS_Store' -exec rm -f {} +

.PHONY: requirements
requirements:
	poetry export --without-hashes -f requirements.txt -o requirements.txt

.PHONY: stubs
stubs:
	stubgen -o . -p {PACKAGE}

.PHONY: build-package
build-package:
	$(eval VERSION := $(shell poetry version -s))
	poetry build
	@tar zxf dist/{PACKAGE}-$(VERSION).tar.gz -C ./dist
	@cp dist/{PACKAGE}-$(VERSION)/setup.py setup.py
	@black setup.py
	@rm -rf dist

.PHONY: install
install:
	python setup.py install

.PHONY: uninstall
uninstall:
	pip uninstall -y ${PROJECT}

.PHONY: docs
docs:
	cd docs && make html

.PHONY: tests
tests: tests-python

.PHONY: tests-python
tests-python:
	poetry run pytest

.PHONY: tests-report
tests-report:
	python -u -m pytest -v --cov --cov-report=html

# add new version number.
# do this after committing changes to the local repositry
# and before pushing changes to the remote repository.
.PHONY: version-up
version-up:
ifdef VERSION
	git tag $(VERSION)
	poetry dynamic-versioning
	git add pyproject.toml {PACKAGE}/__init__.py
	git commit -m "$(VERSION)"
	git tag -f $(VERSION)
	git push
	git push --tags
else
	@echo "Usage: make version-up VERSION=vX.X.X"
endif
"""

GITIGNORE: str = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints
.virtual_documents

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# poetry settings
poetry.lock

# OS settings
.DS_Store
"""

FLAKE8: str = """[flake8]
exclude = __pycache__,*.py[cod],build,dist
max-line-length = 79
max-complexity = 15
per-file-ignores =
    *.pyi: E302, E501
extend-ignore = E203
"""

INIT_PY: str = """#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__version__ = "0.0.0"  # Automatically updated by poetry-dynamic-versioning
__all__ = ["__version__"]
"""

DOCS_MAKEFILE: str = """# makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: sphinx-apidoc
sphinx-apidoc:
	sphinx-apidoc --ext-autodoc -f -o source/modules -M "../{PACKAGE}/"
	rm -f source/modules/modules.rst

.PHONY: html
html: sphinx-apidoc
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
"""

DOCS_CONF_PY: str = """#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import Dict, Optional, Any
import os
import sys

from sphinx_pyproject_poetry import SphinxConfig

sys.path.insert(0, os.path.abspath("../../backend"))
config: SphinxConfig = SphinxConfig("../../pyproject.toml", globalns=globals())
project: str = config.name


def linkcode_resolve(
    domain: str,
    info: Dict[str, Any],
) -> Optional[str]:
    if domain != "py":
        return None
    if not info["module"]:
        return None
    filename = info["module"].replace(".", "/")
    if filename == "{PACKAGE}":
        filename += "/__init__.py"
    elif not filename.endswith(".py"):
        filename += ".py"
    return (
        f"{{config.repository}}/{BRANCH}/{{filename}}"
    )
"""


DEV_PACKAGES: List[Dict[str, str]] = [
    {"name": "black"}
    {"name": "flake8", "version": "4.0.1"}
    {"name": "coverage"}
    {"name": "mypy"}
    {"name": "pytest"}
    {"name": "pytest-flake8"}
    {"name": "pytest-cov"}
    {"name": "pytest-mypy"}
    {"name": "sphinx"}
    {"name": "sphinx-rtd-theme", "version": "1.2.0rc2"}
    {"name": "sphinx-pyproject-poetry", "git": "https://github.com/tetutaro/sphinx_pyproject_poetry.git"}
    {"name": "python-lsp-server"}
]


class Project:
    project: str
    package: str
    name: str
    repository: str
    pyversion: str
    logger: Logger

    def __init__(self: Project, logger: Logger) -> None:
        self.logger = logger
        self._get_project_package_from_cwd()
        self._get_name_from_gitconfig()
        self._get_repository_from_config()
        return

    def _get_project_package_from_cwd(self: Project) -> None:
        cwd: Path = Path.cwd()
        project_dir: str = cwd.name
        self.project = project_dir.replace("_", "-")
        self.package = project_dir.replace("-", "_")
        self.logger.info(f"project = {self.project}")
        self.logger.info(f"package = {self.package}")
        return

    def _get_name_from_gitconfig(self: Project) -> None:
        gitconfig: Path = Path.home().joinpath(".gitconfig")
        if not gitconfig.exists():
            self.name = os.environ.get("USER", "name")
        else:
            name: str = ""
            email: str = ""
            with open(gitconfig, "rt") as rf:
                for line in rf.readlines():
                    line = line.strip()
                    if line.startswith("name"):
                        name = line.split("=", 2)[-1].strip()
                    elif line.startswith("email"):
                        email = line.split("=", 2)[-1].strip()
            if name == "":
                self.name = os.environ.get("USER", "name")
            elif email == "":
                self.name = name
            else:
                self.name = f"{name}<{email}>"
        self.logger.info(f"name = {self.name}")
        return

    def _get_repository_from_config(self: Project) -> None:
        config: Path = Path.cwd().joinpath(".git/config")
        if not config.exists():
            self.repository = ""
        else:
            url: str = ""
            with open(config, "rt") as rf:
                for line in rf.readlines():
                    line = line.strip()
                    if line.startswith("url"):
                        url = line.split("=", 2)[-1].strip()
                        break
            if url.endswith(".git"):
                url = url[:-4]
            if url.startswith("git@"):
                self.repository = "https://" + url[4:].replace(":", "/")
            elif url.startswith("http"):
                self.repository = url
            else:
                self.repository = ""
        self.logger.info(f"repository = {self.repository}")
        return

    def _create_pyproject(self: Project) -> None:
        year = datetime.now().strftime("%Y")
        pyproject: Path = Path.cwd().joinpath("pyproject.toml")
        with open(pyproject, "wt") as wf:
            wf.write(
                PYPROJECT.format(
                    PROJECT=self.project,
                    PACKAGE=self.package,
                    REPOSITORY=self.repository,
                    PYVERSION=self.pyversion,
                    YEAR=year,
                )
            )
        return

    def _get_pyenv_versions(self: Project) -> List[str]:
        res: CompletedProcess = subprocess.run(
            ["pyenv", "versions"],
            capture_output=True,
            check=True,
        )
        if res.returncode != 0:
            raise SystemError("pyenv is not installed")
        return [x.strip() for x in res.stdout.decode("utf-8").splitlines()]

    @staticmethod
    def _get_largest_version(versions: List[str]) -> str:
        nvs: List[List[int]] = [
            [int(x, base=10) for x in version.split(".")]
            for version in versions
        ]
        nvs = sorted(nvs, key=lambda x: (x[0], x[1], x[2]), reverse=True)
        return ".".join([str(x) for x in nvs[0]])

    @staticmethod
    def _invoke_cmnd(cmnd: str) -> None:
        cmnds = cmnd.split()
        res: CompletedProcess = subprocess.run(cmnd.split(), check=True)
        if res.returncode != 0:
            raise SystemError(f"command ({cmnd}) failed")
        return

    @staticmethod
    def _invoke_cmnd_ignore_error(cmnd: str) -> None:
        cmnds = cmnd.split()
        try:
            res: CompletedProcess = subprocess.run(cmnd.split(), check=True)
        except Exception:
            pass
        return

    def create_python_environment(self: Project) -> None:
        virtualenvs: List[str] = self._get_pyenv_versions()
        python3_venvs: List[str] = list()
        for venv in virtualenvs:
            if re.match(r"3\.[0-9]+\.[0-9]+$", venv) is not None:
                python3_venvs.append(venv)
        if len(python3_venvs) == 0:
            raise SystemError("python3 virtuanenv is not found")
        latest_venv = self._get_largest_version(python3_venvs)
        self.pyversion = ".".join(x for x in latest_venv.split(".")[:2])
        self._create_pyproject()
        self._invoke_cmnd(cmnd=f"pyenv shell {latest_venv}")
        self._invoke_cmnd(cmnd="poetry shell")
        virtualenvs = self._get_pyenv_versions()
        local_venv: str = ""
        for venv in virtualenvs:
            if venv.startswith(self.project):
                local_venv = venv
                break
        self._invoke_cmnd(cmnd=f"pyenv local {local_venv}")
        self._invoke_cmnd(cmnd="pip install --upgrade pip setuptools wheel")
        return

    def create_basic_files(self: Project) -> None:
        makefile: Path = Path.cwd().joinpath("Makefile")
        with open(makefile, "wt") as wf:
            wf.write(
                MAKEFILE.format(
                    PROJECT=self.project,
                    PACKAGE=self.package,
                )
            )
        gitignore: Path = Path.cwd().joinpath(".gitignore")
        with open(gitignore, "wt") as wf:
            wf.write(GITIGNORE)
        flake8: Path = Path.cwd().joinpath(".flake8")
        with open(flake8, "wt") as wf:
            wf.write(FLAKE8)
        package_dir: Path = Path.cwd().joinpath(self.package)
        package_dir.mkdir(exist_ok=True)
        package_init: Path = package_dir.joinpath("__init__.py")
        with open(package_init, "wt") as wf:
            wf.write(INIT_PY)
        test_dir: Path = Path.cwd().joinpath("tests")
        test_dir.mkdir(exist_ok=True)
        test_init: Path = test_dir.joinpath("__init__.py")
        test_init.touch()
        doc_dir: Path = Path.cwd().joinpath("docs")
        doc_dir.mkdir(exist_ok=True)
        return

    def install_dev_packages(self: Project) -> None:
        packages: List[str] = list()
        for pkg in DEV_PACKAGES:
            git: Opional[str] = pkg.get("git")
            if git is not None:
                packages.append(git)
                continue
            name: Optional[str] = pkg.get("name")
            if name is None:
                continue
            version: Optional[str] = pkg.get("version")
            if version is not None:
                name += f"={version}"
            packages.append(name)
        if len(packages) == 0:
            return
        cmnd = f'poetry add --group dev {" ".join(packages)}'
        self._invoke_cmnd(cmnd=cmnd)
        self._invoke_cmnd_ignore_error(cmnd="rehash")
        return

    def setup_sphinx(self: Project) -> None:
        base: Path = Path.cwd()
        docs: Path = base.joinpath("docs")
        os.chdir(docs)
        cmnd: str = (
            "sphinx-quickstart --quiet --sep --no-batchfile "
            "--ext-autodoc --project {self.project} --author dummy"
        )
        self._invoke_cmnd(cmnd=cmnd)
        os.chdir(base)
        makefile: Path = docs.joinpath("Makefile")
        with open(makefile, "wt") as wf:
            wf.write(DOCS_MAKEFILE.format(
                PACKAGE=self.package
            ))
        branch: str = ""
        if "github" in self.repository:
            branch = "blob/main"
        elif "gitlab" in self.repository:
            branch = "-/tree/main"
        conf_py: Path = docs.joinpath("source/conf.py")
        with open(conf_py, "wt") as wf:
            wf.write(DOCS_CONF_PY.format(
                PACKAGE=self.package,
                BRANCH=branch,
            ))
        return


def main() -> None:
    logger = getLogger(__file__)
    logger.setLevel(INFO)
    formatter = Formatter("%(asctime)s: %(levelname)s: %(message)s")
    handler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    try:
        project = Project(logger=logger)
        project.create_python_environment()
        project.create_basic_files()
        project.install_dev_packages()
        project.setup_sphinx()
    except Exception as e:
        print(f"{e}")
    return


if __name__ == "__main__":
    main()
