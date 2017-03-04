#include "stm32f4xx.h"
#include "CommonConfig.h"
#include "Console.h"
#include "Timer.h"

int main(void)
{ 
	SCB->VTOR = 0x08000000;
	NVIC_CONFIG();
	
	BaseTimer::Instance()->initialize();
	Console::Instance()->printf("\r\nReboot Now\r\n");

	InitWatchDog(5000);
	while(1)
	{
		Console::Instance()->runTransmitter();
		ServiceDog();
	}
}

#if 1

/**
  * @brief  Reports the name of the source file and the source line number
  *   where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t* file, uint32_t line)
{ 
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
	Timer loopTimer(1000,1000);
	
  /* Infinite loop */
  while (1)
  {
		Console::Instance()->runTransmitter();
		if(loopTimer.isAbsoluteTimeUp())
		{
			Console::Instance()->printf("Wrong parameters value: file %s on line %d\r\n", file, line);
		}
  }
}
#endif

