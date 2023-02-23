/* Hello World Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "esp_log.h"

const static char *TAG = "";

static void task1(void *task_num)
{

    while (true)
    {
        printf("CPU Start\n");
        ESP_LOGI(TAG, "Hello world");
       vTaskDelay(1000);
       
    }
     vTaskDelete(NULL);
 
    }

void app_main(void)

{
    xTaskCreate(task1, "task", 2048, NULL, 1, NULL);
  
    printf("test test test test test test \n");
}