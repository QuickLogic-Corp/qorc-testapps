QuickFeather HelloWorldFPGA Application
=======================================

This test/example contains the the fpga design available as an independent component, it is basically only the FPGA part of the :code:`qf_apps/qf_helloworldhw` application project.

The FPGA design is a simple LED-toggle, which toggles the green LED regularly.

How To
------

- Setup:

  - | Update the programmer to the latest from `TinyFPGAProgrammer-Application <https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application>`_ :code:`master`.
    |
    | This has the required changes to support independent m4app, independent appfpga and m4app+appfpga images.
    | Refer to `TinyFPGAProgrammer-Application <https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application>`_ for details on changes.
    |

  - | Update the bootloader to the latest from `qorc-sdk <https://github.com/QuickLogic-Corp/qorc-sdk>`_ :code:`master`, if not already done.
    
    - | Clone the repo, or update it to latest using:
      | :code:`git checkout master && git pull`
    
    - Build the :code:`qf_bootloader` app as usual using :code:`make` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
     
    - | Flash the built bootloader bin using:
      | :code:`qfprog --bootloader output/bin/qf_bootloader.bin --mode fpga-m4` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
    

  - Ensure to use the latest FPGA toolchain which supports generation of FPGA binary (v1.3.1 or above)

- Build:

  - | Build the FPGA design using :
    
    ::

      ql_symbiflow -compile -src fpga/rtl -d ql-eos-s3 -t helloworldfpga -v *.v -p quickfeather.pcf -P PU64 -dump binary
    
    | from this application's root directory
    | The binary will be generated as : :code:`fpga/rtl/helloworldfpga.bin`
    |

- Flash:

  - Set the board in programming mode.

  - | Flash the fpga binary using (from the application root directory)
    
    ::
      
      qfprog --port /dev/ttyACM0 --appfpga fpga/rtl/helloworldfpga.bin --mode fpga
    
    | Note the :code:`--mode` option at the end, which is now mandatory - this specifies the operating mode which the bootloader uses.
    | :code:`--mode fpga` ensures that the bootloader knows that only the appfpga binary is flashed, and it will load the flashed appfpga binary only.
    |

- Run:

  - Reset the board, the appfpga should get loaded by the bootloader and start running.

  - You should see the green LED regularly toggling once the appfpga starts running.
