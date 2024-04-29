import pytest
import os
import logging
import json
import shutil
from pathlib import Path
from git import Repo

logger = logging.getLogger()


def pytest_configure():
    pytest.registration_code = None


@pytest.fixture(scope="session")
def config_file(tmp_path_factory ):
    config = Path(tmp_path_factory.mktemp("conf") / "config.json")
    dest = Path(tmp_path_factory.mktemp("dest"))
    src_comm = Path(tmp_path_factory.mktemp("comm_mcu"))
    src_res = Path(tmp_path_factory.mktemp("resource"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = dest.parts
    config_dict["jobs"][0]["files"][0]["file_location"] = src_comm.parts
    config_dict["jobs"][0]["files"][1]["file_location"] = src_res.parts

    logger.info(str(config_dict))

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    return config


@pytest.fixture(scope="session")
def config_publish_path_not_exist(tmpdir_factory):
    config = Path(tmpdir_factory.mktemp("conf").join("config.json"))
    src_comm = Path(tmpdir_factory.mktemp("comm_mcu"))
    src_res = Path(tmpdir_factory.mktemp("resource"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = Path("not/a/path").parts
    config_dict["jobs"][0]["files"][0]["file_location"] = src_comm.parts
    config_dict["jobs"][0]["files"][1]["file_location"] = src_res.parts

    logger.info(str(config_dict))

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    return config


@pytest.fixture(scope="session")
def config_with_src_files(tmpdir_factory):
    wifi_file = "BMC800_120_WIFIAPP_2.1.0_0x05FCB90F_200504.bin"
    res_file = "BMC800_120_RES_0.6.1_0x8B292186_200207.bin"
    config = Path(tmpdir_factory.mktemp("conf").join("config.json"))
    dest = Path(tmpdir_factory.mktemp("dest"))
    src_comm = Path(tmpdir_factory.mktemp("comm_mcu"))
    src_res = Path(tmpdir_factory.mktemp("resource"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = dest.parts
    config_dict["jobs"][0]["files"][1]["file_location"] = src_comm.parts
    config_dict["jobs"][0]["files"][0]["file_location"] = src_res.parts
    config_dict["jobs"][0]["files"][1]["input_file_name"] = wifi_file
    config_dict["jobs"][0]["files"][0]["file_name"] = res_file

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    with open((src_comm / wifi_file), "w+") as f:
        f.write("asdf")

    with open((src_res / res_file), "w+") as f:
        f.write("asdf")

    return config


@pytest.fixture(scope="session")
def config_with_built_files(tmpdir_factory):
    wifi_file = "BMC800_120_WIFIAPP_2.1.1_0x05FCB90F_200505.bin"
    res_file = "BMC800.bin"
    config = Path(tmpdir_factory.mktemp("conf_built").join("config.json"))
    dest = Path(tmpdir_factory.mktemp("dest_built"))
    src_comm = Path(tmpdir_factory.mktemp("comm_mcu_built"))
    src_res = Path(tmpdir_factory.mktemp("resource_built"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = dest.parts
    config_dict["jobs"][0]["files"][1]["file_location"] = src_comm.parts
    config_dict["jobs"][0]["files"][0]["file_location"] = src_res.parts
    config_dict["jobs"][0]["files"][1]["input_file_name"] = wifi_file
    config_dict["jobs"][0]["files"][0]["file_name"] = res_file

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    with open((src_comm / wifi_file), "w+") as f:
        f.write("asdf")

    with open((src_res / res_file), "w+") as f:
        f.write("asdf")

    return config


@pytest.fixture(scope="session")
def dest_dir(tmpdir_factory):
    dest = tmpdir_factory.mktemp("root").join(["builds", "debug"])
    print(str(dest))

    return dest


@pytest.fixture(scope="function")
def git_repo(tmp_path_factory ):
    working_path = Path(tmp_path_factory.mktemp("conf"))
    hello = working_path / 'hello.txt'
    hello.write_text('hello world!')

    repo = Repo.init(working_path)
    repo.git.add('--all')

    repo.index.commit("Initial commit")
    repo.create_tag("ver_5.2.0")

    return working_path


@pytest.fixture(scope="function")
def package_setup_git(tmp_path_factory ):
    wifi_file_120 = "BMC800_120_WIFIAPP_2.1.0_0x05FCB90F_200504.bin"
    res_file_120 = "BMC800.bin"
    working_path = Path(tmp_path_factory.mktemp("conf_built"))
    config = working_path / "config.json"
    dest = Path(tmp_path_factory.mktemp("dest_built"))
    src_comm_120 = Path(tmp_path_factory.mktemp("comm_mcu_built"))
    src_res_120 = Path(tmp_path_factory.mktemp("resource_built"))
    src_comm_240 = Path(tmp_path_factory.mktemp("comm_mcu_built"))
    src_res_240 = Path(tmp_path_factory.mktemp("resource_built"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["version_path"] = working_path.parts
    config_dict["publish_path"] = dest.parts
    config_dict["jobs"][0]["files"][1]["file_location"] = src_comm_120.parts
    config_dict["jobs"][0]["files"][0]["file_location"] = src_res_120.parts
    config_dict["jobs"][0]["files"][1]["input_file_name"] = wifi_file_120
    config_dict["jobs"][0]["files"][0]["file_name"] = res_file_120

    config_dict["jobs"][1]["files"][1]["file_location"] = src_comm_240.parts
    config_dict["jobs"][1]["files"][0]["file_location"] = src_res_240.parts
    wifi_file_240 = config_dict["jobs"][1]["files"][1]["input_file_name"]
    res_file_240 = config_dict["jobs"][1]["files"][0]["input_file_name"]

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    with open((src_comm_120 / wifi_file_120), "w+") as f:
        f.write("asdf")

    with open((src_res_120 / res_file_120), "w+") as f:
        f.write("asdf")

    with open((src_comm_240 / wifi_file_240), "w+") as f:
        f.write("asdf")

    with open((src_res_240 / res_file_240), "w+") as f:
        f.write("asdf")

    repo = Repo.init(working_path)
    repo.git.add('--all')

    repo.index.commit("Initial commit")
    repo.create_tag("ver_5.2.0") 

    return working_path, config


@pytest.fixture(scope="session")
def config_no_jobs_file(tmp_path_factory ):
    working_path = Path(tmp_path_factory.mktemp("conf_built"))
    config = Path(tmp_path_factory.mktemp("conf") / "config.json")
    dest = Path(tmp_path_factory.mktemp("dest"))

    with open("package_tool/tests/package_config_2.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = dest.parts

    logger.info(str(config_dict))

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    repo = Repo.init(working_path)
    repo.git.add('--all')

    repo.index.commit("Initial commit")
    repo.create_tag("ver_5.2.0")

    return working_path, config

@pytest.fixture(scope="function")
def config_no_version_set(tmp_path_factory ):
    working_path = Path(tmp_path_factory.mktemp("conf_built"))
    config = Path(tmp_path_factory.mktemp("conf") / "config.json")
    dest = Path(tmp_path_factory.mktemp("dest"))

    with open("package_tool/tests/package_config_1.json", 'r') as f:
        config_dict = json.load(f)

    config_dict.pop("base_version")
    config_dict["publish_path"] = dest.parts
    config_dict["version_path"] = working_path.parts

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    repo = Repo.init(working_path)
    repo.git.add('--all')

    repo.index.commit("Initial commit")
    repo.create_tag("ver_5.2.0")

    return working_path, config


@pytest.fixture(scope="function")
def config_flat_file(tmpdir_factory, tmp_path_factory):
    working_path = Path(tmp_path_factory.mktemp("conf_built"))
    build = working_path / "build"
    wifi_app_dev1_bin = build / "BSV600_PRODUCTION_dev1.bin"
    wifi_app_dev1_elf = build / "BSV600_PRODUCTION_dev1.elf"
    wifi_app_dev1_map = build / "BSV600_PRODUCTION_dev1.map"
    wifi_app_prod_bin = build / "BSV600_PRODUCTION_production.bin"
    wifi_app_prod_elf = build / "BSV600_PRODUCTION_production.elf"
    wifi_app_prod_map = build / "BSV600_PRODUCTION_production.map"
    wifi_app_stg_bin = build / "BSV600_PRODUCTION_staging.bin"
    wifi_app_stg_elf = build / "BSV600_PRODUCTION_staging.elf"
    wifi_app_stg_map = build / "BSV600_PRODUCTION_staging.map"
    sompro_2_stg_bin = build / "sompro_2_staging.bin"
    sompro_2b_stg_bin = build / "sompro_2b_staging.hex"

    config = Path(tmp_path_factory.mktemp("conf") / "config.json")
    dest = Path(tmp_path_factory.mktemp("dest"))
    Path.mkdir(build)

    with open("package_tool/tests/package_config_3.json", 'r') as f:
        config_dict = json.load(f)

    config_dict["publish_path"] = dest.parts
    config_dict["jobs"][0]["files"][0]["file_location"] = wifi_app_dev1_bin.parent.parts
    config_dict["jobs"][1]["files"][0]["file_location"] = wifi_app_stg_bin.parent.parts
    config_dict["jobs"][2]["files"][0]["file_location"] = wifi_app_prod_bin.parent.parts
    config_dict["jobs"][3]["files"][0]["file_location"] = wifi_app_dev1_bin.parent.parts
    config_dict["jobs"][3]["files"][1]["file_location"] = wifi_app_dev1_elf.parent.parts
    config_dict["jobs"][3]["files"][2]["file_location"] = wifi_app_dev1_map.parent.parts
    config_dict["jobs"][3]["files"][3]["file_location"] = wifi_app_prod_bin.parent.parts
    config_dict["jobs"][3]["files"][4]["file_location"] = wifi_app_prod_elf.parent.parts
    config_dict["jobs"][3]["files"][5]["file_location"] = wifi_app_prod_map.parent.parts
    config_dict["jobs"][3]["files"][6]["file_location"] = wifi_app_stg_bin.parent.parts
    config_dict["jobs"][3]["files"][7]["file_location"] = wifi_app_stg_elf.parent.parts
    config_dict["jobs"][3]["files"][8]["file_location"] = wifi_app_stg_map.parent.parts
    config_dict["jobs"][5]["files"][0]["file_location"] = sompro_2_stg_bin.parent.parts
    config_dict["jobs"][5]["files"][1]["file_location"] = sompro_2b_stg_bin.parent.parts

    with open(config, 'w+') as config_file:
        json.dump(config_dict, config_file)

    with open((wifi_app_dev1_bin), "w+") as f:
        f.write("abcd")

    with open((wifi_app_dev1_elf), "w+") as f:
        f.write("efgh")

    with open((wifi_app_dev1_map), "w+") as f:
        f.write("ijkl")

    with open((wifi_app_prod_bin), "w+") as f:
        f.write("mnop")

    with open((wifi_app_prod_elf), "w+") as f:
        f.write("qrst")

    with open((wifi_app_prod_map), "w+") as f:
        f.write("uvwx")

    with open((wifi_app_stg_bin), "w+") as f:
        f.write("yz12")

    with open((wifi_app_stg_elf), "w+") as f:
        f.write("3456")

    with open((wifi_app_stg_map), "w+") as f:
        f.write("7890")

    with open((sompro_2_stg_bin), "w+") as f:
        f.write("sompro")

    with open((sompro_2b_stg_bin), "w+") as f:
        f.write("sommor")

    repo = Repo.init(working_path)
    repo.git.add('--all')

    repo.index.commit("Initial commit")
    repo.create_tag("ver_5.2.0")

    return working_path, config