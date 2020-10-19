all:	usbspeed baremetal ramblockinit

.PHONY:usbspeed
usbspeed:
	cd qf_$@/GCC_Project && make

CLEAN_TARGET += usbspeed
usbspeed_clean:
	cd qf_$(subst _clean,,$@)/GCC_Project && make clean

.PHONY:baremetal
baremetal:
	cd qf_$@/GCC_Project && make

CLEAN_TARGET += baremetal
baremetal_clean:
	cd qf_$(subst _clean,,$@)/GCC_Project && make clean

.PHONY:ramblockinit
ramblockinit:
	cd qf_$@/GCC_Project && make

CLEAN_TARGET += ramblockinit
ramblockinit_clean:
	cd qf_$(subst _clean,,$@)/GCC_Project && make clean


$(info CLEAN_TARGET $(CLEAN_TARGET))
clean:	$(CLEAN_TARGET:%=%_clean)

