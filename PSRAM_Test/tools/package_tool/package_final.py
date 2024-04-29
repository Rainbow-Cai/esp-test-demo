'''
###############################################################################
    Copyright (c) 2020-present Breville Pty. Ltd. - All rights reserved.
###############################################################################

package final should be called after building and testing artifacts.  It will 
re-name if required and package the build into a .zip file in the file share.
The package will be uniquiely named with the version number of the build.

###############################################################################
Authors:
    shannon.mccullough@breville.com
###############################################################################
'''

import logging
import json
import zlib
import os
from argparse import ArgumentParser
from shutil import make_archive, rmtree, copy, copytree
from pathlib import Path

from package_tool import (
    GitManager,
    ConfigParser
)

logger = logging.getLogger(__name__)
FILENAME_CONFIG = "package_config.json"


def custom_copy_tree(src, dst, symlinks=False, ignore=None):
    """ because older Python versions (3.6) don't support 'dirs_exist_ok'
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def create_package_directory(job_config, variant_path, version):
    '''
    First creats a path for the package (job)
    Second creates a path from each file type in the job
    '''
    package_path = Path(variant_path) / f"{job_config.get_variant()}_{version}"
    rmtree(package_path, ignore_errors=True)
    package_path.mkdir(parents=True, exist_ok=True)

    return package_path


def create_file_type_directories(job_config, package_path, version):
    '''
    First creats a path for the package (job)
    Second creates a path from each file type in the job
    '''
    variant_file_dst_paths = {}
    for file_type in job_config.get_types():
        variant_file_path = Path(package_path) / file_type
        variant_file_dst_paths[file_type] = variant_file_path
        variant_file_path.mkdir(exist_ok=True)

    return variant_file_dst_paths


def copy_files_into_package(job_config, variant_file_dst, version):
    '''
    spins through each file type in the job and copies from source into
    the desination.  
    '''
    for file_type in job_config.get_types():
        if isinstance(variant_file_dst, dict):
            dst_dir = variant_file_dst[file_type]
        else:
            dst_dir = variant_file_dst

        checksum = calculate_crc32(job_config.get_file_path(file_type))

        src_path = job_config.get_file_path(file_type)
        dst_path = Path(dst_dir) / job_config.get_file_name(file_type, checksum, version)

        copy(src_path, dst_path)


def create_manifest(config, variant_path, version):

    manif_path = Path(variant_path) / f"{config.get_variant()}_{version}.json"
    asset_list = []

    for file_type in config.get_types():
        checksum = calculate_crc32(config.get_file_path(file_type))
        asset_list.append(
            {
                "type": file_type,
                "file": [
                    config.get_file_name(file_type, checksum, version)
                ],
                "ver": config.get_file_version(file_type)
            }
        )

    manifest = {
        "ver": version,
        "model":config.get("model")
    }
    
    model_type = config.get("model_type")
    if model_type is not None:
        manifest["model_type"] = model_type

    manifest["brand"] = config.get("brand")
    manifest["asset"] = asset_list

    with open(manif_path, 'w') as m:
        json.dump(manifest, m, indent=4)


def create_zip_ota_package(config, variant_path, version, base_path):
    dst_path = Path(base_path) / f"{config.get_variant()}_{version}"
    make_archive(dst_path, 'zip', root_dir=variant_path)

    return dst_path


def calculate_crc32(binary_file):
    logger.info(f"calculate_crc32 path: {binary_file}")
    with open(binary_file, "rb") as f:
        checksum = hex(zlib.crc32(f.read()))
        return checksum

    raise Exception("Could not calculate crc32")


def package_final(branch_name, config_file, working_directory=None, write_tag='1'):
    if working_directory == None:
        working_directory = Path.cwd()

    config = ConfigParser(working_directory / config_file)

    git_manager = GitManager(
        working_directory,
        config.get_version(),
        config.get_tag_prefix(),
        branch_name
    )

    base_path = working_directory / "packager"
    next_version = git_manager.generate_breville_version()

    for job in config.get_jobs():
        if not job.is_required():
            continue

        variant_path = base_path / job.get_variant()
        job.check_file_names()
        job.extract_file_versions()

        job.check_files_exist()

        package_path = create_package_directory(
            job,
            variant_path,
            next_version
        )

        if job.subdirectories_enabled():
            variant_file_dst_paths = create_file_type_directories(
                job,
                package_path,
                next_version
            )
            copy_files_into_package(job, variant_file_dst_paths, next_version)

        else:
            copy_files_into_package(job, package_path, next_version)

        if job.manifest_enabled():
            logger.info("creating manifest")
            create_manifest(job, package_path, next_version)

        if job.zip_enabled():
            package_path = create_zip_ota_package(
                job,
                variant_path,
                next_version,
                base_path
            )

        else:
            package_path = variant_path

        artifact_path = Path(
            config.get_publish_path()
        )

        if not artifact_path.exists():
            artifact_path.mkdir(parents=True)

        if Path.is_dir(package_path):
            custom_copy_tree(package_path, artifact_path)
        else:
            copy(f"{package_path}.zip", artifact_path)

        logger.info("get_publish_path" + str(config.get_publish_path()))

    if git_manager.get_is_publish_branch() and write_tag == '1':
        git_manager.write_tag()

    if base_path.exists():
        rmtree(base_path)

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
        '--write-tag', help='setting to "0" stops tags being added to repo',
        default='1'
    )
    args = parser.parse_args()
    logger.info(f"working on branch: {args.branch}")

    package_final(args.branch, args.config, write_tag=args.write_tag)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(relativeCreated)6d %(threadName)s %(message)s'
    )

    main()


