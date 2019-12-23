/*
 * ir-sensor.c
 *
 *  Created on: 19 nov. 2019
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <stdint.h>
#include "ir-sensor.h"

// Shared flags
uint8_t fIRHH=0;
uint8_t fIRMM=0;

void setup_ir()
{
    // Setup TX control signals
    IRTX1_PDIR |= IRTX1_BIT;
    IRTX1_POUT &= ~IRTX1_BIT;

    IRTX2_PDIR |= IRTX2_BIT;
    IRTX2_POUT &= ~IRTX2_BIT;

    // Setup RX input signals
    IRRX1_PDIR &= ~IRRX1_BIT;   // Input
    IRRX1_POUT &= ~IRRX1_BIT;   // Tie pull down
    IRRX1_PREN |= IRRX1_BIT;    // Enable pull
    //IRRX1_PIES |= IRRX1_BIT;    // Select interrupt edge
    //IRRX1_PIFG &= ~IRRX1_BIT;   // Clear interrupt flag
    //IRRX1_PIE |= IRRX1_BIT;     // Enable interrupt

    IRRX2_PDIR &= ~IRRX2_BIT;   // Input
    IRRX2_POUT &= ~IRRX2_BIT;   // Tie pull down
    IRRX2_PREN |= IRRX2_BIT;    // Enable pull
    //IRRX2_PIES |= IRRX2_BIT;    // Select interrupt edge
    //IRRX2_PIFG &= ~IRRX2_BIT;   // Clear interrupt flag
    //IRRX2_PIE |= IRRX2_BIT;     // Enable interrupt

}

void enable_IRTX1()
{
    IRTX1_POUT |= IRTX1_BIT;
}

void disable_IRTX1()
{
    IRTX1_POUT &= ~IRTX1_BIT;
}

void enable_IRTX2()
{
    IRTX2_POUT |= IRTX2_BIT;
}

void disable_IRTX2()
{
    IRTX2_POUT &= ~IRTX2_BIT;
}

uint16_t debounce_IR_HH=0;
uint8_t get_IR_HH()
{
    if(debounce_IR_HH==0){
        if (!(IRRX2_PIN & IRRX2_BIT))
        {
            debounce_IR_HH = 400;
            return 1;
        }
    }else{
        debounce_IR_HH--;
    }
    return 0;
}

uint16_t debounce_IR_MM=0;
uint8_t get_IR_MM()
{
    if(debounce_IR_MM==0){
        if (!(IRRX1_PIN & IRRX1_BIT))
        {
            debounce_IR_MM = 400;
            return 1;
        }
    }else{
        debounce_IR_MM--;
    }
    return 0;
}

#pragma vector = PORT2_VECTOR
__interrupt void Port_2(void)
{
    switch(P2IFG){
    case IRRX1_BIT:
        // Clear interrupt flag
        P2IFG &= ~IRRX1_BIT;
        // Assert flag
        fIRHH=1;
        break;
    case IRRX2_BIT:
        // Clear interrupt flag
        P2IFG &= ~IRRX2_BIT;
        // Assert flag
        fIRMM=1;
        break;
    default:
        // Clear interrupt flag
        P2IFG = 0;
    }
}
