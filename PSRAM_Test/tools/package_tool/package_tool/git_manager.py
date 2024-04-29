'''
###############################################################################
    Copyright (c) 2020-present Breville Pty. Ltd. - All rights reserved.
###############################################################################

Git Manager interfaces with the git repositiory found in the passed working 
directory.  It will analyse the tag and commit history to create new version 
numbers  

###############################################################################
Authors:
    shannon.mccullough@breville.com
###############################################################################
'''
import re
import logging
from git import Repo

logger = logging.getLogger(__name__)

VERSION_PATTERN = r"_\d{,5}\.\d{,5}"
VERSION_PARTS = r"[\d+]+"
RELESE_STRING_ID = "release"
MASTER_STRING_ID = "master"

class GitManager:
    def __init__(self, working_dir, config_version, prefix="ver_", branch=""):
        self.repo = Repo(working_dir)
        self.prefix = prefix

        # check that the reop is clean
        # if self.repo.is_dirty():
        #     raise Exception("ensure all files are checked in before building")

        #Jenkins runs in detached head, ie no branch is checked out
        self.is_publish_branch = False
        if branch == "":
            self.branch = self.repo.active_branch.name
        else:
            self.branch = branch

        if (
            self.branch == MASTER_STRING_ID or
            RELESE_STRING_ID in self.branch
        ):
            self.base_version = config_version
            self.is_publish_branch = True
        else:
            self.base_version = ['0','0']

        # Create version string based on last tag
        self.next_version_str_tag = (
            f"{self.base_version[0]}." + \
            f"{self.base_version[1]}." + \
            f"{self.patch_based_on_last_tag()}"
        )

        # Create version string based on commit count
        self.next_version_str_commit = (
            f"0.0.{self.patch_based_on_commit_count()}"
        )

        logger.debug("next_version_str_tag: " + self.next_version_str_tag)
        logger.debug("next_breville_string: " + self.next_version_str_commit)

    def get_is_publish_branch(self):
        return self.is_publish_branch

    def patch_based_on_last_tag(self):
        tag_list = self._parse_tags_for_last_patch(
            self.repo,
            self.base_version
        )
        if tag_list:
            sorted_tag_list = sorted(
                tag_list,
                key = lambda x: int(x[2]),
                reverse=True
            )
            logging.debug("list found version tags: " + str(sorted_tag_list))
            return str(int(sorted_tag_list[0][2]) + 1)

        else:
            return "0"

    def patch_based_on_commit_count(self):

        total_commits = self.repo.git.rev_list('--count', 'HEAD')
        short_hash = self.repo.git.rev_parse('--short', 'HEAD')

        # returns the count of commits as str
        return f"{total_commits}-g{short_hash}"

    def _parse_tags_for_last_patch(self, repo, version):
        tags_list = repo.tags
        vers_list = []

        for tag_ref in tags_list:
            tag = tag_ref.name
            if tag[:len(self.prefix)] == self.prefix:
                ver = tuple(re.findall(r"[\d+]+", tag[(len(self.prefix)):]))
                if len(ver)>0 and (ver[0]==version[0] and ver[1]==version[1]):
                    vers_list.append(ver)

        return vers_list

    def get_next_version_string(self):
        return self.next_version_str_tag

    def get_branch_name(self):
        return self.branch

    def write_tag(self):
        tag = f"{self.prefix}{self.generate_breville_version()}"
        self.repo.create_tag(tag)
        logger.debug("created new tag: " + tag)

    def generate_breville_version(self):
        if self.branch == MASTER_STRING_ID:
            version_string = self.next_version_str_tag
        elif RELESE_STRING_ID in self.branch:
            version_string = self.next_version_str_tag
        else:
            version_string = self.next_version_str_commit

        return version_string

    def get_git_tag(self):
        return self.repo.git.describe('--tag')

    def get_git_date(self):
        return self.repo.git.log("-n1", "--date=format:%Y-%m-%d", "--pretty=%cd")

    def get_git_time(self):
        return self.repo.git.log("-n1", "--date=format:%H:%M:%S", "--pretty=%cd")

    def get_git_commit_long_hash(self):
        return self.repo.git.log("-n1", "--pretty=%H")

    def get_git_commit_short_hash(self):
        return self.repo.git.log("-n1", "--pretty=%h")

    def get_git_commit_subject(self):
        return self.repo.git.log("-n1", "--pretty=%s")
    
    def get_git_log(self):
        return self.repo.git.log("-n1")
