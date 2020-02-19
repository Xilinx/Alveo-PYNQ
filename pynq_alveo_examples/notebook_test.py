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

__author__ = "Peter Ogden"
__copyright__ = "Copyright 2020, Xilinx"
__email__ = "pynq_support@xilinx.com"


import os
import re
from pynq.utils import run_notebook

NOTEBOOK_PATH = os.path.join(os.path.dirname(__file__), 'notebooks')


def get_stdout(result, cell_num):
    outputs = result.outputs[cell_num-1]
    for output in outputs:
        if output['output_type'] == 'stream' and output['name'] == 'stdout':
            return output['text']
    return None


_time_lookup = {
    's': 1,
    'ms': 0.001,
    'us': 0.000001
}


def get_timeit_time(result, cell_num):
    stdout = get_stdout(result, cell_num)
    m = re.match('([0-9.]+) ([a-z]+)', stdout)
    if m is None:
        raise RuntimeError('No timing data found')
    return float(m[1]) * _time_lookup[m[2]]


def test_welcome():
    # No cell outputs to verify
    result = run_notebook(
        '0_welcome_to_pynq/welcome-to-pynq.ipynb', NOTEBOOK_PATH)


def test_intro_add():
    result = run_notebook(
        '1_introduction/1-vector-addition.ipynb', NOTEBOOK_PATH)
    # TODO: add stdout compare for first cell
    assert result._7 is True  # First compare
    assert get_stdout(result, 1) == 'SUCCESS!\n'


def test_intro_add_mult():
    result = run_notebook(
        '1_introduction/2-vadd-and-vmult.ipynb', NOTEBOOK_PATH)
    # TODO: add stdout compare for first cell
    assert result._7 is True  # First compare
    assert get_stdout(result, 1) == 'SUCCESS!\n'


def test_intro_explore():
    result = run_notebook(
        '1_introduction/3-exploring-a-bitstream.ipynb', NOTEBOOK_PATH)


def test_intro_opencl():
    result = run_notebook(
        '1_introduction/4-opencl-comparison.ipynb', NOTEBOOK_PATH)


def test_kernel_opt():
    result = run_notebook(
        '2_kernel_optimization/1-kernel-optimizations.ipynb', NOTEBOOK_PATH)
    assert result._5 is True
    assert result._15 is True
    assert result._18 is True


def test_using_streams():
    result = run_notebook(
        '2_kernel_optimization/2-using-streams.ipynb', NOTEBOOK_PATH)
    assert result._10 is True


def test_streams_memories():
    result = run_notebook(
        '2_kernel_optimization/3-memories-and-streams.ipynb', NOTEBOOK_PATH)
    assert result._2 == result._4
    assert result._2 == result._8
    assert result._3 == result._6
    assert result._2 + 4 * 1024 * 1024 == result._3
    assert result._9 == 'krnl_stream_vadd_1.out_r'
    assert result._10 is not None


def test_scheduling():
    result = run_notebook(
        '3_advanced_features/1-efficient-accelerator-scheduling.ipynb',
        NOTEBOOK_PATH)
    assert result._5 is True
    assert result._11 is True

def test_compression_intro():
    result = run_notebook(
        'data_compression/intro-to-compression.ipynb', NOTEBOOK_PATH)
    assert result._12
    assert result._13 < 1

def test_compression_overlapped():
    result = run_notebook(
        'data_compression/overlapping-communication-compute.ipynb',
        NOTEBOOK_PATH)
    assert result._8
    base_time = get_timeit_time(result, 9)
    overlapped_time = get_timeit_time(result, 15)
    assert overlapped_time < base_time   

def test_compression_zlib():
    result = run_notebook(
        'data_compression/zlib-compression.ipynb', NOTEBOOK_PATH)
    assert result._20
    hw_time = get_timeit_time(result, 23)
    sw_time = get_timeit_time(result, 24)

