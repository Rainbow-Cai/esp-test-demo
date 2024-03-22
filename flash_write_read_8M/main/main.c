/* Finding Partitions Example
   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <string.h>
#include <assert.h>
#include "esp_partition.h"
#include "spi_flash_mmap.h"
#include "esp_log.h"

static const char *TAG = "example";

void app_main(void)
{
    int i;
    /*
    * This example uses the partition table from ../partitions_example.csv. For reference, its contents are as follows:
    *
    *  nvs,        data, nvs,      0x9000,  0x6000,
    *  phy_init,   data, phy,      0xf000,  0x1000,
    *  factory,    app,  factory,  0x10000, 1M,
    *  storage,    data, ,             , 0x40000,
    */

    // Find the partition map in the partition table
    const esp_partition_t *partition = esp_partition_find_first(ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_ANY, "storage");
    assert(partition != NULL);

    static char store_data[] = "ESP-IDF Partition Operations Example (Read, Erase, Write 12 dhidfsbgirgnwiiiiiiiihfehii\
    hfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhg\
    bxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuih\
    uqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsb\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsa\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsa\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsa\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsa\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsa\
    girgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuhsa\
    dggiduiauiuihuqfhsdjufuuwughdhidfsbgirgnwiiiiiiiihfehiihfgifhgbxhsadggiduiauiuihuqfhsdjufuuwugh";
    
    static char read_data[sizeof(store_data)];

    // Erase entire partition
    memset(read_data, 0xFF, sizeof(read_data));

    uint32_t write_offset = 0x0;
     ESP_ERROR_CHECK(esp_partition_erase_range(partition, write_offset, partition->size));
 ESP_LOGI(TAG, "Written data start");
   for(i=0;i<8192;i++)
   { 
    
    //ESP_LOGI(TAG, "Written data");
    // Write the data, starting from the beginning of the partition
    ESP_ERROR_CHECK(esp_partition_write(partition, write_offset, store_data, sizeof(store_data)));
    //ESP_LOGI(TAG, "Written data: %s", store_data);
    

    // Read back the data, checking that read data and written data match
    //ESP_ERROR_CHECK(esp_partition_read(partition, write_offset, read_data, sizeof(read_data)));
    // assert(memcmp(store_data, read_data, sizeof(read_data)) == 0);
   // ESP_LOGI(TAG, "Read data: %s", read_data);
   //printf( "test_offset = %0lx\n", test_offset);
   write_offset +=0x400;
    }
  

    ESP_LOGI(TAG, "Written data stop");
      printf( "write_offset = 0x%0lx \n", write_offset);
      printf( "write size  = %0ld Bytes \n ", write_offset);

    uint32_t read_offset = 0x0;
    ESP_LOGI(TAG, "read data start");
   for(i=0;i<8192;i++)
   {
    
    //ESP_LOGI(TAG, "Written data");
    // Write the data, starting from the beginning of the partition
    //ESP_ERROR_CHECK(esp_partition_write(partition, test_offset, store_data, sizeof(store_data)));
    //ESP_LOGI(TAG, "Written data: %s", store_data);
    
    // Read back the data, checking that read data and written data match
    ESP_ERROR_CHECK(esp_partition_read(partition, read_offset, read_data, sizeof(read_data)));
    // assert(memcmp(store_data, read_data, sizeof(read_data)) == 0);
   // ESP_LOGI(TAG, "Read data: %s", read_data);
   //printf( "test_offset = %0lx\n", test_offset);
   read_offset +=0x400;
    }

    ESP_LOGI(TAG, "read data stop");
    printf( "read_offset = 0x%0lx \n", read_offset);
    printf( "read size = %0ld Bytes\n", read_offset);
    
    // Erase the area where the data was written. Erase size shoud be a multiple of SPI_FLASH_SEC_SIZE
    // and also be SPI_FLASH_SEC_SIZE aligned

    // ESP_ERROR_CHECK(esp_partition_erase_range(partition, 0, SPI_FLASH_SEC_SIZE));

    // // Read back the data (should all now be 0xFF's)
    // memset(store_data, 0xFF, sizeof(read_data));
    // ESP_ERROR_CHECK(esp_partition_read(partition, 0, read_data, sizeof(read_data)));
    // assert(memcmp(store_data, read_data, sizeof(read_data)) == 0);

    // ESP_LOGI(TAG, "Erased data");

    // ESP_LOGI(TAG, "Example end");

}
