#include "hardware.h"
#include "IoHomecontrol.h"
#include "Logic.h"
#include "FunctionBlocksModule.h"
#include "OpenKNX.h"
#if defined(KNX_IP_WIFI) || defined(KNX_IP_LAN)
#include "NetworkModule.h"
#endif

void setup()
{
    openknx.init();

#if defined(KNX_IP_WIFI) || defined(KNX_IP_LAN)
    openknx.addModule(0, openknxNetwork);
#endif
    openknx.addModule(1, openknxIoHomecontrol);
    openknx.addModule(2, openknxLogic);
    openknx.addModule(3, openknxFunctionBlocksModule);

    openknx.setup();
}

void loop()
{
    openknx.loop();
}

#ifdef OPENKNX_DUALCORE
void setup1()
{
    openknx.setup1();
}

void loop1()
{
    openknx.loop1();
}
#endif