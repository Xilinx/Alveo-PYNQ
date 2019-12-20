# Overlays for Alveo-PYNQ

In order to run the provided introductory notebooks we have designed a few 
overlays, and we have included the source files to rebuild them in this folder.
In particular, the overlays are obtained by combining a few ad-hoc kernels, 
along with a selected number of examples from the 
[Vitis Accel Examples](https://github.com/Xilinx/Vitis_Accel_Examples/tree/63bae10d581df40cf9402ed71ea825476751305d) 
repository.

## Included Overlays

There are a total of three overlays included in this repository:

1. **Introduction**: this overlay includes the *vector addition kernel* from 
the Vitis Accel Examples' 
[hello world](https://github.com/Xilinx/Vitis_Accel_Examples/tree/63bae10d581df40cf9402ed71ea825476751305d/hello_world) 
application, and the *vector multiplication kernel* from the 
[SLR Assign](https://github.com/Xilinx/Vitis_Accel_Examples/tree/63bae10d581df40cf9402ed71ea825476751305d/sys_opt/slr_assign) 
application. It is used for the 
[introduction notebooks](../pynqexamples/notebooks/1-introduction).

2. **Kernel Optimizations**: this overlay contains the *vector addition* and 
*vector multiplication* kernels (using streams) from the Vitis Accel Examples' 
[Stream Kernel to Kernel Memory Mapped](https://github.com/Xilinx/Vitis_Accel_Examples/tree/63bae10d581df40cf9402ed71ea825476751305d/host/streaming_k2k_mm) 
application, as well as a *wide vector addition* kernel that uses a 
a 512 bit datapath and has been specifically developed for this overlay, and 
whose source code is available [here](./src/kernel_opt.cpp). This last kernel 
is duplicated in the design, with one version using only a single memory bank, 
and the second version using a different memory bank for each buffer. It is used 
for the [kernel optimization notebooks](../pynqexamples/notebooks/2-kernel-optimization).

3. **Advanced Features**: this overlay includes a *vector addition* and *matrix
multiplication* kernels specifically developed for this overlay, for which the 
source code is available [here](./src/advanced_features.cpp). It is used for 
the [advanced features notebooks](../pynqexamples/notebooks/3-advanced-features).

## Supported Cards/Shells

Currently, we distribute overlays only for the following Alveo cards and shells:

Shell                    | Board             
-------------------------|-----------------
xilinx_u200_xdma_201830_2|Xilinx Alveo U200
xilinx_u250_xdma_201830_2|Xilinx Alveo U250

Designs are built using Vitis 2019.2.

## Rebuilding Overlays

Make sure you have cloned the Alveo-PYNQ repo using the `--recursive` option, 
so that the included git submodules are also pulled at checkout.
In case you haven't, you can check them out at a later stage by typing:
   ```bash
   git submodule update --init --recursive
   ```

To build xclbins for a new shell, move to the `overlays` folder and run the 
`make build` command, passing the appropriate `DEVICE`:
   ```bash
   cd overlays
   make build DEVICE=<target-shell>
   ```

You can then do `make install` to copy the overlays in the appropriate 
notebooks folder. 
If you want to do everything in one go (`build` and `install`):
   ```bash
   make DEVICE=<target-shell>
   ```

To install built xclbins in a specific path (different from the default one):
   ```bash
   make install INSTALL_PATH=<target-path>
   ```

It is expected that the target path contains the appropriate notebooks folders.
Otherwise, the installation will fail.

## Deploying Examples from Cloned Repo

As explained in the repository's main [README](../README.md), once you have 
synthesized and installed the overlays in the appropriate notebooks folder, you 
can deploy the examples to a target path directly from the cloned repository. 
This is currently the only way to deploy the examples when using manually 
synthesized overlays.

After having synthesized and installed the overlays, as explained above, move
to the root of this repository and run

```bash
python3 -m pynqexamples -p <target-path>
