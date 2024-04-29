import pytest
import logging
from pathlib import Path

from bin_generator.srec_helper import SrecHelper
from bin_generator.file_to_treat import FileToTreat

logger = logging.getLogger()

VERSION = "5.2.1"
INPUT_HEX_EXAMPLE = Path("bin_generator/tests/data/BMC800_BBB_APPNOR.hex")

def test_srec_helper(app_config_fixture):
    ftt = FileToTreat(VERSION, 2, path_string=INPUT_HEX_EXAMPLE)

    SrecHelper(ftt, app_config_fixture)
