#ifndef _MAIN_H_
#define _MAIN_H_

#include "driver/uart.h"

#define DBG_TAG "wifi-uart-test"


#define PARTIAL_MAC			mac[3], mac[4], mac[5]

#define USART_SPEED			941176
#define TXD_PIN (GPIO_NUM_19)
#define RXD_PIN (GPIO_NUM_22)
#define STM32_UART_NUM UART_NUM_1
#define RX_BUF_SIZE 500

#define COL_CYAN 				"\033[36;1m"
#define COL_WIFI			COL_CYAN

void wifiInit(wifi_mode_t mode);
void initUSART();
void uartRXTask();
void uartTX(void *data, size_t dataLen);

#endif