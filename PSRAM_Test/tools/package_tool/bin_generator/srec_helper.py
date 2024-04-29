import logging
from pathlib import Path
from subprocess import Popen, PIPE, CalledProcessError

from bin_generator.file_to_treat import FileToTreat, PartitionHex
from bin_generator.app_config import AppConfig

SREC_TOOLS_PATH = Path(__file__).parent / "srec_tools"
SREC_CAT = SREC_TOOLS_PATH / "srec_cat.exe"
SREC_INFO = SREC_TOOLS_PATH / "srec_info.exe"

logger = logging.getLogger()

class SrecHelper:
    def __init__(self, hexFileToTreat: FileToTreat, app_config):
        self.file_name = hexFileToTreat.path.name
        self.hex_file_to_treat = hexFileToTreat
        self.file_nambe_stem = hexFileToTreat.path.stem
        self.file_index = hexFileToTreat.file_type_num
        self.version = hexFileToTreat.version
        self.app_config = app_config
        self.partition_files = []

        if self._get_addresses():
            self.app_config.generated_bin_dir.mkdir(
                parents=True,
                exist_ok=True
            )
            self._split_partitions()

    def _execute_cmd(self, cmd: str, parameters: str):
        try:
            param = parameters.split(' ')
            cmd_list = [cmd] + param
            logger.info(f"cmd: {' '.join(cmd_list)}")
            p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b'stuff')
            if output: logger.info(f"tc out: {output}")
            if err:
                logger.error(f"_execute_cmd stderr {err.decode('utf-8')}")
                raise RuntimeError(f"tc err: {err.decode('utf-8')}")
            return output.decode('utf-8')
        except CalledProcessError as exc:
            logger.info(f"Status : FAIL, {exc.returncode}, {exc.output}")
            return None

    def _get_addresses(self):
            logger.info(">>>>Getting addresses")
            infos = self._execute_cmd(
                str(SREC_INFO),
                str(self.hex_file_to_treat.path) + " -intel"
            )

            if infos == None:
                raise RuntimeError("No partitions found in .hex file")

            # parse info finding the address offsets
            for line in infos.splitlines():

                logger.debug(f"for line: {line}")

                # remove double spaces (taken from c# but probably redundant)
                line = " ".join(line.split())

                # Add parent file name into filename
                # TODO, this bits pretty dodgy
                if line[:5] == "Data:":
                    logger.debug("Data Found")
                    parameters = line.replace("\r", "").split(' ')
                    offsetInternalStart = parameters[1]
                    offsetInternalEnd = parameters[3]
                    partition = PartitionHex(
                        "0x" + offsetInternalStart,
                        "0x" + offsetInternalEnd,
                        self.app_config.generated_bin_dir / (
                            f"partition_from_{self.file_nambe_stem}"
                            f"_{str(self.file_index)}.bin"
                        )
                    )
                    partition_file_to_treat = FileToTreat(
                        self.version,
                        self.file_index,
                        partition=partition
                    )
                    self.partition_files.append(partition_file_to_treat)
                    self.file_index += 1

                elif not ":" in line:
                    logger.debug("Colon found")
                    parameters = line.replace("\r", "").split(' ')
                    if len(parameters) == 3:
                        offsetExternalStart = parameters[0]
                        offsetExternalEnd = parameters[2]
                        partition = PartitionHex(
                            "0x" + offsetExternalStart,
                            "0x" + offsetExternalEnd,
                            self.app_config.generated_bin_dir / (
                                f"partition_from_{self.file_nambe_stem}"
                                f"_{str(self.file_index)}.bin"
                            )
                        )
                        partition_file_to_treat = FileToTreat(
                            self.version, 
                            self.file_index, 
                            partition=partition
                        )
                        self.partition_files.append(partition_file_to_treat)
                        self.file_index += 1
            return True

    def _split_partitions(self):
        logger.info(">>>>Spliting partition")
        for partition_file in self.partition_files:
            addr_start = int(partition_file.partition.begin.split('x')[1], 16)
            addr_end = int(partition_file.partition.end.split('x')[1], 16)

            self._execute_cmd(
                str(SREC_CAT), 
                f'{str(self.hex_file_to_treat.path)} -intel '
                f'-crop {hex(addr_start)} {hex(addr_end + 1)} '
                f'-offset -{hex(addr_start)} -o {str(partition_file.path)} '
                f'-binary'
            )

    def get_partitions(self):
        return self.partition_files
