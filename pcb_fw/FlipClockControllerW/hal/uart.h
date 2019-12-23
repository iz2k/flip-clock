/*
 * uart.h
 *
 *  Created on: 18 nov. 2019
 *      Author: IbonZalbide
 */

#ifndef HAL_UART_H_
#define HAL_UART_H_


void setup_uart();
void send_uart_int_nl(int value);
void send_uart_int(int value);
void send_uart_string_nl(char *string);
void send_uart_string(char *string);


#endif /* HAL_UART_H_ */
