import pytest
import logging
import re

from package_tool import (
    GitManager,
    ConfigParser,
    JobParser
)

logger = logging.getLogger()

def test_load_config_bad_publish_path(config_publish_path_not_exist):
    with pytest.raises(FileNotFoundError):
        ConfigParser(config_publish_path_not_exist)

def test_load_config(config_file):
    ConfigParser(config_file)

def test_load_config_get_version(config_file):
    parser = ConfigParser(config_file)
    logger.debug("Found Version: " + str(parser.get_version()))
    assert parser.get_version() == ["9","0"]

def test_load_config_check_jobs(config_file):
    parser = ConfigParser(config_file)
    jobs = parser.get_jobs()

    for job in jobs:
        assert type(job) == JobParser

def test_check_job_file_types(config_file):
    parser = ConfigParser(config_file)
    jobs = parser.get_jobs()
    for job in jobs:
        type_list = job.get_types()

    assert "resource" in type_list
    assert "comm_mcu" in type_list

def test_check_job_file_path(config_with_src_files):
    parser = ConfigParser(config_with_src_files)
    jobs = parser.get_jobs()
    
    jobs[0].get_file_path("comm_mcu")

def test_check_job_files(config_with_built_files):
    parser = ConfigParser(config_with_built_files)
    jobs = parser.get_jobs()

    jobs[0].extract_file_versions()

def test_check_job_filename_date(config_with_built_files):
    FILE_NAME_PATTERN = r"^.{6}_\d{3}_\D{2,8}_\d{,5}\.\d{,5}\.\d{,5}_0x[A-Fa-f0-9]{8}_\d{6}.*\.bin$"
    parser = ConfigParser(config_with_built_files)
    jobs = parser.get_jobs()

    for job in jobs:
        for file in job.config["files"]:
            f_name = job.get_file_name(file['type'], '0x12345678', "1.2.0")
            logger.info(f"{f_name}")
            assert re.search(FILE_NAME_PATTERN, f_name)
