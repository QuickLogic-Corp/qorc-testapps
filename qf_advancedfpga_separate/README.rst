QuickFeather Advanced (Cortex M4 + FPGA) Application - Separated
================================================================

This test/example contains the :code:`qf_advancedfpga` example, but with the fpga design compiled into a separate binary, and the m4 code alone compiled into a separate binary.

The original example has the m4 code include the fpga code (in a C header form) into a single m4 binary.

How To
------

- Ensure that an appropriate version of the FPGA toolchain is used for compilation, which supports the FPGA binary generation (v1.3.1 or above)
- Build as usual using :code:`make` from the :code:`GCC_Project` dir
- The M4 binary is generated in :code:`GCC_Project/output/bin` and the FPGA binary is generated in :code:`fpga/rtl`
- Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)
- Flash both the m4 and fpga binaries using (from the :code:`GCC_Project` directory) ::

   qfprog --port /dev/ttyACM0 --m4app output/bin/qf_advancedfpga_separate.bin --appfpga ../fpga/rtl/AL4S3B_FPGA_top.bin --mode fpga-m4

Notes
-----

1. Ensure that an appropriate version of the FPGA toolchain is used for compilation, which supports the FPGA binary generation (v1.3.1 or above)

   Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)

2. The FPGA compilation in the makefile :code:`Makefile.common` has the :code:`-dump binary` option added so that the FPGA binary is generated, in the :code:`rtl/` directory.

3. The FPGA power domain should not be switched off as this will reset the FPGA configuration and any access into the FPGA will result in a hardfault.

   This is done in :code:`s3x_pwrcfg.c` where we set the value of :code:`cfg_state` field of the :code:`PI_FB` power domain to :code:`PI_NO_CFG` instead of the default :code:`PI_SET_SHDN`.

4. The pad configuration in the M4 Application does not need to set any FPGA related pads, it will be applied by the Bootloader automatically.

   These can be removed from :code:`pincfg_table.c` (we have removed in the current test application).

   However, leaving them in the M4 Application will not have any adverse effect, so they can be left in as well.