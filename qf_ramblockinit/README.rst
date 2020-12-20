QuickFeather FPGA RAM Block Init Test
=====================================

This is a test app to exercise the fpga loader to initialize the RAM blocks using the RAM initialization values prescribed in the HEX files in the FPGA design directory.
This also exercises the ability of the QuickLogic FPGA toolchain to use the HEX files to generate the RAM initialization values.

The RAM initialization values are in addition to the FPGA bitstream.

In the header generation method, where the FPGA bitstream is represented as a C array, the RAM initialization values are also represented as another C array in the FPGA header produced.
In the binary generation method, the FPGA bitstream and the RAM initialization values are present in a specific format in the FPGA binary produced.
Similarly, in the debugger script generation methods (currently JLink and OpenOCD scripts), the RAM initialization values are present.

In the current application, the header generation method is used, which produces a header file, which contains the FPGA bitstream, and the RAM Initialization values.

The header file generated is :code:`fpga/rtl/top_bit.h` and has the following structure

::

  uint32_t	axFPGABitStream[] = {

  /* 32 bit values which is the FPGA bitstream to be programmed */
  
  };
  
  uint32_t   axFPGAMemInit[] = {

  /* RAM Block 0 */
  0x40018000, 0x400, /* START ADDR, NUMBER OF WORDS*/
  VALUES,

  ... repeated for number of RAM Blocks to be initialized.
  };

  uint32_t   axFPGAIOMuxInit[] = {

  REG,VALUE
  ... repeated for number of PADs used by the FPGA
  ... and overall MUX settings
  };

To load the FPGA bitstream, and perform RAM initialization, the following API is used:

::

  load_fpga_with_mem_init(axFPGABitStream_length, axFPGABitStream, axFPGAMemInit_length, axFPGAMemInit)

Refer to :code:`src/fpga_design.c` and :code:`src/fpga_design.h` for one method of using the :code:`fpga/rtl/top_bit.h` FPGA arrays in :code:`src/main.c` to call the FPGA Loader API.

The implementation of the FPGA Loader API can be found in :code:`qorc-sdk/Libraries/FPGA/fpga_loader.c`.



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

  - Build as usual using :code:`make` from the :code:`GCC_Project` dir

  - The FPGA header is generated in :code:`fpga/rtl` as :code:`top_bit.h` and The M4 binary is generated in :code:`GCC_Project/output/bin` which is built including the FPGA header internally.

- Flash:

  - Set the board in programming mode.

  - | Flash the m4 binary (from the :code:`GCC_Project` directory)
    
    ::

      qfprog --port /dev/ttyACM0 --m4app output/bin/qf_ramblockinit.bin --mode m4

    | Note the :code:`--mode` option at the end, which is now mandatory - this specifies the operating mode which the bootloader uses.
    | :code:`--mode m4` ensures that the bootloader knows that the m4app binary is flashed, and it will load the flashed m4app binary.
    |


- Run:

  - | Ensure that a (3.3V) USB-UART cable is connected to the EOS S3 UART pins.
    | For QuickFeather, refer to `quick-feather-dev-board <https://github.com/QuickLogic-Corp/quick-feather-dev-board#advanced>`_ for details.
    | Connect a Serial Terminal app to the USB port of the USB-UART cable (most likely a ttyUSBx device) at 115200 baud and 8N1 configuration.

  - Reset the board, m4app should get loaded by the bootloader and start running.

  - You should see a banner similar to below on the EOS S3 UART: 

    ::

      ##########################
      Quicklogic QuickFeather RAM Init Test
      SW Version: qorc-sdk/qf_testapps/qf_ramblockinit
      Sep 20 2020 14:24:43
      ##########################
    
      #*******************
      Command Line Interface
      App SW Version: qorc-sdk/qf_testapps/qf_ramblockinit
      #*******************
      [0] >


  - | If there are any errors in the RAM initialization, you would see :code:`FPGA Load Failed!`
    | Hopefully, you would not get a chance to see this message...
    |
