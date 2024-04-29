from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

FILE_VERSION_PATTERN = r"_\d{,5}\.\d{,5}\.\d{,5}(_|-)"
VERSION_PATTERN = r"\d{,5}\.\d{,5}\.\d{,5}"
VERSION_PARTS = r"[\d+]+"


class FileToTreat:

    def __init__(self, version, type, path_string=None, partition=None):

        if partition != None:
            self._partition = partition
            self._file_output_path = partition.path.parts  # seems redundant
            self._path = partition.path
            self._filename = partition.path.name

        elif path_string != None:
            self._path = Path(path_string)
            self._filename = self._path.name
            self._file_output_path = self._path.parts  # seems redundant
            self._partition = None

        version_in_name = self._extract_file_versions(self._path.name)

        if version_in_name == None:
            # remove any git hash suffix
            self._version = self._trim_git_hash(version)
        else:
            self._version = version_in_name

        self._file_type_num = type

        logger.debug(
            f"new FileToTreat, path: {self._path.name}, ver: {self._version}"
        )

    def _extract_file_versions(self, file_name):
        rtn_ver = None
        version_string = re.search(FILE_VERSION_PATTERN, file_name)

        if version_string and len(version_string[0]) > 0:
            ver_list = re.findall(VERSION_PARTS, version_string[0])

            if len(ver_list[0]) > 0:
                rtn_ver = f"{ver_list[0]}.{ver_list[1]}.{ver_list[2]}"

            logger.debug(f"extracted version: {rtn_ver}, from {file_name}")
        return rtn_ver

    def _trim_git_hash(self, version):
        version_string = re.search(VERSION_PATTERN, version)
        return version_string[0]

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def partition(self):
        return self._partition

    @partition.setter
    def partition(self, partition):
        self._partition = partition

    @property
    def file_type_num(self):
        return self._file_type_num

    @file_type_num.setter
    def file_type_num(self, file_type_num):
        self._file_type_num = file_type_num

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        self._file_type = file_type

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def file_output_path(self):
        return self._file_output_path

    @file_output_path.setter
    def file_output_path(self, file_output_path):
        self._file_output_path = file_output_path


class PartitionHex:

    def __init__(self, partitionBegin, partitionEnd, path):
        self._path = path
        self._partitionBegin = partitionBegin
        self._partitionEnd = partitionEnd
        logger.debug(f"new PartitionHex instance, path: {str(self.path)}")

    @property
    def path(self):
        return self._path

    @property
    def begin(self):
        return self._partitionBegin

    @property
    def end(self):
        return self._partitionEnd
