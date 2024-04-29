import pytest
import logging
from pathlib import Path
from git import Repo

from package_tool import (
    GitManager,
    ConfigParser,
)

from package_setup import package_setup

logger = logging.getLogger()

BASE_VERSION = ["9", "0"]

def test_setup(package_setup_git):
    working_path = package_setup_git[0]
    repo = Repo(working_path)
    branch_name = "dev_BZC-234"

    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(15):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")

    package_setup(branch_name, package_setup_git[1], working_path)

    with open(working_path / "version.txt", "r") as f:
        version = f.readline()
        assert "0.0.16-g" in version

def test_setup_master(package_setup_git):
    working_path = package_setup_git[0]
    repo = Repo(working_path)

    for n in range(15):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")

    package_setup("master", package_setup_git[1], working_path)
    
    with open(working_path / "version.txt", "r") as f:
        version = f.readline()
        assert version == "9.0.0"

