/*
 * stepper.c
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */
#include <msp430.h>
#include <stdint.h>
#include "stepper.h"

const int8_t stepmtx [8][4] =
{
  {1, 0, 0, 0},
  {1, 1, 0, 0},
  {0, 1, 0, 0},
  {0, 1, 1, 0},
  {0, 0, 1, 0},
  {0, 0, 1, 1},
  {0, 0, 0, 1},
  {1, 0, 0, 1}
};

int8_t iStpHH=0;

void setup_stepper()
{
    // Set stepper control pins as output
    STPHH_1_PDIR |= STPHH_1_BIT;
    STPHH_2_PDIR |= STPHH_2_BIT;
    STPHH_3_PDIR |= STPHH_3_BIT;
    STPHH_4_PDIR |= STPHH_4_BIT;

    STPMM_1_PDIR |= STPMM_1_BIT;
    STPMM_2_PDIR |= STPMM_2_BIT;
    STPMM_3_PDIR |= STPMM_3_BIT;
    STPMM_4_PDIR |= STPMM_4_BIT;
}

void stepper_HH_move()
{
    stepmtx[iStpHH][0] ? (STPHH_1_POUT |= STPHH_1_BIT) : (STPHH_1_POUT &= ~ STPHH_1_BIT);
    stepmtx[iStpHH][1] ? (STPHH_2_POUT |= STPHH_2_BIT) : (STPHH_2_POUT &= ~ STPHH_2_BIT);
    stepmtx[iStpHH][2] ? (STPHH_3_POUT |= STPHH_3_BIT) : (STPHH_3_POUT &= ~ STPHH_3_BIT);
    stepmtx[iStpHH][3] ? (STPHH_4_POUT |= STPHH_4_BIT) : (STPHH_4_POUT &= ~ STPHH_4_BIT);
    if(++iStpHH>7)iStpHH=0;
}

void stepper_HH_stop()
{
    // Set signaling to 0
    STPHH_1_POUT &= ~ STPHH_1_BIT;
    STPHH_2_POUT &= ~ STPHH_2_BIT;
    STPHH_3_POUT &= ~ STPHH_3_BIT;
    STPHH_4_POUT &= ~ STPHH_4_BIT;
}
