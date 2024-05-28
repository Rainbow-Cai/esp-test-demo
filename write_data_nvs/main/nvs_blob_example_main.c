/* Non-Volatile Storage (NVS) Read and Write a Blob - Example

   For other examples please check:
   https://github.com/espressif/esp-idf/tree/master/examples

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "driver/gpio.h"
#include <string.h>

#define STORAGE_NAMESPACE "storage"
#define STORAGE_PARTITION "test"

#if CONFIG_IDF_TARGET_ESP32C3
#define BOOT_MODE_PIN GPIO_NUM_9
#else
#define BOOT_MODE_PIN GPIO_NUM_0
#endif //CONFIG_IDF_TARGET_ESP32C3


esp_err_t save_blob_test(uint32_t key)
{
    nvs_handle_t my_handle;
    esp_err_t err;
    char key_str[16];

    // Open
    err = nvs_open_from_partition(STORAGE_PARTITION, STORAGE_NAMESPACE, NVS_READWRITE, &my_handle);
    if (err != ESP_OK) return err;

    size_t required_size = 54; 

    // Read previously saved blob if available
    char* test_data = malloc(required_size * sizeof(char));
    memset(test_data, 0, 54);
    memset(test_data, 0x66, 53);

    memset(key_str, 0, sizeof(key_str));
    sprintf(key_str,"%d",key);


    err = nvs_set_blob(my_handle, key_str, test_data, required_size);
    free(test_data);

    if (err != ESP_OK) return err;

    // Commit
    err = nvs_commit(my_handle);
    if (err != ESP_OK) return err;

    // Close
    nvs_close(my_handle);
    return ESP_OK;
}



void app_main(void)
{
    esp_err_t err = nvs_flash_init_partition(STORAGE_PARTITION);
    if (err == ESP_ERR_NVS_NO_FREE_PAGES || err == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        // NVS partition was truncated and needs to be erased
        // Retry nvs_flash_init
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init_partition(STORAGE_PARTITION);
    }
    ESP_ERROR_CHECK( err );


    uint32_t count = 0;

    /* Read the status of GPIO0. If GPIO0 is LOW for longer than 1000 ms,
       then save module's run time and restart it
     */
    while (1) {
        
        err = save_blob_test(++count);
        if (err != ESP_OK) {
            printf("Error (%s) saving restart counter to NVS! count = %d\n", esp_err_to_name(err),count);
            break;
        }
        if (0 == count%1000) {
            printf("count = %d\n",count);
        }
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}
