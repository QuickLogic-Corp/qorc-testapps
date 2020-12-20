QuickFeather Advanced (Cortex M4 + FPGA) Application - Separated
================================================================

This test/example contains the :code:`qf_advancedfpga` example, but with the fpga design compiled into a separate binary, and the m4 code compiled into a separate binary.

The original example has the m4 code include the fpga code (in a C header form) into a single m4 binary.

This example test app can be used as a guide for apps which have both m4 code and fpga rtl to be built within the same application project, and flashed as separate binary images.

Other changes from the :code:`qf_advancedfpga` application:

- | :code:`GCC_Project/makefiles/Makefile_common` changed to add generation of appfpga binary using the FPGA toolchain with the :code:`-dump binary` added as below:
  | :code:`time ql_symbiflow  -compile -src $(MAIN_FPGA_RTL_DIR) -d ql-eos-s3 -t $(RTL_TOP_MODULE) -v $(FPGA_RTL_SRCS) -p quickfeather.pcf -P PU64 -dump header -dump binary | grep -v $(SYMBIFLOW_WARN_PATTERN)`
  |

- | :code:`src/main.c` changed to remove the fpga loader, line: :code:`load_fpga(sizeof(axFPGABitStream),axFPGABitStream);`
  |

- | :code:`src/s3x_pwrcfg.c` changed to keep the FPGA power domain without change, default setting shuts down the FPGA power domain when m4app initialization happens:
  
  .. code::

        [PI_FB] =  {
            .name = "FB",
            .pctrl = PI_CTRL(0xa0, 0xa4, 0x200, 0x210, 1, 2, 2),
            .ginfo = PI_GINFO(4, S3X_FB_02_CLK, S3X_FB_16_CLK, S3X_FB_21_CLK , S3X_CLKGATE_FB, 0),
            .cfg_state = PI_SET_SHDN,
        },

  changed to:

  .. code::

        [PI_FB] =  {
            .name = "FB",
            .pctrl = PI_CTRL(0xa0, 0xa4, 0x200, 0x210, 1, 2, 2),
            .ginfo = PI_GINFO(4, S3X_FB_02_CLK, S3X_FB_16_CLK, S3X_FB_21_CLK , S3X_CLKGATE_FB, 0),
            .cfg_state = PI_NO_CFG,
        },

Note also that the clock settings for the FPGA domain need to be set correctly from the M4 code.

Most FPGA designs will use clocks C16 and C21 and these must be kept at appropriate frequencies, depending on FPGA design

For this particular design, we need both C16 and C21 at 12MHz, which is done in :code:`fpga_ledctlr.c`

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

  - Build as usual using :code:`make` from the :code:`GCC_Project` dir

  - The M4 binary is generated in :code:`GCC_Project/output/bin` and the FPGA binary is generated in :code:`fpga/rtl` due to our change in the :code:`Makefile_common`

- Flash:

  - Set the board in programming mode.

  - | Flash both the m4 and fpga binaries using (from the :code:`GCC_Project` directory)

    ::

      qfprog --port /dev/ttyACM0 --m4app output/bin/qf_advancedfpga_separate.bin --appfpga ../fpga/rtl/AL4S3B_FPGA_top.bin --mode fpga-m4

    | Note the :code:`--mode` option at the end, which is now mandatory - this specifies the operating mode which the bootloader uses.
    | :code:`--mode fpga-m4` (or equivalently :code:`--mode m4-fpga`) ensures that the bootloader knows that both m4app binary and the appfpga binary are flashed, and it will load the flashed appfpga binary and then load the m4app binary.
    |


- Run:

  - | Ensure that a (3.3V) USB-UART cable is connected to the EOS S3 UART pins.
    | For QuickFeather, refer to `quick-feather-dev-board <https://github.com/QuickLogic-Corp/quick-feather-dev-board#advanced>`_ for details.
    | Connect a Serial Terminal app to the USB port of the USB-UART cable (most likely a ttyUSBx device) at 115200 baud and 8N1 configuration.

  - Reset the board, the appfgpa and m4app should get loaded by the bootloader and start running.

  - You should see a banner similar to below on the EOS S3 UART: 
    ::

      ##########################
      Quicklogic QuickFeather Advanced FPGA Example
      SW Version: qorc-sdk/qf_apps/qf_advancedfpga
      Sep 20 2020 14:24:43
      ##########################
    
      #*******************
      Command Line Interface
      App SW Version: qorc-sdk/qf_apps/qf_advancedfpga
      #*******************
      [0] >


  - | The :code:`ledctlr` submenu option is available, and can be used to set RGB led to change color at specific intervals.
    |
    | :code:`ledctlr` test sequence:
    | At the :code:`[0] >` prompt, which is the level 0 prompt, use: 

    1. :code:`ledctlr` to enter the submenu
    2. :code:`color0 1` sets the color0 (for timeslot0) to blue, you should see the blue led turn on
    3. :code:`color1 2` sets the color1 (for timeslot1) to green, no visible change
    4. :code:`color2 4` sets the color2 (for timeslot2) to red, no visible change
    5. :code:`duration0 500` sets the duration of timeslot0 (for color0)
    6. | :code:`duration1 500` sets the duration of timeslot1 (for color1)
       | Now, color0(blue) should be seen for 500ms, and color1(green) should be seen for 500ms and should repeat.
    7. | :code:`duration2 1000` sets the duration of timeslot2 (for color2)
       | Now, color0(blue) for 500ms, color1(green) for 500ms and color2(red) for 1000ms should be seen, and should repeat.


Notes
-----

1. | The FPGA compilation in the makefile :code:`Makefile.common` has the :code:`-dump binary` option added so that the FPGA binary is generated, in the :code:`rtl/` directory.
   | This simplifies the build process so that both m4 and fpga build can be invoked with a simple :code:`make` as usual.
   |

2. | Ensure that the FPGA power domain is not be switched off in the m4 code, as this will reset the FPGA configuration and any access into the FPGA will result in a hardfault.
   | This can be done in :code:`s3x_pwrcfg.c` where we set the value of :code:`cfg_state` field of the :code:`PI_FB` power domain to :code:`PI_NO_CFG` instead of the default :code:`PI_SET_SHDN`.
   |
   | On a related note, ensure that the FPGA source clocks (C16, C21 for most designs) are set at a suitable frequency according to design, in the M4 code.

3. | The pad configuration in the m4 code does not need to set any FPGA related pads, as it will be applied by the Bootloader automatically.
   | These can be removed from :code:`pincfg_table.c` (we have removed the pad config in the current test application).
   | However, leaving them in the M4 Application will not have any adverse effect, so they can be left in as well.
   |
