import pytest
import logging
from pathlib import Path
from shutil import copytree

from bin_generator.app_config import AppConfig

logger = logging.getLogger()

FILES = {
    "Bootloader1": "bin_generator/tests/data/BMC800_BOOT1_H_1.4.0_0x00793D1A_200914.bin",
    "app_hex": "bin_generator/tests/data/BMC800_BBB_APPNOR.hex",
    "nand_dir": "bin_generator/tests/data/NandFlashContent",
    "power_board": "bin_generator/tests/data/BV1888L1_120_PB_A_1.0.1_0x004F7721_20200706.bin",
    "comms_boot": "bin_generator/tests/data/esp32_app.bin",
    "comms_app": "bin_generator/tests/data/esp32_boot.bin",
}

VERSION = "1.2.3"
VOLTAGE = "120"

def pytest_configure():
    pytest.registration_code = None


@pytest.fixture(scope="session")
def path_root(tmpdir_factory ):

    path_source = Path(tmpdir_factory.mktemp("temp")) #creates temp 
    path_root = path_source.parent

    return path_root

@pytest.fixture(scope="session")
def bin_source(path_root ):

    logger.info("Starting")

    #create a path to not yet existing dir
    path_source = path_root / "source"       
    
    #only works if createing a dir (pre python 3.8)
    copytree(Path("bin_generator/tests/data"), path_source)     

    files = {
        "path_src_bootloader" : path_source / "bootloader1.bin",
        "path_src_application": path_source / "app.bin",
        "path_src_nor": path_source / "nor.bin",
        "path_src_nand": path_source / "nand.bin",
        "path_src_powerboard":  path_source / "pcb.bin",
    }

    for _, f in files.items():
        with open(f, "w+") as h:
            h.write("")

    logger.info("TEMP DIRS AT:" + str(path_source))

    return path_source


@pytest.fixture(scope="module")
def app_config_fixture():
    
    app_config = AppConfig(
        VERSION,
        VOLTAGE,
        # boot1=FILES["Bootloader1"],
        app_hex=FILES["app_hex"],
        nand_dir=FILES["nand_dir"],
        # power_board=FILES["power_board"],
        # comms_boot=FILES["comms_boot"],
        # comms_app=FILES["comms_app"]
    )
    return app_config


@pytest.fixture(scope="module")
def nand_folder(path_root ):
    nand_path = path_root / "source" / "NandFlashContent"

    return nand_path
