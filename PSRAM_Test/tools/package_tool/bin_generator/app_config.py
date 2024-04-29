import json
import logging
import re
from datetime import datetime
from pathlib import Path

from bin_generator.file_to_treat import FileToTreat

logger = logging.getLogger(__name__)
VERSION_PATTERN = r"\d{,5}\.\d{,5}\.\d{,5}"

class AppConfig:

    NAMEPREFIX = "BMC800"
    HEADERSIZE = 1024
    NAND_OUTPUT_SUFFIX = "NAND.bin"

    BOOTLOADER1 = 0
    APPLICATION = 1
    NOR_FLASH = 2
    NAND_FLASH = 3
    POWER_BOARD = 4
    SOUNDCHIP = 5
    RESERVED = 6
    PACKAGE = 7
    BOOTLOADER0 = 8
    SAFETY_LIBRARY = 9
    CONNECTIVITY_BOOTLOADER = 10
    CONNECTIVITY_APPLICATION = 11
    
    def __init__(self, version, voltage=None, workspace="workspace", boot1=None,
                 app_hex=None, nand_dir=None, power_board=None, sound=None,
                 comms_boot=None, comms_app=None, production_files=False):

        logger.info(
            f"{version}, {voltage}, {boot1}, {app_hex}, {nand_dir},"
            f"{power_board}, {sound}, {comms_boot}, {comms_app}, {production_files}"
        )

        self.version = version
        self._full_version = version
        self._voltage = voltage
        self._production_files = production_files
        self.working_dir = Path(workspace)
        self.working_dir.mkdir(parents=True, exist_ok=True)

        self.final_package_with_binary = self.working_dir / Path(
            "final_package_with_binary"
        )

        self.bin_with_header_dir = self.working_dir / Path(
            "bin_with_header_dir"
        )

        self.generated_bin_dir = self.working_dir / Path(
            "generated_bin_dir"
        )

        self._input_list = []

        if boot1 != None:
            if not Path(boot1).exists(): 
                raise FileNotFoundError('file not found')

            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.BOOTLOADER1,
                    path_string=boot1
                )
            )

        if app_hex != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.APPLICATION,
                    path_string=app_hex
                )
            )
        
        if nand_dir != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.NAND_FLASH,
                    path_string=nand_dir
                )
            )

        if power_board != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.POWER_BOARD,
                    path_string=power_board
                )
            )

        if sound != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.SOUNDCHIP,
                    path_string=sound
                )
            )

        if comms_boot != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.CONNECTIVITY_BOOTLOADER,
                    path_string=comms_boot
                )
            )

        if comms_app != None:
            self._input_list.append(
                FileToTreat(
                    version,
                    AppConfig.CONNECTIVITY_APPLICATION,
                    path_string=comms_app
                )
            )


    def _trim_git_hash(self, version):
        version_string = re.search(VERSION_PATTERN, version)
        return version_string[0]

    @property
    def input_file_list(self):
        return self._input_list
    
    @property
    def full_version(self):
        return self._full_version

    @property
    def version(self):
        if hasattr(self, '_version'):
            return self._version
        else:
            return None

    @version.setter
    def version(self, version):
        self._version = self._trim_git_hash(version)

    @property
    def voltage(self):
        return self._voltage

    @property
    def date_str(self):
        return datetime.now().strftime("%d%m%y")
    
    @property
    def production_files(self):
        return self._production_files
