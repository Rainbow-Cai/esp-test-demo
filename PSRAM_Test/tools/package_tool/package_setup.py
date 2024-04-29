'''
###############################################################################
    Copyright (c) 2020-present Breville Pty. Ltd. - All rights reserved.
###############################################################################

package setup loads the configuraiton, checks all the provided file names meet 
naming requirements and runs some checks to ensure that those files exist.

Then it will produce two new files, one with a version number and one with the
last commit log entry.

###############################################################################
Authors:
    shannon.mccullough@breville.com
###############################################################################
'''
import logging
from shutil import copy
from argparse import ArgumentParser
from pathlib import Path

from package_tool import (
    GitManager,
    ConfigParser
)

logging.basicConfig(
    level=logging.INFO,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)

logger = logging.getLogger(__name__)

FILENAME_CONFIG = "package_config.json"
FILENAME_VERSION = "version.txt"
FILENAME_LOG = "log.txt"

def package_setup(branch_name, config_file, working_directory=None, force_tag='0'):
    '''
    This module when run:
     - checks if configured input files match naming spec
     - creates build_version.txt which contains the next version number
     - creates a log.txt which includs the current git commit log
    '''
    if working_directory == None:
        working_directory = Path.cwd()
    
    config = ConfigParser(working_directory / config_file)

    git_manager = GitManager(
        working_directory,
        config.get_version(),
        config.get_tag_prefix(),
        branch_name
    )

    version_path = config.get_version_path()
    version_path.mkdir(parents=True, exist_ok=True)

    # for files with input names, checks name matches requirements.
    for job in config.get_jobs():
         job.check_file_names()

    path_build_info = version_path / FILENAME_VERSION
    with open(path_build_info, 'w+') as f:
        f.write(git_manager.generate_breville_version())

    path_log = version_path / FILENAME_LOG
    with open(path_log, 'w+') as f:
        f.write(git_manager.get_git_log())

    if force_tag == '1':
        git_manager.write_tag()

def main():
    parser = ArgumentParser("Jenkins runs with detached head - BRANCH needed")
    parser.add_argument(
        '--branch', help='branch name',
        default='master'
    )
    parser.add_argument(
        '--config', help='configuration json file',
        default=FILENAME_CONFIG
    )
    parser.add_argument(
        '--force-tag', help='setting to "1" creates tag on setup',
        default='0'
    )
    args = parser.parse_args()
    logger.info(f"working on branch: {args.branch}")

    package_setup(args.branch, args.config, force_tag=args.force_tag)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(relativeCreated)6d %(threadName)s %(message)s'
    )

    main()


