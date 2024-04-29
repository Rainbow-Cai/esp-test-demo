import pytest
import logging
import json
from git import Repo

from package_tool import (
    GitManager,
    ConfigParser
)

from package_final import package_final

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
    
    git_manager = GitManager(working_path, BASE_VERSION)
    branch_name = git_manager.get_branch_name()
    expected = git_manager.generate_breville_version()

    package_final(branch_name, package_setup_git[1], working_path)

def test_setup_master(package_setup_git):
    working_path = package_setup_git[0]
    repo = Repo(working_path)

    for n in range(5):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager = GitManager(working_path, BASE_VERSION)
    branch_name = git_manager.get_branch_name()
    expected = git_manager.generate_breville_version()
    logger.info("+-+-+-+-   " + expected)
    logger.info("+-+-+-+-   " + str(working_path))
    logger.info("+-+-+-+-   " + str(package_setup_git[1]))

    package_final(branch_name, package_setup_git[1], working_path)


def test_big_show(package_setup_git):
    working_path = package_setup_git[0]
    repo = Repo(working_path)

    branch_name = "dev_BZC-234"
    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(5):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
        if n % 2 == 1:
            package_final(branch_name, package_setup_git[1], working_path)

    repo.git.checkout('master')

    repo.git.merge(branch_name)
    package_final('master', package_setup_git[1], working_path)

    assert repo.git.describe("--tag") == "ver_9.0.0"
    
    branch_name = "dev_BZC-312"
    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(5, 10):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
        if n % 2 == 1:
            package_final(branch_name, package_setup_git[1], working_path)

    repo.git.checkout('master')

    repo.git.merge(branch_name)
    package_final('master', package_setup_git[1], working_path)

    assert repo.git.describe("--tag") == "ver_9.0.1"

    with open(working_path / package_setup_git[1]) as c:
        config_dict = json.load(c)

    config_dict["base_version"] = ["9", "3"]

    with open(working_path / package_setup_git[1], 'w+') as config_file:
        json.dump(config_dict, config_file)
    
    branch_name = "dev_BZC-345"
    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(10, 12):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
        if n % 2 == 1:
            package_final(branch_name, package_setup_git[1], working_path)

    repo.git.checkout('master')
    repo.git.merge(branch_name)

    package_final('master', package_setup_git[1], working_path)
    assert repo.git.describe("--tag") == "ver_9.3.0"

    hello = working_path / f'hello{12}.txt'
    hello.write_text('hello world!')
    repo.git.add('--all')
    repo.index.commit(f"final - commits")

    package_final('master', package_setup_git[1], working_path)
    assert repo.git.describe("--tag") == "ver_9.3.1"


def test_config_no_jobs(config_no_jobs_file):
    working_path = config_no_jobs_file[0]
    repo = Repo(working_path)
    branch_name = "dev_BZC-234"

    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(15):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")

    git_manager = GitManager(working_path, BASE_VERSION)
    branch_name = git_manager.get_branch_name()

    package_final(branch_name, config_no_jobs_file[1], working_path)


def test_config_without_zip(config_flat_file):
    working_path = config_flat_file[0]
    repo = Repo(working_path)

    for n in range(5):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")

    git_manager = GitManager(working_path, BASE_VERSION)
    branch_name = git_manager.get_branch_name()
    expected = git_manager.generate_breville_version()

    logger.info("test_config_without_zip " + expected)
    logger.info("test_config_without_zip " + str(working_path))
    logger.info("test_config_without_zip " + str(config_flat_file[1]))

    package_final(branch_name, config_flat_file[1], working_path)