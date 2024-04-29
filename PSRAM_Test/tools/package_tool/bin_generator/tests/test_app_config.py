from bin_generator.app_config import AppConfig

boot1="bin_generator/tests/data/BMC800_BOOT1_H_1.4.0_0x00793D1A_200914.bin"
app_hex="bin_generator/tests/data/BMC800_BBB_APPNOR_V.V.V_0xFFFFFF_YYMMDD.hex"
nand_dir="bin_generator/tests/data/NandFlashContent"
power_board="bin_generator/tests/data/BV1888L1_120_PB_A_1.0.1_0x004F7721_20200706.bin"
comms_boot="bin_generator/tests/data/esp32_app.bin"
comms_app="bin_generator/tests/data/esp32_boot.bin"

def test_app_load_a_file():
    version = "1.2.3"
    voltage = "120"

    AppConfig(version, voltage, app_hex=app_hex)

def test_app_load_all_files():

    version = "1.2.3"
    voltage = "120"

    AppConfig(version, voltage,
        boot1=boot1,
        app_hex=app_hex,
        nand_dir=nand_dir,
        power_board=power_board,
        comms_boot=comms_boot,
        comms_app=comms_app
        )

def test_loads_correct_version():
    version = "1.2.3"
    voltage = "120"

    app_config = AppConfig(version, voltage,
        boot1=boot1,
        )

    assert app_config.version == "1.2.3"

def test_trims_githash_from_version():
    version = "4.5.6-g6a0b9e1"
    voltage = "120"

    app_config = AppConfig(version, voltage,
        boot1=boot1,
        )

    assert app_config.version == "4.5.6"
