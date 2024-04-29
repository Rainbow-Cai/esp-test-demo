'''
###############################################################################
    Copyright (c) 2023-present Breville Pty. Ltd. - All rights reserved.
###############################################################################

build_info_file generates a simple txt file in the provided path.
information is included for environment variables, mostly set by Jenkins

file and path for outptu
--output_file=my_info.txt

List of special environment variables to include in the file
--env_var_list="BES890_APP_NAME,BES890_V2_STM32_NAME"

###############################################################################
Authors:
    shannon.mccullough@breville.com
###############################################################################
'''
from argparse import ArgumentParser
import datetime
import os


def generate_basic_content():
    contents = (
        f"Breville Firmware Build Info\n"
        f"created by package_tool/build_info_file.py\n"
        f"--------------------------------------------------------------------------------\n"
        f"PRODUCT = {os.environ['PRODUCT']}\n"
        f"VERSION = {os.environ['VERSION']}\n"
        f"BUILD_DATE = {datetime.datetime.now()}\n"
        f"GIT_COMMIT = {os.environ['GIT_COMMIT']}\n"
        f"GIT_BRANCH = {os.environ['GIT_BRANCH']}\n"
        f"BUILD_NUMBER = {os.environ['BUILD_NUMBER']}\n"
        f"NODE_NAME = {os.environ['NODE_NAME']}\n"
        f"--------------------------------------------------------------------------------\n"
    )
    return contents


def new_arg_content(content, new_arg):
    content += f'{new_arg} = {os.environ[new_arg]}\n'
    return content


if __name__ == "__main__":
    parser = ArgumentParser("provide output file name and any extra vars to record.")
    parser.add_argument(
        '--output_file', help='file and path for outptu',
        default='build_info.txt'
    )
    parser.add_argument(
        '--env_var_list', help='configuration json file',
        default=""
    )
    args = parser.parse_args()
    contents = generate_basic_content()

    environment_variables = args.env_var_list.replace(' ','').split(',')

    for var in environment_variables:
        if var != '':
            contents = new_arg_content(contents, var)

    with open(args.output_file,"w") as f:
        f.write(contents)
