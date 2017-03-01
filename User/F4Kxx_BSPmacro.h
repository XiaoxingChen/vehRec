#ifndef F4KXX_BSPMACRO_H
#define F4KXX_BSPMACRO_H

#define F4KXX_CAN1_IOGROUP		(CCanRouter::GROUP_A11)
#define F4KXX_CAN2_IOGROUP		(CCanRouter::GROUP_B12)

/* Macros for board version */
//#define RUN_FOR_SPARK_BOARD
//#define RUN_FOR_FW_BOARD
#define RUN_FOR_INT_BOARD

/* for Spark Board */
#ifdef RUN_FOR_SPARK_BOARD

#define CHASSIS_UART					USART2
#define GYRO_UART							UART5
#define BATT_UART							USART3
#define SONIC_UART						UART4
#define RS485_UART						USART4
#define RFIDREADER_UART				UART4

#define MAGTRACK_CANROUTER		CanRouter2
#define CHASSISDRV_CANROUTER 	CanRouter1
#define COPLEY_CANROUTER 			CanRouter1
#define RL_DRV_CANROUTER 			CanRouter2
#define SUBSYSTEM_CANROUTER		CanRouter2

#endif

/* for FuWu Control Board */
#ifdef RUN_FOR_FW_BOARD

#define CHASSIS_UART					USART2
#define GYRO_UART							USART1
#define BATT_UART							USART3
#define SONIC_UART						UART4
#define RS485_UART						UART4
#define RFIDREADER_UART				UART4

#define MAGTRACK_CANROUTER		CanRouter1
#define CHASSISDRV_CANROUTER 	CanRouter2
#define COPLEY_CANROUTER 			CanRouter2
#define RL_DRV_CANROUTER 			CanRouter1
#define SUBSYSTEM_CANROUTER		CanRouter1

#endif

/* for INT Board */
#ifdef RUN_FOR_INT_BOARD

#define CHASSIS_UART					USART2
#define GYRO_UART							USART1
#define BATT_UART							USART3
#define SONIC_UART						USART2
#define RS485_UART						USART6
#define RFIDREADER_UART				UART4

#define MAGTRACK_CANROUTER		CanRouter1
#define CHASSISDRV_CANROUTER 	CanRouter1
#define COPLEY_CANROUTER 			CanRouter2
#define RL_DRV_CANROUTER 			CanRouter1
#define SUBSYSTEM_CANROUTER		CanRouter1

#endif

#endif
//end of file
