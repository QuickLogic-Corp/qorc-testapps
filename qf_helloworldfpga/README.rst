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

  - | Update the bootloader to the latest from `qorc-sdk <https://github.com/QuickLogic-Corp/qorc-sdk>`_ :code:`master`
    |
    | Clone the qorc-sdk repo, or update it to latest using:
    | :code:`git checkout master && git pull`
    | Build the :code:`qf_bootloader` app as usual using :code:`make` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
    | Flash the built bootloader bin using:
    | :code:`qfprog --bootloader output/bin/qf_bootloader.bin` from :code:`qf_apps/qf_bootloader/GCC_Project` directory
    |

  - | Ensure to use the latest FPGA toolchain which supports generation of FPGA binary (v1.3.1 or above)
    |
    | Alternatively, FPGA toolchain daily build can be setup as below:

    ::
      
      export INSTALL_DIR=/path/to/fpga/toolchain/install
      wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O conda_installer.sh
      bash conda_installer.sh -b -p $INSTALL_DIR/conda && rm conda_installer.sh
      source "$INSTALL_DIR/conda/etc/profile.d/conda.sh"
      echo "include-system-site-packages=false" >> $INSTALL_DIR/conda/pyvenv.cfg
      CONDA_FLAGS="-y --override-channels -c defaults -c conda-forge"
      conda update $CONDA_FLAGS -q conda
      curl $(curl https://storage.googleapis.com/symbiflow-arch-defs-install/latest) > arch.tar.gz
      tar -C $INSTALL_DIR -xvf arch.tar.gz && rm arch.tar.gz
      conda install $CONDA_FLAGS -c quicklogic-corp/label/ql yosys="0.8.0_0002_gc3b38fdc 20200901_073908" python=3.7
      conda install $CONDA_FLAGS -c quicklogic-corp/label/ql yosys-plugins="1.2.0_0009_g9ab211c 20201001_121833"
      conda install $CONDA_FLAGS -c quicklogic-corp/label/ql vtr="v8.0.0_rc2_2894_gdadca7ecf 20201008_140004"
      conda install $CONDA_FLAGS -c quicklogic-corp iverilog
      conda install $CONDA_FLAGS -c tfors gtkwave
      conda install $CONDA_FLAGS make lxml simplejson intervaltree git pip
      conda activate
      pip install python-constraint
      pip install serial
      pip install git+https://github.com/QuickLogic-Corp/quicklogic-fasm
      conda deactivate
    
  - | Initialize the FPGA toolchain to use.
    |
    | Export the environment variable :code:`$INSTALL_DIR` using:
    
    ::
    
      export INSTALL_DIR=/path/to/fpga/toolchain
      
    | where :code:`$INSTALL_DIR` points to the base path of the FPGA toolchain install directory
    |
    | Initialize the conda env for the toolchain using:
    
    ::
    
     export PATH="$INSTALL_DIR/quicklogic-arch-defs/bin:$INSTALL_DIR/quicklogic-arch-defs/bin/python:$PATH"
     source "$INSTALL_DIR/conda/etc/profile.d/conda.sh"
     conda activate

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
