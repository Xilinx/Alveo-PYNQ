#  Copyright (C) 2020 Xilinx, Inc
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from setuptools import setup, find_packages
from pynqutils.setup_utils import build_py, extend_package


__author__ = "Giuseppe Natale"
__copyright__ = "Copyright 2020, Xilinx"
__email__ = "pynq_support@xilinx.com"


# global variables
module_name = "pynq_alveo_examples"
data_files = []

with open("README.md", encoding="utf-8") as fh:
    readme_lines = fh.readlines()[4:]
long_description = ("".join(readme_lines))

extend_package(module_name, data_files)
setup(name=module_name,
      version="1.0.3",
      description="Introductory Examples for using PYNQ with Alveo",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Giuseppe Natale",
      author_email="pynq_support@xilinx.com",
      url="https://github.com/Xilinx/Alveo-PYNQ",
      packages=find_packages(),
      download_url="https://github.com/Xilinx/Alveo-PYNQ",
      package_data={
          "": data_files,
      },
      python_requires=">=3.8.0",
      # keeping 'setup_requires' only for readability - relying on
      # pyproject.toml and PEP 517/518
      setup_requires=[
          "pynq>=3.0.1",
          "pynqutils>=0.1.1"
      ],
      install_requires=[
          "pynq>=3.0.1",
          "pynqutils>=0.1.1",
          "jupyter",
          "jupyterlab",
          "plotly",
          "lz4",
          "matplotlib",
          "ipython"
      ],
      entry_points={
          "pynq.notebooks": [
              "0-welcome-to-pynq = {}.notebooks.0_welcome_to_pynq".format(
                  module_name),
              "1-introduction = {}.notebooks.1_introduction".format(
                  module_name),
              "2-kernel-optimization = {}.notebooks."
              "2_kernel_optimization".format(module_name),
              "3-advanced-features = {}.notebooks.3_advanced_features".format(
                  module_name),
              "4-building-and-emulation = {}.notebooks."
              "4_building_and_emulation".format(module_name),
              "data-compression = {}.notebooks.data_compression".format(
                  module_name)
          ]
      },
      cmdclass={"build_py": build_py},
      license="Apache License 2.0"
      )
