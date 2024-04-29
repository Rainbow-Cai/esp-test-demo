import pytest
import logging
from pathlib import Path

from bin_generator.__main__ import run


logger = logging.getLogger()


def test_full_generate_run(app_config_fixture):
    
    run(app_config_fixture)

