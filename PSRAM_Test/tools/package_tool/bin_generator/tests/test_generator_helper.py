import pytest
import logging
from pathlib import Path

from bin_generator.app_config import AppConfig
from bin_generator.file_to_treat import FileToTreat
from bin_generator.generator_helper import (
    write_package,
    write_nor_package,
    generate_nand,
    generate_bin_with_header,
    generate_partition_with_hex,
    crc32_fsl
)


logger = logging.getLogger()


def test_crc32_fsl(app_config_fixture):
    seed = 0
    buff = bytearray()

    for i in range(1000):
        buff.extend(i.to_bytes(2, byteorder="little"))

    crc = crc32_fsl(seed, buff, buf_len=len(buff))

    logger.info(f"caculated crc is: {str(crc)}")


def test_generate_partition_with_hex(bin_source, app_config_fixture):

    hex_file_path = bin_source / "BMC800_BBB_APPNOR.hex"
    ftt = FileToTreat(version="10.20.30", type=1, path_string=hex_file_path)
    generate_partition_with_hex(ftt, app_config_fixture)

def test_generate_partition_NOR_with_hex(bin_source):

    version = "1.2.3"
    voltage = "120"

    hex_file_path = bin_source / "BMC800_BBB_APPNOR.hex"

    app_config = AppConfig(version, voltage,
        app_hex=hex_file_path,
        production_files=True,
        )

    ftt = FileToTreat(version="10.20.30", type=1, path_string=hex_file_path)
    file_list = generate_partition_with_hex(ftt, app_config)

    logger.info(f"--------------- -------- - - - - - {len(file_list)}")

    for binfile in file_list:
        logger.info(f"object type: {type(binfile)}\t file type: {binfile.file_type_num}")
        write_nor_package(binfile, app_config)



def test_generate_bin_with_header(path_root, bin_source, app_config_fixture):

    bin_file_path = (
        bin_source / "BV1888L1_120_PB_A_1.0.1_0x004F7721_20200706.bin"
    )
    ftt = FileToTreat(version="2.3.4", type=4, path_string=bin_file_path)

    generate_bin_with_header(ftt, app_config_fixture)


def test_generate_nand(nand_folder,app_config_fixture):
    version = "5.6.7"
    ftt = FileToTreat(version, type=3, path_string=nand_folder)

    generate_nand(ftt, app_config_fixture)

def test_generate_nand_seperate(nand_folder, bin_source):
    version = "12.34.56"
    voltage = "120"

    app_config = AppConfig(version, voltage,
        nand_dir=nand_folder,
        production_files=True,
        )
    ftt = FileToTreat(version, type=3, path_string=nand_folder)

    bin_file_without_header = generate_nand(ftt, app_config)
    bin_with_header = generate_bin_with_header(bin_file_without_header, app_config)
    write_package([bin_with_header], app_config)
