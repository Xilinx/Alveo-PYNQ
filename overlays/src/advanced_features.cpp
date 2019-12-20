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


#include <hls_stream.h>

#define N 512

typedef int data_type;

void read_data(const int* data, hls::stream<int>& stream) {
	for (int i = 0; i < N * N; ++i) {
#pragma HLS PIPELINE II=1
		stream.write(*data++);
	}
}

void write_data(hls::stream<int>& stream, int* data) {
	for (int i = 0; i < N * N; ++i) {
#pragma HLS PIPELINE II=1
		*data++ = stream.read();
	}
}

void stream_to_array(hls::stream<int>& stream, int data[N][N]) {
	for (int i = 0; i < N; ++i) {
		for (int j = 0; j < N; ++j) {
#pragma HLS PIPELINE II=1
			data[i][j] = stream.read();
		}
	}
}

struct wide_stream {
	int data[N];
};


void mmult_kernel(hls::stream<wide_stream>& in_a, hls::stream<wide_stream>& in_b, hls::stream<int>& out) {
    for (int i = 0; i < N * N; i++) {
#pragma HLS PIPELINE II=1
		  data_type result = 0;
		  wide_stream a = in_a.read();
#pragma HLS ARRAY_PARTITION variable=a.data complete dim=1
		  wide_stream b = in_b.read();
#pragma HLS ARRAY_PARTITION variable=b.data complete dim=1
		  for (int k = 0; k < N; k++) {
#pragma HLS UNROLL
			   data_type term = a.data[k] * b.data[k];
			   result += term;
		  }
		  out.write(result);

    }
}

void to_wide_a(hls::stream<data_type>& in, hls::stream<wide_stream>& out) {
	for (int i = 0; i < N; ++i) {
		wide_stream transfer;
#pragma HLS ARRAY_PARTITION variable=transfer.data complete
		for (int j = 0; j < N; ++j){
#pragma HLS PIPELINE II=1
			transfer.data[j] = in.read();
			if (j == N-1) {
				out.write(transfer);
			}
		}
	}
}

void replicate_a(hls::stream<wide_stream>&in, hls::stream<wide_stream>& out) {
	for (int i = 0; i < N; ++i) {
		wide_stream elem = in.read();
#pragma HLS ARRAY_PARTITION variable=elem.data complete dim=1
		for (int j = 0; j < N; ++j) {
#pragma HLS PIPELINE II=1
			out.write(elem);
		}
	}
}

void to_wide_b(data_type _B[N][N], hls::stream<wide_stream>& out) {
	for (int i = 0; i < N; ++i) {
		for (int j = 0; j < N; ++j) {
#pragma HLS PIPELINE II=1
			wide_stream transfer;
#pragma HLS ARRAY_PARTITION variable=transfer.data complete dim=1
			for (int k = 0; k < N; ++k) {
				transfer.data[k] = _B[k][j];
			}
			out.write(transfer);
		}
	}
}

extern "C" void mmult(const int* A, const int* B, int* C)
{
#pragma HLS DATAFLOW

// #pragma HLS INTERFACE s_axilite register port=M
#pragma HLS INTERFACE s_axilite port=return bundle=control
#pragma HLS INTERFACE m_axi port=A offset=slave bundle=gmem_AC depth=32*32 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE m_axi port=B offset=slave bundle=gmem_B  depth=32*32 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE m_axi port=C offset=slave bundle=gmem_AC depth=32*32 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256

	hls::stream<int> a_stream("a_stream");
	hls::stream<int> b_stream("b_stream");
	hls::stream<int> c_stream("c_stream");

	read_data(A, a_stream);
	read_data(B, b_stream);


     data_type _B[N][N];
#pragma HLS array_partition variable=_B cyclic factor=256 dim=1

     hls::stream<wide_stream> a_wide("a_wide");
     hls::stream<wide_stream> a_replicated("a_replicated");
     hls::stream<wide_stream> b_wide("b_wide");

     to_wide_a(a_stream, a_wide);
     replicate_a(a_wide, a_replicated);
     stream_to_array(b_stream, _B);

     to_wide_b(_B, b_wide);

     mmult_kernel(a_replicated, b_wide, c_stream);
     write_data(c_stream, C);
}

void add_kernel(hls::stream<int>& a, hls::stream<int>& b, hls::stream<int>& c) {
	for (int i = 0; i < N * N; ++i) {
		c.write(a.read() + b.read());
	}
}

extern "C" void vadd(const int* A, const int* B, int* C) {
#pragma HLS INTERFACE s_axilite port=return bundle=control
#pragma HLS INTERFACE m_axi port=A offset=slave bundle=gmem_AC depth=256 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE m_axi port=B offset=slave bundle=gmem_B  depth=16*16 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS INTERFACE m_axi port=C offset=slave bundle=gmem_AC depth=16*16 num_read_outstanding=8 num_write_outstanding=8 max_read_burst_length=256 max_write_burst_length=256
#pragma HLS DATAFLOW

	hls::stream<int> a_stream("a_stream");
	hls::stream<int> b_stream("b_stream");
	hls::stream<int> c_stream("c_stream");

	read_data(A, a_stream);
	read_data(B, b_stream);

	add_kernel(a_stream, b_stream, c_stream);

	write_data(c_stream, C);
}
