QuickFeather HelloWorld FPGA Application
========================================

This test/example contains the the fpga design available as an independent component.


How To
------

- | Ensure that the FPGA toolchain is updated to the one which supports generation of FPGA binary.
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


- | Export the environment variable :code:`$INSTALL_DIR` using:
  | :code:`export INSTALL_DIR=/path/to/fpga/toolchain`
  | where :code:`$INSTALL_DIR` points to the base path of the FPGA toolchain install directory
  | Initialize the conda env for the toolchain using:
  | :code:`export PATH="$INSTALL_DIR/quicklogic-arch-defs/bin:$INSTALL_DIR/quicklogic-arch-defs/bin/python:$PATH"`
  | :code:`source "$INSTALL_DIR/conda/etc/profile.d/conda.sh"`
  | :code:`conda activate`
  |
  

- | Build the FPGA design using :
  | :code:`ql_symbiflow -compile -src fpga/rtl -d ql-eos-s3 -t helloworldfpga -v *.v -p quickfeather.pcf -P PU64 -dump binary`
  | from this application's root directory
  | The binary will be generated as : :code:`fpga/rtl/helloworldfpga.bin`

- Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)

- | Flash both the fpga binary using (from the application root directory)
  | :code:`qfprog --port /dev/ttyACM0 --appfpga fpga/rtl/helloworldfpga.bin --mode fpga`

Notes
-----

1. :code:`usb2serial.bit` is prebuilt bitstream only, taken as is from the s3_gateware (:code:`usb2serial.bin`) and kept here for convenience.
   
   The name is changed from :code:`usb2serial.bin` to :code:`usb2serial.bit` for clarity that it is the bitstream only.

   The (very minimal) python script :code:`fpga/gen_usb2serial_binary.py` can be run to generate the fpga binary :code:`usb2serial_fpga.bin` which can be loaded by the bootloader.

   Ensure that the bootloader flashed supports separate fpga and m4 binary loading (v2.1 or above)

2. The FPGA power domain should not be switched off as this will reset the FPGA configuration and any access into the FPGA will result in a hardfault.

   This is done in :code:`s3x_pwrcfg.c` where we set the value of :code:`cfg_state` field of the :code:`PI_FB` power domain to :code:`PI_NO_CFG` instead of the default :code:`PI_SET_SHDN`.

3. In the current example, the pad configuration is being done in the M4 application only, as the iomux content is empty (yet)
