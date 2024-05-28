/* Himem API example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_heap_caps.h"
#include "esp32/spiram.h"
#include "sdkconfig.h"



// 在代码中声明数组
static float coefficient[20] = {0.0, 0.00852, 0.0078, 0.001393, 0.00225, 0.00322, 0.0541, 0.00734, 0.0968, 0.012, 0.0109 /* 这里省略了数组的部分元素 */ };

void storeArrayToPSRAM() {
    // 使用 heap_caps_malloc() 函数分配 PSRAM 上的内存空间
    float *psramArray = (float *)heap_caps_malloc(sizeof(coefficient), MALLOC_CAP_SPIRAM);
    if (psramArray == NULL) {
        printf("无法在PSRAM上分配内存\n");
        return;
    }

    // 将数组数据复制到 PSRAM 内存空间
    memcpy(psramArray, coefficient, sizeof(coefficient));

   for (int i = 0; i < 20; i++) {
        printf("%f\n", psramArray[i]);
    }
    
    // 在这里可以进行一些操作，使用 psramArray 数组

    // 最后，释放在 PSRAM 上分配的内存
    heap_caps_free(psramArray);
}

void app_main() {
    storeArrayToPSRAM();
        // 打印存储在PSRAM中的数据
 
}
