/**********
 * Copyright (C) 2019 Xilinx, Inc
 *
 * Licensed under the Apache License, Version 2.0 (the "License"). You may
 * not use this file except in compliance with the License. A copy of the
 * License is located at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 *********/

/**********
 *
 * Author: Peter Ogden
 * Email:  pynq_support@xilinx.com
 *
 *********/

#include <ap_int.h>

typedef ap_uint<512> uint512_t;

extern "C" void vadd_wide(uint512_t* a, uint512_t* b, uint512_t* c, int count) {
#pragma HLS INTERFACE s_axilite port=return bundle=control
#pragma HLS INTERFACE m_axi port=a offset=slave bundle=gmem_a depth=4096 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE s_axilite port=a bundle=control
#pragma HLS INTERFACE m_axi port=b offset=slave bundle=gmem_b  depth=4096 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE s_axilite port=b bundle=control
#pragma HLS INTERFACE m_axi port=c offset=slave bundle=gmem_c depth=4096 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE s_axilite port=c bundle=control
#pragma HLS INTERFACE s_axilite port=count bundle=control
        int iterations = count >> 4;
        for (int i = 0; i < iterations; ++i) {
#pragma HLS PIPELINE II=1
                uint512_t a_val = *a++;
                uint512_t b_val = *b++;
                uint512_t c_val;
                for (int j = 0; j < 16; ++j) {
#pragma HLS UNROLL
                    int hi = j*32 + 31;
                    int lo = j*32;
                    c_val.range(hi,lo) = a_val.range(hi,lo) + b_val.range(hi,lo);
                }
                *c++ = c_val;
        }
}
