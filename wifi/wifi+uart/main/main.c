#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_spiffs.h"
#include "esp_vfs.h"
#include "lwip/dns.h"
#include "lwip/err.h"
#include "lwip/inet.h"
#include "lwip/ip4_addr.h"
#include "lwip/netdb.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include <ctype.h>
#include <unistd.h>
#include "esp32/rom/spi_flash.h"
#include "nvs.h"
#include "nvs_flash.h"
#include "soc/rtc_wdt.h"
#include <esp32/rom/rtc.h>
#include <string.h>
#include <sys/param.h>
#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "esp_wifi.h"
#include "driver/gpio.h"
#include "mdns.h"
#include <stdio.h>
#include <string.h>

#include "main.h"



SemaphoreHandle_t uartMutex;
static EventGroupHandle_t s_wifi_event_group;
wifi_config_t apConfig;
wifi_config_t staConfig;

uint8_t 	mac[6];

void app_main(void)
{
    uartMutex = xSemaphoreCreateMutex(); 
    esp_efuse_mac_get_default(mac);
    //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    initUSART();
    wifiInit(WIFI_MODE_APSTA); // Uart works OK
    // wifiInit(WIFI_MODE_AP); // Uart works OK
    // wifiInit(WIFI_MODE_STA); // Uart works unstable
}

void netif_event_handler(void *arg, esp_event_base_t event_base,
                         int32_t event_id, void *event_data)
{
    if (event_base == WIFI_EVENT) {
        switch (event_id) {
        case WIFI_EVENT_AP_START:
            ESP_LOGI(DBG_TAG, COL_WIFI "START AP");
            break;
        case WIFI_EVENT_STA_START:
            ESP_LOGI(DBG_TAG, COL_WIFI "START CLI");
            esp_wifi_connect();
            break;
        case WIFI_EVENT_STA_DISCONNECTED:
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: connect to the AP fail", event_base);
            esp_wifi_connect();
            break;
        case WIFI_EVENT_AP_STACONNECTED:
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: WIFI_EVENT_AP_STACONNECTED", event_base);
            wifi_event_ap_staconnected_t *event = (wifi_event_ap_staconnected_t *)event_data;
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: station " MACSTR " join, AID=%d", event_base, MAC2STR(event->mac), event->aid);
            break;
        default:
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: UNKNOWN EVENT ID: %d", event_base, event_id);
            break;
        }
    } else if (event_base == IP_EVENT) {
        switch (event_id) {
        case IP_EVENT_STA_GOT_IP:
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: IP_EVENT_STA_GOT_IP", event_base);
            ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
            ESP_LOGI(DBG_TAG, "got ip:" IPSTR, IP2STR(&event->ip_info.ip));
            break;
        default:
            ESP_LOGI(DBG_TAG, COL_WIFI "%s: UNKNOWN EVENT ID: %d", event_base, event_id);
            break;
        }
    } else {
        ESP_LOGI(DBG_TAG, COL_WIFI "%s", event_base);
    }
}


void wifiInit(wifi_mode_t mode)
{
    
    esp_netif_t *esp_netif_sta;
    esp_netif_t *esp_netif_ap;


    s_wifi_event_group = xEventGroupCreate();

    // TCP/IP
    ESP_ERROR_CHECK(esp_netif_init()); // tcpip_adapter_init();
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_sta = esp_netif_create_default_wifi_sta();
    esp_netif_ap = esp_netif_create_default_wifi_ap();
    // set_hostname();
    ESP_ERROR_CHECK(esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &netif_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &netif_event_handler, NULL));

    // WiFi
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
    // ESP_ERROR_CHECK(esp_wifi_set_ps(WIFI_PS_NONE)); // Disable WiFi powersave
    ESP_ERROR_CHECK(esp_wifi_set_ps(WIFI_PS_MAX_MODEM)); // Enable WiFi powersave
    
    // Set user STA config
    sprintf((char *)staConfig.sta.ssid, "rainbow_2.4G");
    sprintf((char *)staConfig.sta.password, "espressif");

    // Set AP config
    sprintf((char *)apConfig.ap.ssid, "%s %s_%02X%02X%02X", "test", "test", PARTIAL_MAC);
    sprintf((char *)apConfig.ap.password, "%s%02X%02X%02X", "test", PARTIAL_MAC);
    apConfig.ap.max_connection = 5;
    apConfig.ap.authmode = WIFI_AUTH_WPA2_PSK;

    // Apply config and start WiFi
    ESP_LOGI(DBG_TAG, COL_WIFI "STA: %s; STA_PWD: %s; AP: %s; AP_PWD: %s", staConfig.sta.ssid, staConfig.sta.password, apConfig.ap.ssid, apConfig.ap.password);
    ESP_ERROR_CHECK(esp_wifi_set_mode(mode));
    switch(mode){
        case WIFI_MODE_APSTA:
            ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &staConfig));
        case WIFI_MODE_AP:
            ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_AP, &apConfig));
            break;
        case WIFI_MODE_STA:
            ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &staConfig));
            break;
        default:
            return;
    }

    ESP_ERROR_CHECK(esp_wifi_start());

    // esp_netif_dhcpc_start(esp_netif_sta); // Start DHCP client

    
}



void initUSART(void)
{

    err_t deinitErr, initErr;

    xSemaphoreTake(uartMutex, portMAX_DELAY);
    deinitErr = uart_driver_delete(STM32_UART_NUM);

    //init USART to communicate with stm32
    const uart_config_t uart_config = {
        // .baud_rate = 115200,
        .baud_rate = USART_SPEED,
        //.baud_rate = 941176,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        //.parity = UART_PARITY_EVEN,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE};
    uart_param_config(STM32_UART_NUM, &uart_config);
    uart_set_pin(STM32_UART_NUM, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    // We won't use a buffer for sending data.
    initErr = uart_driver_install(STM32_UART_NUM, RX_BUF_SIZE * 2, RX_BUF_SIZE * 2, 0, NULL, 0);

    xSemaphoreGive(uartMutex);
    ESP_LOGI(DBG_TAG, "USER deinit=%d init=%d", deinitErr, initErr);
    xTaskCreate(&uartRXTask, "uartRXTask", 4096, NULL, 5, NULL);
}

void uartTX(void *data, size_t dataLen){
    xSemaphoreTake(uartMutex, portMAX_DELAY);
    uart_write_bytes(STM32_UART_NUM, (char *)data, dataLen + 3);
    //free(data);
    xSemaphoreGive(uartMutex);
}

void uartRXTask(){
    uint8_t *data = (uint8_t *)calloc(1, RX_BUF_SIZE + 1);
    while (1) {
        //serve stm32 requests
        const int rxBytes = uart_read_bytes(STM32_UART_NUM, data, RX_BUF_SIZE, 10);
        if (rxBytes){
            data[rxBytes] = 0;
            ESP_LOGI(DBG_TAG, "Read %d bytes 0x%x 0x%x 0x%x 0x%x",
             						rxBytes, data[0], data[1], data[2], data[3]);
            
           uartTX(data,strlen((const char *)data) +1);

            ESP_LOG_BUFFER_HEXDUMP("RX", data, rxBytes, ESP_LOG_INFO);
            //uart_write_bytes(STM32_UART_NUM, (char *)data, strlen((const char *)data) +1);

        }
    }
    free(data);
}

