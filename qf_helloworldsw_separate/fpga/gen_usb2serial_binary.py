
# a *very* minimal conversion from a bitstream only fpga to fpga binary format 
# that can be loaded by the qorc-sdk bootloader(v2.1 or above)

# 8 word header:
# bin version = 0.1 = 0x00000001
# bitstream size = 75960 = 0x000128B8
# bitstream crc = 0x0 (not used)
# meminit size = 0x0 (not used)
# meminit crc = 0x0 (not used)
# iomux size = 0x0 (not used)
# iomux crc = 0x0 (not used)
# reserved = 0x0 (not used)

header = [
    0x00000001,
    0x000128B8,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000,
    0x00000000
]

fpga_binary_bytearray = bytearray()

# add header bytes
for each_word in header:
    fpga_binary_bytearray.extend(int(each_word).to_bytes(4, "little"))

# add bitstream content
with open('usb2serial.bit', 'rb') as fpga_bitstream:
    fpga_binary_bytearray.extend(fpga_bitstream.read())

# other content is zero length, save binary:

with open('usb2serial_fpga.bin', 'wb') as fpga_binary:
    fpga_binary.write(fpga_binary_bytearray)