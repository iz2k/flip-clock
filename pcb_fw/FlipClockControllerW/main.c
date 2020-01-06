#include <msp430.h> 
#include <stdint.h>
#include "hal/mcu.h"
#include "hal/ir-sensor.h"
#include "hal/sw-sensor.h"
#include "hal/stepper.h"
#include "hal/uart.h"

#define HH_DIVIDER  3

// Private routine prototypes
void decode_command();
void print_info();

// Shared variables
extern uint8_t fSystick;
extern uint8_t RxBuf[64];
extern uint8_t fCmd;

// Main varibales
uint8_t current_HH=1;
uint8_t expected_HH=0;
uint8_t divcounter_HH=0;
uint8_t sync_HH_done=0;

#pragma PERSISTENT(cal_HH)
uint8_t cal_HH=0;
#pragma PERSISTENT(cal_MM)
uint8_t cal_MM=0;

uint8_t sync_delay_HH=0;
uint8_t sync_delay_MM=0;
#pragma PERSISTENT(cal_sdelay_HH)
uint8_t cal_sdelay_HH=00;
#pragma PERSISTENT(cal_sdelay_MM)
uint8_t cal_sdelay_MM=0;


typedef enum
{
    StatusStop,
    StatusRun,
    StatusFindSyncHH,
    StatusSyncDelayHH,
    StatusFindSyncMM,
    StatusSyncDelayMM,
} Status_t;

Status_t status=StatusRun;

/**
 * main.c
 */
void main(void)
{
    uint16_t nsteps_HH=0;

	setup_mcu();
	setup_ir();
	setup_sw();
	setup_stepper();
	setup_uart();
	setup_systick();

    unlock_GPIOs();

    enable_IRTX1();
    enable_IRTX2();

    stepper_HH_stop();

    __bis_SR_register(GIE);

    while(1)
    {
        if (fSystick)
        {
            // Deassert flag
            fSystick=0;
            switch(status)
            {
            case StatusRun:
                // Check SYNC HH
                if(get_sync_HH())
                {
                    sync_delay_HH = 1;
                }
                if(sync_delay_HH !=0)
                {
                    if(sync_delay_HH++ > cal_sdelay_HH)
                    {
                        current_HH = cal_HH;
                        sync_HH_done=1;
                        sync_delay_HH=0;
                    }
                }
                // Check IRRX HH
                if (get_IR_HH())
                {
                    if (sync_HH_done) current_HH++;
                    if (current_HH>23) current_HH=0;
                    send_uart_string("W: ");
                    send_uart_int(current_HH);
                    send_uart_string(" (");
                    send_uart_int(nsteps_HH);
                    send_uart_string_nl(")");
                    nsteps_HH=0;
                }
                // Control HH
                if (current_HH != expected_HH)
                {
                    if(divcounter_HH++>=HH_DIVIDER){
                        stepper_HH_move();
                        nsteps_HH++;
                        divcounter_HH=0;
                    }
                }else{
                    stepper_HH_stop();
                }
                break;
            case StatusFindSyncHH:

                // Check SYNC HH
                if(!get_sync_HH())
                {
                    if(divcounter_HH++>=HH_DIVIDER){
                        stepper_HH_move();
                        nsteps_HH++;
                        divcounter_HH=0;
                    }
                }else{
                    sync_delay_HH = 1;
                    status = StatusSyncDelayHH;
                }
                // Check IRRX HH
                if (get_IR_HH())
                {
                    send_uart_int_nl(nsteps_HH);
                    nsteps_HH=0;
                }
                break;
            case StatusSyncDelayHH:
                if(sync_delay_HH !=0)
                {
                    if(sync_delay_HH++ > cal_sdelay_HH)
                    {
                        stepper_HH_stop();
                        sync_delay_HH=0;
                        current_HH = cal_HH;
                        status = StatusStop;
                    }else{
                        stepper_HH_move();
                        nsteps_HH++;
                    }
                }
                // Check IRRX
                if (get_IR_HH())
                {
                    send_uart_int(nsteps_HH);
                    nsteps_HH=0;
                }
                break;
            }

        }

        if (fCmd)
        {
            // Deassert flag
            fCmd=0;
            // Decode command
            decode_command();
        }


    }
}

void decode_command()
{
    switch(RxBuf[0])
    {
    case 'w': // Set HOUR
    case 'W': // Set HOUR
        expected_HH = (RxBuf[1]-48)*10 + RxBuf[2]-48;
        break;
    case 's': // Find SYNC position
    case 'S': // Find SYNC position
        switch(RxBuf[1])
        {
        case 'w':
        case 'W':
            status = StatusFindSyncHH;
            break;
        }
        break;
    case 'c': // CAL SYNC position values
    case 'C': // CAL SYNC position values
        switch(RxBuf[1])
        {
        case 'w':
        case 'W':
            SYSCFG0 = FRWPPW | DFWP;
            cal_HH = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            current_HH = cal_HH;
            expected_HH = cal_HH;
            break;
        }
        status = StatusRun;
        break;
    case 'd': // CAL SYNC DELAY value
    case 'D': // CAL SYNC DELAY value
        switch(RxBuf[1])
        {
        case 'w':
        case 'W':
            SYSCFG0 = FRWPPW | DFWP;
            cal_sdelay_HH = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            break;
        }
        status = StatusRun;
        break;
        case 'y': // SHOW INFO
        case 'Y': // SHOW INFO
            print_info();
            break;
        case 'x': // STOP
        case 'X': // STOP
            status = StatusStop;
            break;
        case 'r': // STOP
        case 'R': // STOP
            status = StatusRun;
            break;
    }

}

void print_info()
{
    send_uart_string_nl("FlipClockController");
    send_uart_string_nl("-------------------");
    send_uart_string(" Current WW: ");
    send_uart_int_nl(current_HH);
    send_uart_string_nl(" Sync WW:");
    send_uart_string("  Cal: ");
    send_uart_int(cal_HH);
    send_uart_string("  Delay: ");
    send_uart_int_nl(cal_sdelay_HH);
}
