//
// Copyright (c) 2023, Breville Pty Ltd. All rights reserved.
//


#include <string.h>

// FreeRTOS includes
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_psram.h"
#include "freertos/idf_additions.h"
#include "esp32/himem.h"

// ESP-IDF includes
#include "esp_netif.h"
#include "driver/gpio.h"

// Defines
#define APP_VERSION_MAJOR 99
#define APP_VERSION_MINOR 99
#define APP_VERSION_BUILD 104

#define TEST_TASK_PRIORITY tskIDLE_PRIORITY + 6
#define TEST_TASK_STACK_SIZE (1024 * 60)
#define TEST_TASK_NAME "Test Task"

// Constants
static const TickType_t TASK_PERIOD = 10 / portTICK_PERIOD_MS;  // 10ms

// Data
static TaskHandle_t ssTestTaskHandle = {0};
static QueueHandle_t ssQueue;

static void testTaskFunction(void* pvParameters)
{
    TickType_t intervalStartTime = xTaskGetTickCount();

     printf("333333333333333333333333\n");

    while(true)
    {
        // Check if there's a new message in the queue
        uint32_t rxMessage;
        if(xQueueReceive(ssQueue, &rxMessage, 0))
        {
            // Do something
        }
 printf("4444444444444444444\n");
        vTaskDelayUntil(&intervalStartTime, TASK_PERIOD);

         printf("555555555555555555\n");
    }
}

BaseType_t TestTask_Start(void)
{    
    // Create a queue to hold queueMessage_t.
    ssQueue = xQueueCreateWithCaps(10, 4, MALLOC_CAP_SPIRAM);
    printf("11111111111111111111\n");
    if(ssQueue == 0)
    {
        // Failed to create a queue.
        return 0;
    }
 printf("22222222222222222222222222\n");
    // Create recipe cook task
  

 // char * test = heap_caps_malloc(TEST_TASK_STACK_SIZE, MALLOC_CAP_SPIRAM);

 //  memset(test, 0x66, 1024 * 60);
return xTaskCreateWithCaps(testTaskFunction, TEST_TASK_NAME, TEST_TASK_STACK_SIZE, NULL, TEST_TASK_PRIORITY, &ssTestTaskHandle, MALLOC_CAP_SPIRAM);

}

int app_main(void) 
{
      size_t memfree= (int)  esp_himem_get_free_size();
      printf("Start esp_spiram_get_size=%d\n",(int) esp_psram_get_size());

    printf("Start free_heap_size=%d\n", (int) esp_get_free_heap_size());
    printf("Start esp_get_free_internal_heap_size=%d\n",(int) esp_get_free_internal_heap_size());
printf("Start esp_himem_get_free_size=%d\n",(int) memfree);

    printf("\n Starting app_main %d.%d.%d\n", APP_VERSION_MAJOR, APP_VERSION_MINOR, APP_VERSION_BUILD);

    TestTask_Start();
  
  
      printf("esp_spiram_get_size=%d\n",(int) esp_psram_get_size());

    printf("free_heap_size=%d\n", (int) esp_get_free_heap_size());

printf("esp_get_free_internal_heap_size=%d\n",(int) esp_get_free_internal_heap_size());
printf("esp_himem_get_free_size=%d\n",(int) memfree);



    return 0;
}
