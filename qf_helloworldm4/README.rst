QuickFeather HelloWorld M4 Application
======================================

This test/example contains the :code:`qf_helloworldm4` example, which is a bare-minimum m4 only application.

How To
------

- Build as usual using :code:`make` from the :code:`GCC_Project` dir
- The M4 binary is generated in :code:`GCC_Project/output/bin`
- Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)
- Flash both the m4 and fpga binaries using (from the :code:`GCC_Project` directory) ::

   qfprog --port /dev/ttyACM0 --m4app output/bin/qf_helloworldm4.bin --mode m4
