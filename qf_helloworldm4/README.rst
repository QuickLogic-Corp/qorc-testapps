QuickFeather HelloWorld M4 Application
======================================

This test/example contains the :code:`qf_helloworldm4` example, which is a bare-minimum m4 only application.

How To
------
- Setup:

  - | Update the programmer to the latest from `TinyFPGAProgrammer-Application <https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application>`_ :code:`master`.
    |
    | This has the required changes to support independent m4app, independent appfpga and m4app+appfpga images.
    | Refer to `TinyFPGAProgrammer-Application <https://github.com/QuickLogic-Corp/TinyFPGA-Programmer-Application>`_ for details on changes.
    |

  - | Update the bootloader to the latest from `qorc-sdk <https://github.com/QuickLogic-Corp/qorc-sdk>`_ :code:`master`
    |
    | Clone the repo, or update it to latest using:
    | :code:`git checkout master && git pull`
    | Build the :code:`qf_bootloader` app as usual using :code:`make` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
    | Flash the built bootloader bin using:
    | :code:`qfprog --bootloader output/bin/qf_bootloader.bin` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
    |

- Build this application as usual using :code:`make` from the :code:`GCC_Project` directory

- The M4 binary is generated in :code:`GCC_Project/output/bin`

- Flash the m4 binary using (from the :code:`GCC_Project` directory) ::

   qfprog --port /dev/ttyACM0 --m4app output/bin/qf_helloworldm4.bin --mode m4

- | Note the :code:`--mode` option at the end, which is now mandatory - this specifies the operating mode which the bootloader uses.
  | :code:`--mode m4` ensures that the bootloader knows that only the m4app binary is flashed, and it will load the flashed m4app binary only.
