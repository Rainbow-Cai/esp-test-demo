#include <stdio.h>
#include "esp_system.h"
#include "esp_log.h"
#include <time.h>
#include <sys/time.h>
#include "esp_sleep.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "driver/gpio.h"
#include "driver/rtc_io.h"
#include "soc/rtc.h"

#define DEEP_SLEEP_TIME (50000000) // 3min
RTC_DATA_ATTR int bootCount = 0;

void app_main(void)
{

 //zero-initialize the config structure.
    // gpio_config_t io_conf = {};
    // //disable interrupt
    // io_conf.intr_type = GPIO_INTR_DISABLE;
    // //bit mask of the pins that you want to set,e.g.GPIO18/19
    // io_conf.pin_bit_mask = 1ULL<<GPIO_NUM_19;
    // //configure GPIO with the given settings
    // gpio_config(&io_conf);
  printf("wakeup Count: %d\n", bootCount);
  // user_sys_entry_sleep_mode();
  /* Wake up in 1000ms */
  ESP_LOGI("app", "deep_sleep testing\r\n");

  /* Get timestamp before entering sleep */
   //zero-initialize the config structure.
    
  gpio_set_direction(GPIO_NUM_18, GPIO_MODE_OUTPUT);
  gpio_pullup_en(GPIO_NUM_18);
  gpio_set_level(GPIO_NUM_18, 1);

  gpio_hold_en(GPIO_NUM_18); // HX711 POWER OFF
  gpio_deep_sleep_hold_en();

   //gpio_hold_en(GPIO_NUM_10);


  printf("Wake up!\n");
  
  esp_sleep_enable_timer_wakeup(DEEP_SLEEP_TIME); 
  
  // 增加重启次数计数器
  ++bootCount;

  printf("Entering deep sleep\n");

  esp_deep_sleep_start();

 // vTaskDelay(pdMS_TO_TICKS(1000));
}
