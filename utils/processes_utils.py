import multiprocessing as mp
import time


def integer_process_worker(stop_time: float, index: int, queue: mp.Queue) -> None:
    '''Run integer operations until stop_time and put this process total operations in queue.'''
    value = 1 + index
    iterations = 0

    while time.perf_counter() < stop_time:
        value = value * 3
        value = value + 7
        value = value - 5
        value = value // 3
        value = value * 2
        iterations += 1

    queue.put(iterations * 5)


def float_process_worker(stop_time: float, index: int, queue: mp.Queue) -> None:
    '''Run floating-point operations until stop_time and put this process total operations in queue.'''
    value = 1.0 + float(index)
    iterations = 0

    while time.perf_counter() < stop_time:
        value = value * 3.0
        value = value + 7.0
        value = value - 5.0
        value = value / 3.0
        value = value * 2.0
        iterations += 1

    queue.put(iterations * 5)


def processes_manager(worker, process_count: int, duration_seconds: float) -> tuple[float, int, float]:
    '''Start worker processes, wait for completion, and return elapsed time and throughput.'''
    queue: mp.Queue = mp.Queue()
    processes = []

    start = time.perf_counter()
    stop_time = start + duration_seconds

    for index in range(process_count):
        process = mp.Process(target=worker, args=(stop_time, index, queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    totals = [queue.get() for _ in range(process_count)]
    elapsed = time.perf_counter() - start
    total_operations = sum(totals)
    ops_per_second = total_operations / elapsed
    return elapsed, total_operations, ops_per_second