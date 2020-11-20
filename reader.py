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

def meanDiff(M, filtered_values):
    index = 0
    sum = 0
    count = 0
    average = 0

    sum -= filtered_values[index]["ir"]
    filtered[index]["ir"] = M
    sum += filtered_values[index]["ir"]
    index += 1
    index = index % mean_filter_size

    if count < mean_filter_size:
        count += 1

    avg = sum / count
    return avg - M

def butterworthFilter(x, filtered_values):
    pass

def beat_detect()




values = create_values(10)
dc_result = dcremoval(values, 20000, 0.95)
meandiff_result = meanDiff(0, dc_result)


        

