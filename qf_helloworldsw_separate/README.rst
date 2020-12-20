QuickFeather HelloWorld SW (Cortex M4 + FPGA) Application - Separated
=====================================================================

This test/example contains the :code:`qf_helloworldsw` example, but with the fpga design (usb2serial) available as a separate binary, and the m4 code alone compiled into a separate binary.

The original example has the m4 code include the fpga code (in a C header form) into a single m4 binary.

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
    
- Build:

  - Build this application as usual using :code:`make` from the :code:`GCC_Project` directory

  - The M4 binary is generated in :code:`GCC_Project/output/bin`

- Flash:

  - the binary format file :code:`fpga/usb2serial_fpga.bin` is available in this project - this is the usb2serial fpga binary that the bootloader can load.
  
  - Flash both the m4 and fpga binaries using (from the :code:`GCC_Project` directory) 
    
    ::

      qfprog --port /dev/ttyACM0 --m4app output/bin/qf_helloworldsw_separate.bin --appfpga ../fpga/usb2serial_fpga.bin --mode fpga-m4

    | Note the :code:`--mode` option at the end, which is now mandatory - this specifies the operating mode which the bootloader uses.
    | :code:`--mode fpga-m4` (or equivalently :code:`--mode m4-fpga`) ensures that the bootloader knows that both m4app binary and the appfpga binary are flashed, and it will load the flashed appfpga binary and then load the m4app binary.
    |


- Run:

  - | The m4app uses the USB2SERIAL on the FPGA to communicate, instead of the EOS S3 UART in this case.
    | Connect a Serial Terminal app to the USB port of the QuickFeather board (most likely a ttyACMx device) at 115200 baud and 8N1 configuration.

  - Reset the board, the appfgpa and m4app should get loaded by the bootloader and start running.

  - You should see a banner similar to below on the EOS S3 UART:

    ::

      ##########################
      Quicklogic QuickFeather LED / User Button Test
      SW Version: qorc-sdk/qf_apps/qf_helloworldsw
      Sep 20 2020 14:24:43
      ##########################

      #*******************
      Command Line Interface
      App SW Version: qorc-sdk/qf_apps/qf_helloworldsw
      #*******************
      [0] >


  - | The :code:`diag` submenu option is available, and can be used to toggle the RGB leds or detect the USR button press:
    |
    | Toggle LEDs:
    | At the :code:`[0] >` prompt, which is the level 0 prompt, use:
    
    - :code:`diag red` to toggle the red led
    - :code:`diag green` to toggle the green led
    - :code:`diag blue` to toggle the blue led
    
    | Detect USR button press:
    | At the :code:`[0] >` prompt, which is the level 0 prompt, do: 

    - Keep the USR button pressed (connected to IO_6 on QuickFeather) and execute: :code:`diag userbutton` to check state - it should show :code:`TODO fill the ouput here`
    - Without the USR button pressed, :code:`diag userbutton` should show: :code:`TODO fill the output here`
    

Notes
-----

1. :code:`usb2serial.bit` is prebuilt bitstream only, taken as is from the s3_gateware (:code:`usb2serial.bin`) and kept here for convenience.
   
   The name is changed from :code:`usb2serial.bin` to :code:`usb2serial.bit` for clarity that it is the bitstream only.

   The (very minimal) python script :code:`fpga/gen_usb2serial_binary.py` can be run to generate the fpga binary :code:`usb2serial_fpga.bin` which can be loaded by the bootloader.

2. The FPGA power domain should not be switched off as this will reset the FPGA configuration and any access into the FPGA will result in a hardfault.

   This is done in :code:`s3x_pwrcfg.c` where we set the value of :code:`cfg_state` field of the :code:`PI_FB` power domain to :code:`PI_NO_CFG` instead of the default :code:`PI_SET_SHDN`.

3. In the current example, the pad configuration is being done in the M4 application only, as the iomux content is empty in the fpga binary (yet to be updated)
