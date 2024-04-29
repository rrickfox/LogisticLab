import full_depth_first_threading
import start_with_first_jump
import time

start_time = time.time()
ret = full_depth_first_threading.one_vehicle_dfs_threading(120, False)
print(f"first solution ({ret[0]}) after {time.time() - start_time} seconds")
ret2 = start_with_first_jump.one_vehicle_dfs_threaded(ret[1], 180, False)
print(ret2)
print(f"--- {(time.time() - start_time)} seconds ---")