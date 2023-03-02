/*
 * SPDX-FileCopyrightText: 2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "touch_proximity_plus.h"
#include "buzzer.h"
#include "soc/gpio_periph.h"
#include "hal/gpio_types.h"
#include "driver/gpio.h"

const char *TAG = "main";
#define IO_BUZZER_CTRL 36

void example_proxi_callback(uint32_t channel, proxi_evt_t event, void *cb_arg)
{
    switch (event) {
    case PROXI_EVT_ACTIVE:
        buzzer_set_voice(1);
        ESP_LOGI(TAG, "CH%u, active!", channel);
          gpio_set_level(GPIO_NUM_35, 1);
        break;
    case PROXI_EVT_INACTIVE:
        buzzer_set_voice(0);
        ESP_LOGI(TAG, "CH%u, inactive!", channel);
          gpio_set_level(GPIO_NUM_35, 0);
        break;
    default:
        break;
    }
}

void led_init(void)

{
    gpio_config_t io_conf = {};
    // set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    // bit mask of the pins that you want to set,e.g.GPIO18/19
    io_conf.pin_bit_mask = ((1ULL << GPIO_NUM_33) | (1ULL << GPIO_NUM_34) | (1ULL << GPIO_NUM_35));
    io_conf.pull_down_en = 1;
    // disable pull-up mode
    io_conf.pull_up_en = 0;
    // disable pull-down mode

    // configure GPIO with the given settings
    gpio_config(&io_conf);

    //  gpio_init(GPIO_NUM_45);

    gpio_set_level(GPIO_NUM_33, 0);
    gpio_set_level(GPIO_NUM_34, 0);
    gpio_set_level(GPIO_NUM_35, 0);

    // zero-initialize the config structure.
}


void app_main(void)
{

      led_init();
    buzzer_driver_install(IO_BUZZER_CTRL);
    buzzer_set_voice(0);
    proxi_config_t config = (proxi_config_t)DEFAULTS_PROX_CONFIGS();
    config.channel_num = 1;
    config.response_ms = 50;
    config.channel_list[0] = TOUCH_PAD_NUM8;
    config.threshold_p[0] = 0.004;
    config.threshold_n[0] = 0.004;
    config.noise_p = 0.001;
    config.debounce_p = 1;
    touch_proximity_sense_start(&config, &example_proxi_callback, NULL);
    while (1) {
        vTaskDelay(40 / portTICK_PERIOD_MS);
        // gpio_set_level(GPIO_NUM_35, 1);
    }
    //just for example, never comes here
    touch_proximity_sense_stop();
   //  gpio_set_level(GPIO_NUM_35, 1);
}
