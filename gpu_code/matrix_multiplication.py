import os
# Clear any existing CUDA environment variables
os.environ.pop('CUDA_COMPUTE_CAPABILITY', None)

import numpy as np
from numba import cuda, float32
from numba.cuda.cudadrv.driver import CudaAPIError
import math
import time

# Configure CUDA target architecture
cuda.select_device(0)  # Select first CUDA device
# Set PTX version compatible with CUDA 12.2
cuda.set_ptx_compilation_target('sm_75')  # Using a more compatible compute capability

@cuda.jit
def matrix_multiply_kernel(A, B, C):
    """CUDA kernel for matrix multiplication"""
    row, col = cuda.grid(2)
    
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.0
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row, col] = tmp

def matrix_multiply_gpu(A, B):
    """Perform matrix multiplication using GPU"""
    if A.shape[1] != B.shape[0]:
        raise ValueError("Matrix dimensions do not match for multiplication")
    
    M, N = A.shape[0], B.shape[1]
    C = np.zeros((M, N), dtype=np.float32)
    
    try:
        # Copy matrices to device
        print("Copying matrices to GPU...")
        d_A = cuda.to_device(A)
        d_B = cuda.to_device(B)
        d_C = cuda.to_device(C)
        
        # Use smaller block size for better compatibility
        BLOCK_SIZE = 16
        grid_x = math.ceil(M / BLOCK_SIZE)
        grid_y = math.ceil(N / BLOCK_SIZE)
        
        print(f"Grid dimensions: ({grid_x}, {grid_y})")
        print(f"Block dimensions: ({BLOCK_SIZE}, {BLOCK_SIZE})")
        
        # Launch kernel
        print("\nLaunching CUDA kernel...")
        start_time = time.time()
        matrix_multiply_kernel[(grid_x, grid_y), (BLOCK_SIZE, BLOCK_SIZE)](d_A, d_B, d_C)
        cuda.synchronize()
        gpu_time = time.time() - start_time
        
        print("Copying result back to CPU...")
        C = d_C.copy_to_host()
        
        return C, gpu_time
        
    except CudaAPIError as e:
        print(f"CUDA Error: {e}")
        raise

def main():
    # Start with smaller matrices for testing
    M = 1024  # rows of A
    N = 1024  # columns of B
    K = 1024  # columns of A / rows of B
    
    print(f"Matrix dimensions:")
    print(f"A: {M}x{K}")
    print(f"B: {K}x{N}")
    print(f"C: {M}x{N}")
    
    print("\nInitializing matrices...")
    A = np.random.rand(M, K).astype(np.float32)
    B = np.random.rand(K, N).astype(np.float32)
    
    try:
        C, gpu_time = matrix_multiply_gpu(A, B)
        
        # Verify results
        print("\nVerifying results...")
        cpu_start = time.time()
        C_cpu = np.dot(A, B)
        cpu_time = time.time() - cpu_start
        
        if np.allclose(C, C_cpu, rtol=1e-5):
            print("✓ Results match CPU computation!")
        else:
            print("✗ Results DO NOT match CPU computation!")
        
        print("\nPerformance comparison:")
        print(f"GPU Time: {gpu_time*1000:.2f} ms")
        print(f"CPU Time: {cpu_time*1000:.2f} ms")
        print(f"Speedup: {cpu_time/gpu_time:.2f}x")
        
        print("\nSample of result matrix (top-left 3x3):")
        print(C[:3, :3])
        
    except Exception as e:
        print(f"Error during computation: {e}")

if __name__ == "__main__":
    # Print CUDA device information
    device = cuda.get_current_device()
    print(f"Using CUDA device: {device.name}")
    print(f"Compute Capability: {device.compute_capability}")
    print(f"CUDA driver version: {cuda.runtime.get_version()}\n")
    
    main()
