# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/components/bootloader/subproject"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/tmp"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/src/bootloader-stamp"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/src"
  "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "E:/esp/Espressif/frameworks/esp-idf-master/esp-idf/examples/system/deep_sleep/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
