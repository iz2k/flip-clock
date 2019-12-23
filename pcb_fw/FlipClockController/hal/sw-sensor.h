/*
 * sw-sensor.h
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */

#ifndef HAL_SW_SENSOR_H_
#define HAL_SW_SENSOR_H_

// SYNC SW 1 (P3.1)
#define SW1_PDIR  P3DIR
#define SW1_POUT  P3OUT
#define SW1_PIN   P3IN
#define SW1_PREN  P3REN
#define SW1_BIT   BIT1

// SYNC SW 2 (P3.2)
#define SW2_PDIR  P3DIR
#define SW2_POUT  P3OUT
#define SW2_PIN   P3IN
#define SW2_PREN  P3REN
#define SW2_BIT   BIT2

void setup_sw();
uint8_t get_sync_HH();
uint8_t get_sync_MM();


#endif /* HAL_SW_SENSOR_H_ */
