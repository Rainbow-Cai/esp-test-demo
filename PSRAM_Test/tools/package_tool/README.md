# Usage Installed Package

Once instaled the following console commands will be avaible
* ota_package_setup
    * args:
        * --branch 		required
        * --config		path to config file

* ota_package_final
    * args:
        * --branch 		required
        * --config		path to config file
        * --write-tag	default is '1', set '0' to disable

# Usage as sub-module

1. Setup the configuraiton file to build OTA and other file into packages
2. Run package_setup.py to load a version.txt file into the root directory
3. Run package_final.py to rename, copy, and zip files.

# Naming is enforced

| Name Type         | Template                                              |
| ----------------- | ----------------------------------------------------- |
| OTA packages      | AAAAAA_BBB_M.m.zip                                    |
| Firmware packages | AAAAAA_BBB_M.m.P_0xFFFF_YYMMDD(_ENC).bin              |
| Firmware files    | AAAAAA(_BBB)_XXX(_H)_M.m.P_0xFFFF_YYMMDD(_ENC).TTT    |


### where

| Code       | Description     |
| ---------- | --------------- |
| AAAAAA     | name            |
| BBB        | voltage         |
| XXX        | type_code       |
| FFFFFFFF   | checksum        |
| YYMMDD     | year month day  |


----

# Install

`git pull <url>` _repo url_

`cd package_tool` _into the directory_

`pip install .`

# Uninstall

`pip uninstall package_tool`

----

# Run Tests

`python3 -m pytest `
