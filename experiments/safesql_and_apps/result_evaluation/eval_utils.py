import multiprocessing
import datetime
import pytz


class TimeUtils:
    tz = pytz.timezone('America/Los_Angeles')
    
    @staticmethod
    def get_current_time():
        return datetime.datetime.now(TimeUtils.tz).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_timestamp():
        return datetime.datetime.now(TimeUtils.tz).timestamp()

    @staticmethod
    def format_time(seconds):
        return str(datetime.timedelta(seconds=seconds))


def mp_solve(func, args, num_processes=32, timeout=300):
    start_time = TimeUtils.get_current_timestamp()
    formatted_start_time = TimeUtils.get_current_time()
    print(f'[DEBUG] Using {num_processes} processes for solving {len(args)} tasks (start time: {formatted_start_time})')    
    
    all_returns = []
    with multiprocessing.Pool(num_processes) as pool:
        mp_task = pool.starmap_async(func, args)
        try:
            all_returns = mp_task.get(timeout=timeout)
        except multiprocessing.TimeoutError as e:
            print("Global timeout reached!")
            pool.terminate()
            for p in pool._pool:
                p.terminate()
            all_returns = []
        except Exception as e:
            print(f"Unexpected error: {e}")
            pool.terminate()
            all_returns = []
        finally:
            pool.close()
            pool.join()
    
    end_time = TimeUtils.get_current_timestamp()
    used_time = round(end_time - start_time)
    formatted_used_time = TimeUtils.format_time(used_time)
    print(f"Finished processing {len(all_returns)} tasks (total time: {formatted_used_time})")
    return all_returns