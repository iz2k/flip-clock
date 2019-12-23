/*
 * sw-sensor.c
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <stdint.h>
#include "sw-sensor.h"

void setup_sw()
{
    // Setup SYNC switch input signals
    SW1_PDIR &= ~SW1_BIT;   // Input
    SW1_POUT &= ~SW1_BIT;   // Tie pull down
    SW1_PREN |= SW1_BIT;    // Enable pull

    SW2_PDIR &= ~SW2_BIT;   // Input
    SW2_POUT &= ~SW2_BIT;   // Tie pull down
    SW2_PREN |= SW2_BIT;    // Enable pull
}

uint8_t previous_value_HH=0;
uint8_t get_sync_HH()
{
    if(previous_value_HH!=0){
        if (!(SW2_PIN & SW2_BIT))
        {
            previous_value_HH=0;
            return 1;
        }
    }else{
        previous_value_HH=SW2_PIN & SW2_BIT;
    }
    return 0;
}

uint8_t previous_value_MM=0;
uint8_t get_sync_MM()
{
    if(previous_value_MM!=0){
        if (!(SW1_PIN & SW1_BIT))
        {
            previous_value_MM=0;
            return 1;
        }
    }else{
        previous_value_MM=SW1_PIN & SW1_BIT;
    }
    return 0;
}

