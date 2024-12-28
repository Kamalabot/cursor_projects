#include <stdio.h>

// Kernel definition
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (tid < n) {
        c[tid] = a[tid] + b[tid];
    }
}

int main() {
    // Reduce vector size for better visualization
    int n = 10;  // Smaller size for demonstration
    size_t size = n * sizeof(float);

    // Host vectors
    float *h_a, *h_b, *h_c;
    // Device vectors
    float *d_a, *d_b, *d_c;

    printf("1. Allocating host memory...\n");
    h_a = (float*)malloc(size);
    h_b = (float*)malloc(size);
    h_c = (float*)malloc(size);

    // Initialize vectors with different values
    printf("\n2. Initializing host vectors:\n");
    printf("Vector A: ");
    for (int i = 0; i < n; i++) {
        h_a[i] = i * 1.0f;  // [0,1,2,3,...]
        printf("%.1f ", h_a[i]);
    }
    printf("\nVector B: ");
    for (int i = 0; i < n; i++) {
        h_b[i] = i * 2.0f;  // [0,2,4,6,...]
        printf("%.1f ", h_b[i]);
    }
    printf("\n");

    printf("\n3. Allocating GPU memory...\n");
    cudaError_t error;
    error = cudaMalloc(&d_a, size);
    if (error != cudaSuccess) {
        printf("Error allocating d_a: %s\n", cudaGetErrorString(error));
        return -1;
    }
    error = cudaMalloc(&d_b, size);
    if (error != cudaSuccess) {
        printf("Error allocating d_b: %s\n", cudaGetErrorString(error));
        return -1;
    }
    error = cudaMalloc(&d_c, size);
    if (error != cudaSuccess) {
        printf("Error allocating d_c: %s\n", cudaGetErrorString(error));
        return -1;
    }

    printf("\n4. Copying data from CPU to GPU...\n");
    cudaMemcpy(d_a, h_a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, h_b, size, cudaMemcpyHostToDevice);

    printf("\n5. Configuring CUDA kernel launch parameters...\n");
    int blockSize = 256;
    int numBlocks = (n + blockSize - 1) / blockSize;
    printf("   - Block size: %d\n", blockSize);
    printf("   - Number of blocks: %d\n", numBlocks);
    printf("   - Total threads: %d\n", blockSize * numBlocks);

    printf("\n6. Launching CUDA kernel...\n");
    vectorAdd<<<numBlocks, blockSize>>>(d_a, d_b, d_c, n);
    
    // Check for kernel launch errors
    error = cudaGetLastError();
    if (error != cudaSuccess) {
        printf("Kernel launch error: %s\n", cudaGetErrorString(error));
        return -1;
    }

    // Wait for GPU to finish
    cudaDeviceSynchronize();

    printf("\n7. Copying results back to CPU...\n");
    cudaMemcpy(h_c, d_c, size, cudaMemcpyDeviceToHost);

    // Print results
    printf("\n8. Results:\n");
    printf("Vector A: ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", h_a[i]);
    }
    printf("\nVector B: ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", h_b[i]);
    }
    printf("\nResult : ");
    for (int i = 0; i < n; i++) {
        printf("%.1f ", h_c[i]);
    }
    printf("\n");

    // Verify results
    printf("\n9. Verifying results...\n");
    bool correct = true;
    for (int i = 0; i < n; i++) {
        if (h_c[i] != h_a[i] + h_b[i]) {
            printf("Error at index %d: %.1f + %.1f = %.1f (expected: %.1f)\n",
                   i, h_a[i], h_b[i], h_c[i], h_a[i] + h_b[i]);
            correct = false;
            break;
        }
    }
    if (correct) {
        printf("All calculations are correct!\n");
    }

    printf("\n10. Cleaning up memory...\n");
    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    free(h_a);
    free(h_b);
    free(h_c);

    printf("\nProgram completed successfully!\n");
    return 0;
}