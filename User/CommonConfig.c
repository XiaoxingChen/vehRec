#include "stm32f4xx.h"
#include "CommonConfig.h"

void NVIC_CONFIG(void)
{
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); 
		__set_PRIMASK(0);
}
void InitWatchDog(uint16_t time_ms)
{
	IWDG_WriteAccessCmd(IWDG_WriteAccess_Enable);
  IWDG_SetPrescaler(IWDG_Prescaler_32);
  IWDG_SetReload(time_ms);
  IWDG_Enable();
	IWDG_ReloadCounter();
}

