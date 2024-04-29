import logging
from argparse import ArgumentParser
from pathlib import Path

from bin_generator.generator_helper import (
    write_package,
    write_nor_package,
    generate_nand,
    generate_bin_with_header,
    generate_partition_with_hex
)
from bin_generator.file_to_treat import FileToTreat
from bin_generator.app_config import AppConfig

logger = logging.getLogger()


def run(config):
    '''

    '''
    listOfFileToGenerate = []
    listOfFileToTreat = []
    app_file_to_generate = None
    nor_file_to_generate = None
    nand_file_to_generate = None

    for input_file in config.input_file_list:
        logger.info(f":: run :: input_file = {input_file.filename}")

        if input_file.path.is_dir():
            logger.info(
                f"--- generate bin with header from dir, ie NAND content ---"
            )
            bin_file_without_header = generate_nand(input_file, config)
            bin_with_header = generate_bin_with_header(bin_file_without_header, config)
            listOfFileToGenerate.append(bin_with_header)
            if config.production_files:
                nand_file_to_generate = bin_with_header

        elif input_file.path.suffix.upper() == '.HEX':
            logger.info(f"--- generate .bin with header from .HEX ---")
            listOfFileToTreat = generate_partition_with_hex(input_file, config)

            if (len(listOfFileToTreat) != 0 and listOfFileToTreat != None):
                for fileToTreat in listOfFileToTreat:
                    bin_with_header = generate_bin_with_header(fileToTreat, config)

                    if bin_with_header.file_type_num == 1 and config.production_files:
                        app_file_to_generate = bin_with_header
                        listOfFileToGenerate.append(bin_with_header)
                        logger.info(f"------------ adding app")

                    elif bin_with_header.file_type_num == 2 and config.production_files:
                        nor_file_to_generate = fileToTreat
                        logger.info(f"------------ adding nor")

                    else:
                        listOfFileToGenerate.append(bin_with_header)
                        logger.info(f"------------ adding res")

        elif input_file.path.suffix.upper() == '.BIN':
            logger.info("--- generate .bin with header from .bin without ---")
            bin_with_header = generate_bin_with_header(input_file, config)
            listOfFileToGenerate.append(bin_with_header)

        else:
            raise ValueError(
                f"UNSUPPORTED FILE PATH or EXTENSION: {input_file.path.suffix}"
            )

    if config.production_files == False and not len(listOfFileToTreat) == 0:
        logger.info("---- generate final bin package ----")
        write_package(listOfFileToGenerate, config, "RES")

    elif config.production_files == True and not len(listOfFileToTreat) == 0:
        logger.info("---- generate final seperate bin packages ----")
        write_package(listOfFileToGenerate, config, "PROD")
        write_package([app_file_to_generate], config, "APP")
        write_package([nand_file_to_generate], config, "NAND")

    if config.production_files == True and nor_file_to_generate:
        write_nor_package(nor_file_to_generate, config)


def main():
    parser = ArgumentParser("bulid tool for BMC800 .bin upgrade package")
    parser.add_argument(
        '--version', help='bin package version and default for all',
        default=None
    )
    parser.add_argument(
        '--voltage', help='bin package target voltage',
        default=None
    )
    parser.add_argument(
        '--workspace', help='working directory from cwd',
        default="workspace"
    )
    parser.add_argument(
        '--boot1', help='boot1 bin path',
        default=None
    )
    parser.add_argument(
        '--app-hex', help='appliaction and nor hex path',
        default=None
    )
    parser.add_argument(
        '--nand-dir', help='nand content directory',
        default=None
    )
    parser.add_argument(
        '--power-board', help='power board bin path',
        default=None
    )
    parser.add_argument(
        '--sound', help='sound chip bin path',
        default=None
    )
    parser.add_argument(
        '--comms-boot', help='esp32 bootloader bin path',
        default=None
    )
    parser.add_argument(
        '--comms-app', help='esp32 appliaction bin path',
        default=None
    )
    parser.add_argument(
        '--production_files', help='appliaction and nor hex path',
        default=False, action='store_true'
    )
    parser.add_argument(
        '--log-level', 
        help=f'set the logging level: {logging._nameToLevel}',
        choices=logging._nameToLevel,
        default = 'info'
    )

    args = parser.parse_args()
    logging.basicConfig(
        format='%(relativeCreated)6d %(process)6d %(threadName)s %(message)s',
        level=logging._nameToLevel[args.log_level.upper()]
    )

    arg_list = {}
    for arg, value in args.__dict__.items():
        # any arg name that matches config class is added to arg_list
        if arg in AppConfig.__init__.__code__.co_varnames:
            arg_list[arg] = value

    config_obj = AppConfig(**arg_list)

    run(config_obj)

if __name__ == "__main__":
    main()
