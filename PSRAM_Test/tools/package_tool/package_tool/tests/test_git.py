import pytest
import logging
from pathlib import Path
from git import Repo

from package_tool import (
    GitManager,
    ConfigParser,
)

logger = logging.getLogger()

BASE_VERSION = ["5", "2"]

def test_git(git_repo):

    GitManager(git_repo, BASE_VERSION)

def test_get_branch_name(git_repo):
    git_manager = GitManager(git_repo, BASE_VERSION)
    branch_name = git_manager.get_branch_name()
    assert branch_name == "master"

def test_next_version(git_repo):
    git_manager = GitManager(git_repo, BASE_VERSION)
    next_version_string = git_manager.get_next_version_string()
    assert next_version_string == '5.2.1'

def test_next_patch_4(git_repo):
    git_manager = GitManager(git_repo, BASE_VERSION)
    next_patch_string = git_manager.patch_based_on_last_tag()
    assert next_patch_string == "1"

def test_sort_tags_multi_digits(git_repo):
    working_path = git_repo
    repo = Repo(working_path)

    for n in range(23):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
        if n % 2 == 1:
            git_manager = GitManager(git_repo, BASE_VERSION)
            git_manager.write_tag()
    
    next_patch_string = git_manager.generate_breville_version()

    assert "5.2.11" == next_patch_string

def test_next_patch_commits(git_repo):
    working_path = git_repo
    repo = Repo(working_path)

    for n in range(12):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager = GitManager(git_repo, BASE_VERSION)
    next_patch_string = git_manager.patch_based_on_commit_count()
    # n + <0 index correctin> + <initial commit>
    assert f"{n + 2}-g" in next_patch_string


def test_next_patch_commits_off_branch(git_repo):
    working_path = git_repo
    repo = Repo(working_path)
    branch_name = "dev_BZC-234"

    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(13):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager = GitManager(git_repo, BASE_VERSION)
    next_patch_string = git_manager.patch_based_on_commit_count()
    
    assert f"{n + 2}-g" in next_patch_string


def test_write_tags(git_repo):
    working_path = git_repo
    repo = Repo(working_path)
    branch_name = "dev_BZC-234"

    repo.git.branch(branch_name)
    repo.git.checkout(branch_name)

    for n in range(4):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager_1 = GitManager(git_repo, BASE_VERSION)

    next_patch_string = git_manager_1.generate_breville_version()
    git_manager_1.write_tag()

    logger.info("First Tag written: " + next_patch_string)

    for n in range(4, 10):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager_2 = GitManager(git_repo, BASE_VERSION)

    next_patch_string = git_manager_2.generate_breville_version()
    git_manager_2.write_tag()

    logger.info("Second Tag written: " + next_patch_string)

    for n in range(10, 12):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")
    
    git_manager_3 = GitManager(git_repo, BASE_VERSION)
    next_patch_string = git_manager_3.generate_breville_version()
    git_manager_3.write_tag()
    logger.info("LAST Tag written: " + next_patch_string)

    assert f"{n + 2}-g" in next_patch_string


def test_prfix_empty_string(git_repo):
    working_path = git_repo
    repo = Repo(working_path)

    for n in range(12):
        hello = working_path / f'hello{n}.txt'
        hello.write_text('hello world!')
        repo.git.add('--all')
        repo.index.commit(f"{n} - commits")

    git_manager = GitManager(git_repo, BASE_VERSION, prefix="")
    repo.create_tag("5.2.5")
    repo.create_tag("BROKEN")
    next_patch_string = git_manager.patch_based_on_last_tag()
    assert "6" in next_patch_string
