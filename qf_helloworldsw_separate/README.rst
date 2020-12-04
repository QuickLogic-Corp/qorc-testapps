QuickFeather HelloWorld HW (Cortex M4 + FPGA) Application - Separated
=====================================================================

This test/example contains the :code:`qf_helloworldhw` example, but with the fpga design (usb2serial) available as a separate binary, and the m4 code alone compiled into a separate binary.

The original example has the m4 code include the fpga code (in a C header form) into a single m4 binary.

How To
------

- Ensure that the binary format file :code:`fpga/usb2serial_fpga.bin` is available in this project - this is the usb2serial fpga binary that the bootloader can load.
- Build as usual using :code:`make` from the :code:`GCC_Project` dir
- The M4 binary is generated in :code:`GCC_Project/output/bin`
- Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)
- Flash both the m4 and fpga binaries using (from the :code:`GCC_Project` directory) ::

   qfprog --port /dev/ttyACM0 --m4app output/bin/qf_helloworldsw_separate.bin --appfpga ../fpga/usb2serial_fpga.bin --mode fpga-m4

Notes
-----

1. :code:`usb2serial.bit` is prebuilt bitstream only, taken as is from the s3_gateware (:code:`usb2serial.bin`) and kept here for convenience.
   
   The name is changed from :code:`usb2serial.bin` to :code:`usb2serial.bit` for clarity that it is the bitstream only.

   The (very minimal) python script :code:`fpga/gen_usb2serial_binary.py` can be run to generate the fpga binary :code:`usb2serial_fpga.bin` which can be loaded by the bootloader.

   Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)

2. The FPGA power domain should not be switched off as this will reset the FPGA configuration and any access into the FPGA will result in a hardfault.

   This is done in :code:`s3x_pwrcfg.c` where we set the value of :code:`cfg_state` field of the :code:`PI_FB` power domain to :code:`PI_NO_CFG` instead of the default :code:`PI_SET_SHDN`.

3. In the current example, the pad configuration is being done in the M4 application only, as the iomux content is empty (yet)