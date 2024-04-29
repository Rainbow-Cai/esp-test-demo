//
// Copyright (c) 2023, Breville Pty Ltd. All rights reserved.
//

#include "freertos/FreeRTOS.h"

extern void esp_vApplicationTickHook();
void IRAM_ATTR vApplicationTickHook()
{
    esp_vApplicationTickHook();
}

extern void esp_vApplicationIdleHook();
void vApplicationIdleHook()
{
    esp_vApplicationIdleHook();
}

void vApplicationDaemonTaskStartupHook( void )
{
}

void vPortCleanUpTCB(void* tcb){
    return;
}