from max30100 import *
import time
import json

mx30 = MAX30100()

mx30.enable_spo2()

mean_filter_size = 15

def create_values(t):
    read_values = {}
    t1 = time.time()
    count = 0
    while (time.time()-t1) < t:
        mx30.read_sensor()
        ir = mx30.ir
        red = mx30.red
        read_values[count] = {"ir": ir, "red": red}
        count += 1
    print("remove finger")
    print(count)
    return read_values

def filtered_output(x, prev_w, alpha):
    filtered_w = x + alpha * prev_w
    y = filtered_w - prev_w
    return filtered_w, y

def dcremoval(values, start_w, alpha):
    filtered_values = {}
    w_r = start_w
    w_ir = start_w
    for item in values:
        temp_ir = filtered_output(values[item]["ir"], w_ir, alpha)
        temp_r = filtered_output(values[item]["red"], w_r, alpha)
        w_ir,y_ir = temp_ir
        w_r,y_r = temp_r
        filtered_values[item] = {"ir": y_ir, "r": y_r}
    return filtered_values

values = create_values(10)
dc_result = dcremoval(values, 20000, 0.95)



        

