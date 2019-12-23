/*
 * ir-sensor.h
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */

#ifndef HAL_IR_SENSOR_H_
#define HAL_IR_SENSOR_H_

// HW definition

// IR TX 1 (P1.2)
#define IRTX1_PDIR  P1DIR
#define IRTX1_POUT  P1OUT
#define IRTX1_BIT   BIT2

// IR TX 2 (P1.0)
#define IRTX2_PDIR  P1DIR
#define IRTX2_POUT  P1OUT
#define IRTX2_BIT   BIT0

// IR RX 1 (P2.4)
#define IRRX1_PDIR  P2DIR
#define IRRX1_POUT  P2OUT
#define IRRX1_PIN   P2IN
#define IRRX1_PREN  P2REN
#define IRRX1_PIES  P2IES
#define IRRX1_PIFG  P2IFG
#define IRRX1_PIE   P2IE
#define IRRX1_BIT   BIT4

// IR RX 2 (P2.7)
#define IRRX2_PDIR  P2DIR
#define IRRX2_POUT  P2OUT
#define IRRX2_PIN   P2IN
#define IRRX2_PREN  P2REN
#define IRRX2_PIES  P2IES
#define IRRX2_PIFG  P2IFG
#define IRRX2_PIE   P2IE
#define IRRX2_BIT   BIT7

void setup_ir();
void enable_IRTX1();
void disable_IRTX1();
void enable_IRTX2();
void disable_IRTX2();

uint8_t get_IR_HH();
uint8_t get_IR_MM();


#endif /* HAL_IR_SENSOR_H_ */
