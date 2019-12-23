/*
 * stepper.h
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */

#ifndef HAL_STEPPER_H_
#define HAL_STEPPER_H_


// STEPPER HH CTL1:P2.1, CTL2:P2.0, CTL3:P1.6, CTL4:P1.7
#define STPHH_1_PDIR  P2DIR
#define STPHH_1_POUT  P2OUT
#define STPHH_1_BIT   BIT1
#define STPHH_2_PDIR  P2DIR
#define STPHH_2_POUT  P2OUT
#define STPHH_2_BIT   BIT0
#define STPHH_3_PDIR  P1DIR
#define STPHH_3_POUT  P1OUT
#define STPHH_3_BIT   BIT6
#define STPHH_4_PDIR  P1DIR
#define STPHH_4_POUT  P1OUT
#define STPHH_4_BIT   BIT7

// STEPPER MM CTL1:P1.3, CTL2:P2.2, CTL3:P3.0, CTL4:P2.3
#define STPMM_1_PDIR  P1DIR
#define STPMM_1_POUT  P1OUT
#define STPMM_1_BIT   BIT3
#define STPMM_2_PDIR  P2DIR
#define STPMM_2_POUT  P2OUT
#define STPMM_2_BIT   BIT2
#define STPMM_3_PDIR  P3DIR
#define STPMM_3_POUT  P3OUT
#define STPMM_3_BIT   BIT0
#define STPMM_4_PDIR  P2DIR
#define STPMM_4_POUT  P2OUT
#define STPMM_4_BIT   BIT3

void setup_stepper();
void stepper_HH_move();
void stepper_HH_stop();
void stepper_MM_move();
void stepper_MM_stop();

#endif /* HAL_STEPPER_H_ */
