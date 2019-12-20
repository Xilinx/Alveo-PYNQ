#  Copyright (C) 2019 Xilinx, Inc
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

import os
import argparse
from shutil import move, copytree, rmtree


__author__ = "Giuseppe Natale"
__copyright__ = "Copyright 2019, Xilinx"
__email__ = "pynq_support@xilinx.com"


NOTEBO0KS_PATH = os.path.join(os.path.dirname(__file__), "notebooks")
TARGET_NB_DIR = "pynq-examples"


def _examples_parser():
    """Initialize and return the argument parser."""
    parser = argparse.ArgumentParser(description="Deploy Alveo-PYNQ "
                                     "introductory examples")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--shell", type=str,
                       help="Provide a specific shell name")
    group.add_argument("-i", "--interactive", action="store_true",
                       help="Detect available shells and ask which one to use")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force installation even if target example "
                        "directory already exists. The existing directory "
                        "will be renamed adding a timestamp")
    parser.add_argument("-p", "--path", type=str,
                        help="Specify a custom path to install the example "
                        "notebooks. Default is the current working "
                        "directory. A 'pynq-examples' directory will be "
                        "created in the specified path with all the examples.")
    return parser


def _detect_shells(active_only=False):
    """Return a list containing all the detected devices' shells."""
    if "XILINX_XRT" in os.environ:
        from pynq.pl_server import Device
        devices = Device.devices
        if not devices:
            raise Exception("No device found in the system")
        # shell at position 0 is default device
        if active_only:
            return Device.active_device.name
        return [d.name for d in devices]
    else:
        raise Exception("Environment variable XILINX_XRT not found, "
                        "meaning XRT could not be detected, even though "
                        "it is required. Make sure you have sourced the "
                        "XRT setup script before trying again")


def _download_file(download_link, name, path=None):
    """Download the file

    Parameters
    ----------
        download_link: str
            The download link to use
        name: str
            The target file name when saving the file to disk
        path: str
            The path where to save the file. If `None`, the current working
            directory will be used instead
    """
    import urllib.request
    if not path:
        path = os.getcwd()
    file_path = os.path.join(path, name)
    with urllib.request.urlopen(download_link) as response, \
            open(file_path, "wb") as out_file:
        data = response.read()
        out_file.write(data)


def _copy_notebooks(shell, path):
    """ Copy notebooks and download overlays to the target path.

    Removes notebooks for which the associated xclbin could not be found or
    downloaded, and warns the user.

    Parameters
    ----------
        shell: str
            The target shell for the examples. If an xclbin is already found,
            no shell-based download will be done and the shell will be ignored
            for that xclbin
        path: str
            The path where notebooks and overlays are dropped
    """
    copytree(NOTEBO0KS_PATH, path)
    files_to_delete = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xclbin.link"):
                file_path = os.path.join(root, file)
                xclbin = file.replace(".xclbin.link", ".xclbin")
                if not os.path.isfile(os.path.join(root, xclbin)):
                    # xclbin not found in directory, attempt xclbin download
                    import json
                    with open(file_path) as f:
                        links = json.load(f)
                        if shell in links:
                            _download_file(links[shell], xclbin, root)
                        else:  # no xclbin found, delete notebooks
                            files_to_delete.extend([
                                os.path.join(root, ipynb)
                                for ipynb in files
                                if ipynb.endswith(".ipynb")])
                # mark json file for deletion
                files_to_delete.append(file_path)
    # remove files marked for deletion
    for file in files_to_delete:
        os.remove(file)
    # remove empty directories
    for root, dirs, files in os.walk(path):
        for d in dirs:
            d_path = os.path.join(root, d)
            if len(os.listdir(d_path)) == 0:
                import warnings
                os.rmdir(d_path)
                warnings.warn("Could not find valid overlay for notebooks '{}'"
                              ", these notebooks will not be "
                              "installed".format(d))


def main():
    parser = _examples_parser()
    args = parser.parse_args()
    if args.path:
        install_path = args.path
        os.makedirs(install_path, exist_ok=True)
    else:
        install_path = os.getcwd()
    install_fullpath = os.path.join(install_path, TARGET_NB_DIR)
    tmp_fullpath = os.path.join(install_path, "." + TARGET_NB_DIR)
    if os.path.exists(install_fullpath):
        if args.force:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
            backup_dir = TARGET_NB_DIR + '_' + timestamp
            backup_fullpath = os.path.join(install_path, backup_dir)
            move(install_fullpath, backup_fullpath)
        else:
            raise Exception("Target notebook directory already exists. "
                            "Specify another path or use the 'force' option "
                            "to proceed")
    if args.shell:
        shell = args.shell
    elif args.interactive:
        shells = list(dict.fromkeys(_detect_shells()))
        print("Detected shells:")
        for i in range(len(shells)):
            print("{}) - {}\n".format(i, shells[i]))
        idx = -1
        while idx < 0 or idx >= len(shells):
            idx = input("Select for which shell you want to install the "
                        "examples [0-{}]: ".format(len(shells)-1))
            try:
                idx = int(idx)
                if idx < 0 or idx >= len(shells):
                    raise ValueError
            except:
                print("Invalid choice.")
                idx = -1
        shell = shells[idx]
    else:  # default case, detect shells and use default device
        shell = _detect_shells(active_only=True)
    try:
        if os.path.isdir(tmp_fullpath):
            rmtree(tmp_fullpath)
        _copy_notebooks(shell, tmp_fullpath)
        if len(os.listdir(tmp_fullpath)) == 0:
            import warnings
            os.rmdir(tmp_fullpath)
            warnings.warn("No examples available for target shell, nothing "
                          "will be installed")
        else:
            move(tmp_fullpath, install_fullpath)
    except Exception as e:
        if os.path.isdir(tmp_fullpath):
            rmtree(tmp_fullpath)
        if os.path.isdir(install_fullpath):
            rmtree(install_fullpath)
        raise e
