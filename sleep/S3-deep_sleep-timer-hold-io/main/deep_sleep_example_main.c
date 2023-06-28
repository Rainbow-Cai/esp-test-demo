#include <stdio.h>
#include "esp_system.h"
#include "esp_log.h"
#include <time.h>
#include <sys/time.h>
#include "esp_sleep.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "driver/rtc_io.h"
#include "soc/rtc.h"

#define DEEP_SLEEP_TIME (10000000) // 3min
RTC_DATA_ATTR int bootCount = 0;

void app_main(void)
{

  printf("wakeup Count: %d\n", bootCount);
  // user_sys_entry_sleep_mode();
  /* Wake up in 1000ms */
  ESP_LOGI("app", "deep_sleep testing\r\n");

  /* Get timestamp before entering sleep */
  rtc_gpio_init(GPIO_NUM_21);
  rtc_gpio_set_direction(GPIO_NUM_21, RTC_GPIO_MODE_INPUT_OUTPUT);
  rtc_gpio_pullup_en(GPIO_NUM_21);
  rtc_gpio_set_level(GPIO_NUM_21, 1);

    rtc_gpio_hold_en(GPIO_NUM_21); // HX711 POWER OFF
  gpio_deep_sleep_hold_en();
    rtc_gpio_isolate(GPIO_NUM_21);



  printf("Wake up!\n");
  esp_sleep_enable_timer_wakeup(DEEP_SLEEP_TIME); 
  
  // 增加重启次数计数器
  ++bootCount;
rtc_gpio_get_level(GPIO_NUM_21);
  printf("level is %d\n",rtc_gpio_init);
  printf("Entering deep sleep\n");

  esp_deep_sleep_start();

  vTaskDelay(pdMS_TO_TICKS(1000));
}
