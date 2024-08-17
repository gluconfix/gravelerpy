# GravelerPy

gravelerpy is an highly optimized Python program which reduces the time of the [graveler](https://github.com/arhourigan/graveler/blob/main/graveler.py) program from 8days to just a few seconds  

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies.

```bash
pip install numpy scipy tqdm
```

## Optimizations
1. **Imports**:
    - `numpy`: Efficient numerical computations.
    - `multiprocessing`: Parallel processing to utilize multiple CPU cores.
    - `scipy.stats.binom`: Generates binomial random variables efficiently.
    - `tqdm`: Provides a fast, extensible progress bar.
    - `time`: Used for managing delays to prevent busy-waiting.
2. **Worker Function**:

   - **Purpose**: Each worker performs a large number of simulations, finding the maximum value in each batch and updating the shared progress counter.
   - **Optimizations**:
     - **Numpy Vectorization**: Utilizes `numpy` functions (`binom.rvs` for generating samples and `np.max` for finding the maximum), which are optimized and faster than equivalent Python loops.
     - **Efficient Sampling**: Generates large batches of samples at once, reducing the overhead compared to generating samples one at a time.
     - **Direct Counter Updates**: Updates the shared progress counter directly using `multiprocessing.Manager().Value`, which is thread-safe and simplifies the shared state management.
3. **Progress Listener Function**:
   - **Purpose**: Monitors the progress counter and updates the progress bar accordingly.
   - **Optimizations**:
     - **Efficient Progress Bar Updates**: Uses `tqdm` to handle progress updates efficiently, minimizing I/O operations and providing a smooth visual indication of progress.
     - **Sleep Interval**: Includes `time.sleep(1)` to reduce CPU usage during progress polling, which prevents busy-waiting and lowers CPU load.
4. **Main Function**:
   - **Setup**: Configures the number of processes based on available CPU cores, calculates the number of batches, and initializes the multiprocessing pool.
   - **Process Distribution**: Distributes the workload across multiple processes using starmap, which allows each process to handle a subset of the total work.
   - **Progress Management**: Starts a separate process for the progress listener and ensures it receives the final update after all worker processes complete.

5. **Performance Considerations**:
   - **Parallel Processing**: Utilizes all available CPU cores to perform simulations concurrently, significantly speeding up the computation.
   - **Batch Processing**: Processes large batches of samples at once to minimize the overhead and efficiently use computational resources.
   - **Efficient Communication**: Uses a shared counter for progress tracking, which simplifies communication between processes and the progress listener.


## License

[MIT](https://choosealicense.com/licenses/mit/)