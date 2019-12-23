/*
 * uart.c
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <stdint.h>
#include <stdio.h>
#include "uart.h"

volatile uint8_t RxBuf[64];
volatile uint8_t TxBuf[64];
volatile uint8_t iRx=0;
volatile uint8_t iTx=0;
volatile uint8_t fCmd=0;

void setup_uart()
{
    // Configure UART pins
    P2SEL0 |= BIT5 | BIT6;                    // set 2-UART pin as second function

    // Configure UART
    UCA1CTLW0 |= UCSWRST;                     // Put eUSCI in reset
    UCA1CTLW0 |= UCSSEL__SMCLK;
    // Baud Rate calculation
    UCA1BR0 = 4;                              // 1000000/115200 = 8.68
    UCA1MCTLW = 0x5500 | 0x0050 | UCOS16;                       // 1000000/115200 - INT(1000000/115200)=0.68
                                              // UCBRSx value = 0xD6 (See UG)
    UCA1BR1 = 0;
    UCA1CTLW0 &= ~UCSWRST;                    // Initialize eUSCI
    UCA1IE |= UCRXIE;                         // Enable USCI_A0 RX interrupt
}

void send_uart_int_nl(int value)
{
    // Print num
    send_uart_int(value);
    // Print newline
    while(!(UCA1IFG & UCTXIFG));
    UCA1TXBUF=10;
    while(!(UCA1IFG & UCTXIFG));
    UCA1TXBUF=13;
}

void send_uart_int(int value)
{
    int i=0;
    char num[16];
    sprintf(num, "%d", value);
    while(num[i]!=0)
    {
        while(!(UCA1IFG & UCTXIFG));
        UCA1TXBUF=num[i];
        i++;
    }
}

void send_uart_string_nl(char *string)
{
    // Print string
    send_uart_string(string);
    // Print newline
    while(!(UCA1IFG & UCTXIFG));
    UCA1TXBUF=10;
    while(!(UCA1IFG & UCTXIFG));
    UCA1TXBUF=13;
}

void send_uart_string(char *string)
{
    int i=0;
    while(string[i]!=0)
    {
        while(!(UCA1IFG & UCTXIFG));
        UCA1TXBUF=string[i];
        i++;
    }
}


#pragma vector=USCI_A1_VECTOR
__interrupt void USCI_A1_ISR(void)
{
    uint8_t newbyte;
    switch(__even_in_range(UCA1IV,USCI_UART_UCTXCPTIFG))
    {
        case USCI_NONE: break;
        case USCI_UART_UCRXIFG:
            // Get byte
            newbyte=UCA1RXBUF;
            // ECHO byte
            while(!(UCA1IFG & UCTXIFG));
            UCA1TXBUF=newbyte;
            // Detect End of Command (13)
            if (newbyte==13)
            {
                iRx=0;
                fCmd=1;
                //while(!(UCA1IFG & UCTXIFG));
                //UCA1TXBUF=10;
                //while(!(UCA1IFG & UCTXIFG));
                //UCA1TXBUF=13;
            }else{
                RxBuf[iRx++]=newbyte;
            }
            break;
        case USCI_UART_UCTXIFG: break;
        case USCI_UART_UCSTTIFG: break;
        case USCI_UART_UCTXCPTIFG: break;
    }
}


