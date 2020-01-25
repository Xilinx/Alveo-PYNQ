# Introductory Examples for Alveo-PYNQ

This project includes introductory examples for using PYNQ with Alveo. It
requires `pynq` version `2.5.1` and above to work.

Please refer to the [README](overlays/README.md) in the `overlays` folder for 
more information regarding the used overlays and how they are created.

Please notice that not all examples might be available for all the target 
cards/shells. Supported cards and related shells are listed in the overlays 
[README](overlays/README.md).

## Quick Start

Simply install the `pynq-alveo-examples` package using `pip`:
   ```bash
   pip3 install pynq-alveo-examples
   ```

Or if you are using `conda` (`pip3` might not be available, `pip` will refer to 
Python3)
   ```bash
   pip install pynq-alveo-examples
   ```

After the package is installed, to get your own copy of all the notebooks 
available run:
   ```bash
   pynq get-notebooks
   cd pynq-notebooks
   ```

You can try things out by running:
   ```bash
   jupyter notebook
   ```

There are a number of additional options for the `pynq get-notebooks` command,
you can list them by typing 
   ```bash
   pynq get-notebooks --help
   ```

## Install Examples using Cloned Repo

Alternatively to what shown above, you might also want to install the package
from the cloned repository. This might be useful in case you have synthesized 
the included overlays for a board/shell for which we do not distribute overlays
ourselves, as explained in the overlays [README](overlays/README.md). To do so,
`cd` in the root of the cloned repository and run:

```bash
pip3 install -U .
```

Remember that when using conda, `pip3` might not be available, while `pip` will
refer to Python3. In this case, use `pip` instead of `pip3`.

After that, run the `pynq get-notebooks` command to get the examples.
