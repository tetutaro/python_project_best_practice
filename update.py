#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from __future__ import annotations
from typing import List
import os
import re
import subprocess
from subprocess import CompletedProcess
from logging import getLogger, Logger, StreamHandler, Formatter, INFO
from argparse import ArgumentParser


class Project:
    project: str = ""
    package: str = ""
    repository: str = ""
    logger: Logger

    def __init__(self: Project, logger: Logger) -> None:
        self.logger = logger
        self._get_repository_from_config()
        if self.project == "":
            self._get_project_package_from_cwd()
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
        if self.repository != "":
            project_dir: str = self.repository.split("/")[-1]
            self.project = project_dir.replace("_", "-")
            self.package = project_dir.replace("-", "_")
        self.logger.debug(f"repository = {self.repository}")
        return

    def _get_project_package_from_cwd(self: Project) -> None:
        cwd: Path = Path.cwd()
        project_dir: str = cwd.name
        self.project = project_dir.replace("_", "-")
        self.package = project_dir.replace("-", "_")
        self.logger.debug(f"project = {self.project}")
        self.logger.debug(f"package = {self.package}")
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

    def get_latest_venv(self: Project) -> None:
        virtualenvs: List[str] = self._get_pyenv_versions()
        python3_venvs: List[str] = list()
        for venv in virtualenvs:
            if re.match(r"3\.[0-9]+\.[0-9]+$", venv) is not None:
                python3_venvs.append(venv)
        if len(python3_venvs) == 0:
            raise SystemError("python3 virtuanenv is not found")
        latest_venv = self._get_largest_version(python3_venvs)
        print(latest_venv)
        return

    def get_project_python(self: Project) -> None:
        virtualenvs: List[str] = self._get_pyenv_versions()
        local_venv: str = ""
        for venv in virtualenvs:
            if venv.startswith(self.project):
                local_venv = venv
                break
        if local_venv == "":
            raise SystemError("")
        print(local_venv)
        return


def main() -> None:
    # parser arguments
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "action",
        choices=[
            "latest_venv",
            "project_python",
        ],
    )
    args = parser.parse_args()
    # create logger
    logger: Logger = getLogger(__file__)
    logger.setLevel(INFO)
    formatter: Formatter = Formatter("%(asctime)s: %(levelname)s: %(message)s")
    handler: StreamHandler = StreamHandler()
    handler.setLevel(INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    try:
        project: Project = Project(logger=logger)
        if args.action == "latest_venv":
            project.get_latest_venv()
        elif args.action == "project_python":
            project.get_project_python()
    except Exception as e:
        print(f"{e}")
    return


if __name__ == "__main__":
    main()
