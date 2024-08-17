import numpy as np
import multiprocessing as mp
from scipy.stats import binom
from tqdm import tqdm
import time


def worker(seed, num_batches, batch_size, progress_counter):
    np.random.seed(seed)
    max_ones = 0

    for _ in range(num_batches):
        samples = binom.rvs(n=231, p=0.25, size=batch_size)
        batch_max = np.max(samples)
        if batch_max > max_ones:
            max_ones = batch_max

        # Notify progress
        progress_counter.value += batch_size

    return max_ones


def progress_listener(progress_counter, total_simulations):
    with tqdm(total=total_simulations) as pbar:
        last_value = 0
        while True:
            current_value = progress_counter.value
            if current_value >= total_simulations:
                pbar.update(total_simulations - last_value)
                break
            pbar.update(current_value - last_value)
            last_value = current_value
            time.sleep(1)  # Sleep briefly to avoid busy-waiting


def main():
    num_processes = mp.cpu_count()
    total_simulations = 1_000_000_000
    batch_size = 10_000_000
    num_batches = total_simulations // batch_size
    num_batches_per_process = num_batches // num_processes

    # Create a manager and a Value for tracking progress
    with mp.Manager() as manager:
        progress_counter = manager.Value('i', 0)
        pool = mp.Pool(num_processes)

        # Start the progress listener
        listener = mp.Process(target=progress_listener, args=(progress_counter, total_simulations))
        listener.start()

        # Distribute the work across processes
        seeds = np.random.randint(0, 2 ** 31 - 1, size=num_processes)
        results = pool.starmap(worker,
                               [(seed, num_batches_per_process, batch_size, progress_counter) for seed in seeds])

        # Close the pool and wait for all processes to complete
        pool.close()
        pool.join()

        # Ensure that progress listener completes
        progress_counter.value = total_simulations  # Ensure progress_listener can finish
        listener.join()

        # Combine results
        highest_ones = max(results)

        print("Estimated Highest Ones Roll:", highest_ones)


if __name__ == "__main__":
    main()
