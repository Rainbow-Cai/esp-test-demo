from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="package_tool", 
    version="0.2.0",
    author="shannon_mccullough",
    author_email="shannon.mccullough@breville.com",
    description="python packaging tool for ota firmware builds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={
        'package_tool': './package_tool',
        'bin_generator': './bin_generator'
    },
    packages=[
        'package_tool',
        'bin_generator'
    ],
    py_modules=[
        'package_setup',
        'package_final',
        'bin_generator'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.5',
    install_requires=[
        'gitpython',
    ],
    tests_requires=[
        'pytest',
        'pytest-env'
    ],
    entry_points = {
        'console_scripts': [
            'ota_package_setup = package_setup:main',
            'ota_package_final = package_final:main',
            'bmc800_bin_generator = bin_generator.__main__:main'
        ]
    },
    include_package_data=True,
)