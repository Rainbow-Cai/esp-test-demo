/* Deep sleep wake up example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "soc/soc_caps.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_sleep.h"
#include "esp_log.h"
#include "driver/rtc_io.h"
#include "soc/rtc.h"

#include <sys/time.h>

#include "driver/gpio.h"

#define RTC_GPIO4_NUM GPIO_NUM_4
#define RTC_GPIO3_NUM GPIO_NUM_3
#define RTC_GPIO2_NUM GPIO_NUM_2

#define DEEP_SLEEP_TIME (10000000) // 10 S

void app_main(void)
{
    //   vTaskDelay(pdMS_TO_TICKS(10000000));
    // 配置 RTC_GPIO4 为输入
    gpio_config_t io_conf4 = {};
    // io_conf.intr_type = GPIO_PIN_INTR_DISABLE;
    io_conf4.mode = GPIO_MODE_INPUT;
    io_conf4.pin_bit_mask = 1ULL << RTC_GPIO4_NUM;
    io_conf4.pull_down_en = 1;
    io_conf4.pull_up_en = 0;
    gpio_config(&io_conf4);
    printf("GPIO4 INIT\n");

    gpio_config_t io_conf3 = {};
    // io_conf.intr_type = GPIO_PIN_INTR_DISABLE;
    io_conf3.mode = GPIO_MODE_INPUT;
    io_conf3.pin_bit_mask = 1ULL << RTC_GPIO3_NUM;
    io_conf3.pull_down_en = 1;
    io_conf3.pull_up_en = 0;
    gpio_config(&io_conf3);
    printf("GPIO3 INIT\n");

    gpio_config_t io_conf2 = {};
    // io_conf.intr_type = GPIO_PIN_INTR_DISABLE;
    io_conf2.mode = GPIO_MODE_INPUT;
    io_conf2.pin_bit_mask = 1ULL << RTC_GPIO2_NUM;
    // io_conf2.pull_down_en = 1;
    // io_conf2.pull_up_en = 0;
    gpio_config(&io_conf2);
    printf("GPIO2 INIT\n");

    // 设置唤醒源
    // esp_sleep_enable_ext0_wakeup(RTC_GPIO_NUM, 1); // 1 = 高电平唤醒

    // esp_sleep_enable_gpio_wakeup();
    // rtc_gpio_wakeup_enable(GPIO_NUM_4,0x5);

    esp_deep_sleep_enable_gpio_wakeup(BIT(GPIO_NUM_4), 1);

    printf("Wake up from GPIO4!\n");

    esp_deep_sleep_enable_gpio_wakeup(BIT(GPIO_NUM_3), 1);

    printf("Wake up from GPIO3!\n");

    esp_deep_sleep_enable_gpio_wakeup(BIT(GPIO_NUM_2), 1);

    printf("Wake up from GPIO2!\n");

    // 设置 Timer 唤醒源

    esp_sleep_enable_timer_wakeup(DEEP_SLEEP_TIME); // 10 S
    printf("Wake up from Timer!\n");

    vTaskDelay(pdMS_TO_TICKS(5000));
    ESP_LOGI("main", "Entering deep sleep...");
   
    // 进入 deep sleep
    esp_deep_sleep_start();

    vTaskDelay(pdMS_TO_TICKS(10000));
}
