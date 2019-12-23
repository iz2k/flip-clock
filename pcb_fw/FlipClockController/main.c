#include <msp430.h> 
#include <stdint.h>
#include "hal/mcu.h"
#include "hal/ir-sensor.h"
#include "hal/sw-sensor.h"
#include "hal/stepper.h"
#include "hal/uart.h"

#define HH_DIVIDER  3
#define MM_DIVIDER  10

// Private routine prototypes
void decode_command();
void print_info();

// Shared variables
extern uint8_t fSystick;
extern uint8_t RxBuf[64];
extern uint8_t fCmd;
extern uint8_t fIRHH;
extern uint8_t fIRMM;

// Main varibales
uint8_t current_HH=1;
uint8_t current_MM=1;
uint8_t expected_HH=0;
uint8_t expected_MM=0;
uint8_t divcounter_HH=0;
uint8_t divcounter_MM=0;
uint8_t sync_HH_done=0;
uint8_t sync_MM_done=0;

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
    uint16_t nsteps_MM=0;

	setup_mcu();
	setup_ir();
	setup_sw();
	setup_stepper();
	setup_uart();
	setup_systick();

    unlock_GPIOs();


    enable_IRTX1();
    enable_IRTX2();

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
                        sync_HH_done = 1;
                        sync_delay_HH=0;
                    }
                }
                // Check SYNC MM
                if(get_sync_MM())
                {
                    sync_delay_MM = 1;
                }
                if(sync_delay_MM !=0)
                {
                    if(sync_delay_MM++ > cal_sdelay_MM)
                    {
                        current_MM = cal_MM;
                        sync_MM_done = 1;
                        sync_delay_MM=0;
                    }
                }
                // Check IRRX HH
                if (get_IR_HH())
                {
                    if (sync_HH_done) current_HH++;
                    if (current_HH>23) current_HH=0;
                    send_uart_string("H: ");
                    send_uart_int(current_HH);
                    send_uart_string(" (");
                    send_uart_int(nsteps_HH);
                    send_uart_string_nl(")");
                    nsteps_HH=0;
                }
                // Check IRRX MM
                if (get_IR_MM())
                {
                    if (sync_MM_done)current_MM++;
                    if (current_MM>59) current_MM=0;
                    send_uart_string("M: ");
                    send_uart_int(current_MM);
                    send_uart_string(" (");
                    send_uart_int(nsteps_MM);
                    send_uart_string_nl(")");
                    nsteps_MM=0;
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
                // Control MM
                if (current_MM != expected_MM)
                {
                    if(divcounter_MM++>=MM_DIVIDER){
                        stepper_MM_move();
                        nsteps_MM++;
                        divcounter_MM=0;
                    }
                }else{
                    stepper_MM_stop();
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
            case StatusFindSyncMM:
                // Check SYNC MM
                if(!get_sync_MM())
                {
                    if(divcounter_MM++>=MM_DIVIDER){
                        stepper_MM_move();
                        nsteps_MM++;
                        divcounter_MM=0;
                    }
                }else{
                    sync_delay_MM = 1;
                    status = StatusSyncDelayMM;
                }
                // Check IRRX HH
                if (get_IR_MM())
                {
                    send_uart_int_nl(nsteps_MM);
                    nsteps_MM=0;
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
                        status = StatusRun;
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
            case StatusSyncDelayMM:
                if(sync_delay_MM !=0)
                {
                    if(sync_delay_MM++ > cal_sdelay_MM)
                    {
                        stepper_MM_stop();
                        sync_delay_MM=0;
                        current_MM = cal_MM;
                        status = StatusRun;
                    }else{
                        stepper_MM_move();
                        nsteps_MM++;
                    }
                }
                // Check IRRX
                if (get_IR_MM())
                {
                    send_uart_int(nsteps_MM);
                    nsteps_MM=0;
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
    case 'h': // Set HOUR
    case 'H': // Set HOUR
        expected_HH = (RxBuf[1]-48)*10 + RxBuf[2]-48;
        break;
    case 'm': // Set MINUTES
    case 'M': // Set MINUTES
        expected_MM = (RxBuf[1]-48)*10 + RxBuf[2]-48;
        break;
    case 't': // Set Time HHMM
    case 'T': // Set Time HHMM
        expected_HH = (RxBuf[1]-48)*10 + RxBuf[2]-48;
        expected_MM = (RxBuf[3]-48)*10 + RxBuf[4]-48;
        break;
    case 's': // Find SYNC position
    case 'S': // Find SYNC position
        switch(RxBuf[1])
        {
        case 'h':
        case 'H':
            status = StatusFindSyncHH;
            break;
        case 'm':
        case 'M':
            status = StatusFindSyncMM;
            break;
        }
        break;
    case 'c': // CAL SYNC position values
    case 'C': // CAL SYNC position values
        switch(RxBuf[1])
        {
        case 'h':
        case 'H':
            SYSCFG0 = FRWPPW | DFWP;
            cal_HH = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            current_HH = cal_HH;
            expected_HH = cal_HH;
            break;
        case 'm':
        case 'M':
            SYSCFG0 = FRWPPW | DFWP;
            cal_MM = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            current_MM = cal_MM;
            expected_MM = cal_MM;
            break;
        }
        status = StatusRun;
        break;
    case 'd': // CAL SYNC DELAY value
    case 'D': // CAL SYNC DELAY value
        switch(RxBuf[1])
        {
        case 'h':
        case 'H':
            SYSCFG0 = FRWPPW | DFWP;
            cal_sdelay_HH = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            break;
        case 'm':
        case 'M':
            SYSCFG0 = FRWPPW | DFWP;
            cal_sdelay_MM = (RxBuf[2]-48)*10 + RxBuf[3]-48;
            SYSCFG0 = FRWPPW | PFWP | DFWP;
            break;
        }
        status = StatusRun;
        break;
        case 'i': // SHOW INFO
        case 'I': // SHOW INFO
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
    send_uart_string(" Current HH: ");
    send_uart_int_nl(current_HH);
    send_uart_string(" Current MM: ");
    send_uart_int_nl(current_MM);
    send_uart_string_nl(" Sync HH:");
    send_uart_string("  Cal: ");
    send_uart_int(cal_HH);
    send_uart_string("  Delay: ");
    send_uart_int_nl(cal_sdelay_HH);
    send_uart_string_nl(" Sync MM:");
    send_uart_string("  Cal: ");
    send_uart_int(cal_MM);
    send_uart_string("  Delay: ");
    send_uart_int_nl(cal_sdelay_MM);
}
