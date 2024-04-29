import pytest
import logging
from pathlib import Path

from bin_generator.__main__ import run
from bin_generator.file_to_treat import FileToTreat

logger = logging.getLogger()

def test_file_to_treat(bin_source,app_config_fixture):
    bin_file_path = (
        bin_source / "BMC800_BOOT0_0x003E39D8_201006.bin"
    )

    version = "5.6.7"
    ftt = FileToTreat(version, 6, path_string=bin_file_path)
    assert ftt.version == "5.6.7"
