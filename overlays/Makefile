DEVICE := xilinx_u200_xdma_201830_2
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
INSTALL_PATH := ../pynq_alveo_examples/notebooks

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

advanced: check-vitis check-xrt advanced.$(TARGET).$(XSA).xclbin

kernel_opt: check-vitis check-xrt kernel_opt.$(TARGET).$(XSA).xclbin

intro: check-vitis check-xrt intro.$(TARGET).$(XSA).xclbin

# install targets assume both xclbin and dst folder exist
install: $(INSTALL_TARGETS)

check-vitis:
ifndef XILINX_VITIS
	$(error XILINX_VITIS is not set. Please make sure you have sourced the Vitis settings64.{csh,sh})
endif

check-xrt:
ifndef XILINX_XRT
	$(error XILINX_XRT variable is not set. Please make sure you have sourced the XRT setup.{csh,sh})
endif

$(INSTALL_PATH)/1-introduction/intro.xclbin:
ifneq (,$(wildcard intro.$(TARGET).$(XSA).xclbin))
ifneq (,$(wildcard $(INSTALL_PATH)/1-introduction))
	$(CP) intro.$(TARGET).$(XSA).xclbin $@
else ifneq (,$(wildcard $(INSTALL_PATH)/1_introduction))
	$(CP) intro.$(TARGET).$(XSA).xclbin $(INSTALL_PATH)/1_introduction/intro.xclbin
else
	$(warning Could not copy to $(INSTALL_PATH)/1-introduction as the folder does not exist)
endif
else
	$(warning Could not find file intro.$(TARGET).$(XSA).xclbin)
endif
$(INSTALL_PATH)/2-kernel-optimization/kernel_opt.xclbin:
ifneq (,$(wildcard kernel_opt.$(TARGET).$(XSA).xclbin))
ifneq (,$(wildcard $(INSTALL_PATH)/2-kernel-optimization))
	$(CP) kernel_opt.$(TARGET).$(XSA).xclbin $@
else ifneq (,$(wildcard $(INSTALL_PATH)/2_kernel_optimization))
	$(CP) kernel_opt.$(TARGET).$(XSA).xclbin $(INSTALL_PATH)/2_kernel_optimization/kernel_opt.xclbin
else
	$(warning Could not copy to $(INSTALL_PATH)/2-kernel-optimization as the folder does not exist)
endif
else
	$(warning Could not find file kernel_opt.$(TARGET).$(XSA).xclbin)
endif
$(INSTALL_PATH)/3-advanced-features/advanced.xclbin:
ifneq (,$(wildcard advanced.$(TARGET).$(XSA).xclbin))
ifneq (,$(wildcard $(INSTALL_PATH)/3-advanced-features))
	$(CP) advanced.$(TARGET).$(XSA).xclbin $@
else ifneq (,$(wildcard $(INSTALL_PATH)/3_advanced_features))
	$(CP) advanced.$(TARGET).$(XSA).xclbin $(INSTALL_PATH)/3_advanced_features
else
	$(warning Could not copy to $(INSTALL_PATH)/3-advanced-features as the folder does not exist)
endif
else
	$(warning Could not find file advanced.$(TARGET).$(XSA).xclbin)
endif

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
	-$(RM) *.log *.jou  *.info *.ltx *.pb *.link_summary

cleanall: clean
	-$(RM) *.xclbin
