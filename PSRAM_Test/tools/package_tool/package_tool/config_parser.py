'''
###############################################################################
    Copyright (c) 2020-present Breville Pty. Ltd. - All rights reserved.
###############################################################################

Config parser takes the package_tool configuation json file and provides an api
 to its elements.  In addition it provides tests of existance and correctness
 of files required to complete the configured tasks.

###############################################################################
Authors:
    shannon.mccullough@breville.com
###############################################################################
'''
import json
import re
import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger()

FILE_NAME_PATTERN = r"^.{6}_\d{3}_\D{2,8}_\d{,5}\.\d{,5}\.\d{,5}_0x[A-Fa-f0-9]{8}_\d{6}.*\.bin$"
FILE_VERSION_PATTERN = r"_\d{,5}\.\d{,5}\.\d{,5}(_|\-g[A-Fa-f0-9]+|.)"
VERSION_PARTS = r"(\d+|g\w+)"

class ConfigParser:
    def __init__(self, config_file):
        with open(config_file) as c:
            self.config = json.load(c)

        self._recursive_replace(self.config)

        if "base_version" in self.config:
            self.base_version = self.config["base_version"]
        else:
            self.base_version = None

        self.publish_path = self._load_publish_path(self.config)

        self.build_jobs = []
        for job in self.config['jobs']:
            self.build_jobs.append(JobParser(job))

    def _recursive_replace(self, config_json):
        """ Scans config for '$' and repaces any value with similarly named
            enviornment variable's value
        """
        def inner_replace(key, value, obj):
            if isinstance(value, str) and len(value) > 0 and '$' == value[0]:
                try:
                    obj[key] = os.environ[value[1:]]
                except:
                    raise KeyError(f"config expected env var {value}")

                if obj[key] == "false": obj[key] = False
                if obj[key] == "true": obj[key] = True

            elif isinstance(value, dict) or isinstance(value, list):
                self._recursive_replace(value)

        if isinstance(config_json, dict):
            for key, value in config_json.items():
                inner_replace(key, value, config_json)

        elif isinstance(config_json, list):
            for index, item in enumerate(config_json):
                inner_replace(index, item, config_json)

    def _load_publish_path(self, config):
        publish_path = Path(*config["publish_path"])
        if publish_path.exists():
            return publish_path
        else:
            raise FileNotFoundError(publish_path)

    def get_publish_path(self):
        return self.publish_path

    def get_jobs(self):
        return self.build_jobs

    def get_version(self):
        return self.base_version

    def get_version_path(self):
        if "version_path" in self.config:
            return Path(*self.config["version_path"])
        else:
            return Path.cwd()

    def get_tag_prefix(self):
        if "tag_prefix" in self.config:
            return self.config["tag_prefix"]
        else:
            return ""

    def get_git_strategy(self):
        return self.config["git_strategy"]

class JobParser:
    def __init__(self, config):
        self.config = config

    def check_file_names(self):
        for file in self.config["files"]:
            if "input_file_name" in file:
                if not re.search(FILE_NAME_PATTERN, file["input_file_name"]):
                    return False
        return True

    def get(self, key):
        value = None
        if key in self.config:
            value = self.config[key]
        return value

    def get_types(self):
        types = []
        for file in self.config["files"]:
            types.append(file["type"])
        return types

    def extract_file_versions(self):
        for file in self.config["files"]:
            if "input_file_name" in file:
                logger.debug("extract_file_version = " + str(file["input_file_name"]))
                version = re.search(FILE_VERSION_PATTERN, file["input_file_name"])
                file["version"] = re.findall(VERSION_PARTS, version[0])
            if "file_name" in file:
                file["version"] = ""

    def check_files_exist(self):
        for file in self.config["files"]:
            if "file_name" in file:
                path = Path(*file["file_location"]) / file["file_name"]
            elif "input_file_name" in file:
                path = Path(*file["file_location"]) / file["input_file_name"]
            else:
                raise FileNotFoundError("file name to check not in config")

            if path.exists():
                file["full_path"] = path
            else:
                raise FileNotFoundError(path)

    def get_file_path(self, file_type):
        # path to file whcih must be renamed and versioned
        for file in self.config["files"]:
            if file["type"] == file_type:
                if "file_name" in file:
                    logger.info("file_name: " + str(file["file_name"]))
                    return Path(*file["file_location"]) / file["file_name"]

                elif "input_file_name" in file:
                    logger.info("input_file_name: " + str(file["input_file_name"]))
                    return Path(*file["file_location"]) / file["input_file_name"]

                else:
                    raise FileNotFoundError("file name to get not in config")

    def get_file_name(self, file_type, checksum="0xFFFFFFFF", version_string=""):
        for file in self.config["files"]:
            if file["type"] == file_type:
                if "file_name" in file:
                    if "hash" not in file:
                        file["hash"] = checksum
                    identifiers = (
                        "model",
                        "voltage",
                        "type_code",
                        "next_version",
                        "hash",
                        "date",
                    )
                    name = ''
                    for id in identifiers:
                        if (id == "next_version" and "next_version" in file):
                            if version_string != "":
                                name += f"{version_string}_"
                                file["version"] = [version_string]

                        elif (id == 'date' and 'date' in file):
                            name += f"{datetime.now().strftime('%y%m%d')}_"

                        elif id in file:
                            name += f"{file[id]}_"

                        elif id in self.config:
                            name += f"{self.config[id]}_"

                    return f"{name[:-1]}.{file['extension']}"

                elif "input_file_name" in file:
                    return file["input_file_name"]

                else:
                    raise FileNotFoundError("file name not found in config")

    def get_file_version(self, file_type):
        for file in self.config["files"]:
            if file["type"] == file_type:
                return ".".join(file["version"])

    def get_variant(self):
        resp = ""
        if "model" in self.config: resp += f"{self.config['model']}_"
        if "voltage" in self.config: resp+= f"{self.config['voltage']}_"
        if "package_type" in self.config: resp +=  f"{self.config['package_type']}"
        if resp == "": raise LookupError(
            "config must include at least one - model, voltage, package_type"
        )
        return resp

    def subdirectories_enabled(self):
        if "subdirectories" in self.config.keys():
            return bool(self.config["subdirectories"])
        else:
            return False

    def manifest_enabled(self):
        if "manifest" in self.config.keys():
            return bool(self.config["manifest"])
        else:
            return False

    def zip_enabled(self):
        if "zip" in self.config.keys():
            return bool(self.config["zip"])
        else:
            return True

    def is_required(self):
        if "required" in self.config.keys():
            return bool(self.config["required"])
        else:
            return True
