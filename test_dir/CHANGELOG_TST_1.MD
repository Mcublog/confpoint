# CHANGE LOG

| dfs          | dfs           | dfdf | sdfs |      | dfsdf | fsdfs |
| ------------ | ------------- | ---- | ---- | ---- | ----- | ----- |
| sdfs         | ssdfds        | 5554 | sdfs | sdfs |       |       |
| First Header | Second Header |      |      |      |       |       |
| Content Cell | Content Cell  |      |      |      |       |       |
| Content Cell | Content Cell  |      |      |      |       |       |
|              |               |      |      |      |       |       |

## v1.4.0 (2021-08-11)

* BootCommander: add xcp-to-file transport protocol (for Bluetooth update);
* Target: add FlashWriteHook for F4;
* Target: add BootTaskHook;
* Target: add hwid command for UART trasport protocol;
* Target: fix L4 flash layout;
* Host: added x64 libs version;

## v1.3.1 (2021-08-06)

* added handling missing lib file (Python bind);
* added openblt.zip to Host dir (Python bind);
* added support BalbinBlue adapter;

## v1.3.0 (2021-08-03)

* Target: add support STM32G0 (USB, FDCAN);

## v1.2.0 (2021-07-26)

* Target: add support STM32F0 (USB, CAN);
* Target: fix bootloader for Cortex-M0 CPU;

## v1.1.1 (2021-07-01)

* fix opening COM port with number greater than 10;

## v1.1.0 (2021-06-24)

**Description:** After this update need to add BOOT_FLASH_USER_PROG_BASE_ADDRESS define in blt_conf.h
with user program base address.

* Target: add support USB Bulk for STM32L4;
* Target: add BOOT_FLASH_USER_PROG_BASE_ADDRESS define;

## v1.0.1 (2021-06-09)

* add getting buffer offset function from the OpenBLT lib,
it needs for the correct work progress bar in Python

## v1.0.0 (2021-06-02)

* add enumeration and HWID CAN user commands;
* add key generator;
* add Balbin Can adapter support;
* add Balbin filter setting support;
* add Balbin support in Microboot/BootCommander utils.
