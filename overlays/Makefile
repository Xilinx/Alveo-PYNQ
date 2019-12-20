DEVICE = xilinx_u200_xdma_201830_2
TARGET := hw
FREQUENCY := 300
VPP := v++

CP = cp -rf
RM = rm -f
RMDIR = rm -rf

# device2xsa - create a filesystem friendly name from device name
# $(1) - full name of device
device2xsa = $(strip $(patsubst %.xpfm, % , $(shell basename $(DEVICE))))
XSA := $(call device2xsa, $(DEVICE))

XO_DIR := ./_xo.$(TARGET).$(XSA)
XCLBIN_DIR := ./_xclbin.$(TARGET).$(XSA)
MOD_SRC_DIR := .src
SRC_DIR := src
INSTALL_PATH := ../pynqexamples/notebooks

# Kernel compiler global settings
CLFLAGS += -t $(TARGET) --platform $(DEVICE)
ifneq ($(TARGET), hw)
	CLFLAGS += -g
endif

INTRO_XO += $(XO_DIR)/vadd.xo
INTRO_XO += $(XO_DIR)/vmult.xo
KRNL_OPT_XO += $(XO_DIR)/krnl_stream_vadd.xo
KRNL_OPT_XO += $(XO_DIR)/krnl_stream_vmult.xo
KRNL_OPT_XO += $(XO_DIR)/vadd_wide.xo
KRNL_OPT_XO += $(XO_DIR)/vadd_multibanks.xo
ADVANCED_XO += $(XO_DIR)/vadd_advanced.xo
ADVANCED_XO += $(XO_DIR)/mmult.xo

INSTALL_TARGETS += $(INSTALL_PATH)/3-advanced-features/advanced.xclbin
INSTALL_TARGETS += $(INSTALL_PATH)/2-kernel-optimization/kernel_opt.xclbin
INSTALL_TARGETS += $(INSTALL_PATH)/1-introduction/intro.xclbin

all: build install

build: advanced kernel_opt intro

advanced: advanced.$(TARGET).$(XSA).xclbin

kernel_opt: kernel_opt.$(TARGET).$(XSA).xclbin

intro: intro.$(TARGET).$(XSA).xclbin

# install targets assume both xclbin and dst folder exist
install: $(INSTALL_TARGETS)

$(INSTALL_PATH)/1-introduction/intro.xclbin: 
	$(CP) intro.$(TARGET).$(XSA).xclbin $@
$(INSTALL_PATH)/2-kernel-optimization/kernel_opt.xclbin:
	$(CP) kernel_opt.$(TARGET).$(XSA).xclbin $@
$(INSTALL_PATH)/3-advanced-features/advanced.xclbin:
	$(CP) advanced.$(TARGET).$(XSA).xclbin $@

$(MOD_SRC_DIR): 
	mkdir -p $@
$(XCLBIN_DIR): 
	mkdir -p $@
$(XO_DIR): 
	mkdir -p $@

$(MOD_SRC_DIR)/vadd_multibanks.cpp: $(SRC_DIR)/kernel_opt.cpp | $(MOD_SRC_DIR)
	$(CP) $< $@ 
	sed -i "s/void vadd_wide/void vadd_wide_multibanks/" $@
$(XO_DIR)/vadd.xo: vitis-examples/hello_world/src/vadd.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k vadd -o'$@' '$<'
$(XO_DIR)/vmult.xo: vitis-examples/sys_opt/slr_assign/src/kernel.cl | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k vmult -o'$@' '$<'
$(XO_DIR)/krnl_stream_vadd.xo: vitis-examples/host/streaming_k2k_mm/src/krnl_stream_vadd.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k krnl_stream_vadd -o'$@' '$<'
$(XO_DIR)/krnl_stream_vmult.xo: vitis-examples/host/streaming_k2k_mm/src/krnl_stream_vmult.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k krnl_stream_vmult -o'$@' '$<'
$(XO_DIR)/vadd_wide.xo: $(SRC_DIR)/kernel_opt.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k vadd_wide -o'$@' '$<'
$(XO_DIR)/vadd_multibanks.xo: $(MOD_SRC_DIR)/vadd_multibanks.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k vadd_wide_multibanks -o'$@' '$<'
$(XO_DIR)/vadd_advanced.xo: $(SRC_DIR)/advanced_features.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k vadd -o'$@' '$<'
$(XO_DIR)/mmult.xo: $(SRC_DIR)/advanced_features.cpp | $(XO_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XO_DIR) -c -k mmult -o'$@' '$<'
intro.$(TARGET).$(XSA).xclbin: $(INTRO_XO) | $(XCLBIN_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XCLBIN_DIR) --kernel_frequency $(FREQUENCY) -l -o'$@' $(+)
kernel_opt.$(TARGET).$(XSA).xclbin: $(KRNL_OPT_XO) | $(XCLBIN_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XCLBIN_DIR) --kernel_frequency $(FREQUENCY) -l --config kernel_opt.ini -o'$@' $(+)
advanced.$(TARGET).$(XSA).xclbin: $(ADVANCED_XO) | $(XCLBIN_DIR)
	$(VPP) $(CLFLAGS) --temp_dir $(XCLBIN_DIR) --kernel_frequency $(FREQUENCY) -l -o'$@' $(+)

clean:
	-$(RMDIR) _xclbin* _xo* .Xil $(MOD_SRC_DIR)
	-$(RMDIR) *.log *.jou  *.info *.ltx *.pb *.link_summary

cleanall: clean
	-$(RMDIR) *.xclbin
